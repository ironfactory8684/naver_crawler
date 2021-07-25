import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import csv

def get_news(n_url): 
    news_detail = [] 
    #print(n_url) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    pdate = bsoup.select('.t11')[0].text[:11] 
    news_detail.append(pdate) 
    
    # 신문사 크롤링
    pcompany = bsoup.select('#footer address')[0].a.text
    news_detail.append(pcompany) 

    # html 파싱 
    title = bsoup.select('h3#articleTitle')[0].text 
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select('#articleBodyContents')[0].text.replace('\n', " ") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 

    return news_detail


def comments(url): #댓글 함수
    
    # 댓글을 달 빈 리스트를 생성합니다.
    List=[] 

    oid=url.split("oid=")[1].split("&")[0] 
    aid=url.split("aid=")[1]
    page=1     
    header = { 
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
        "referer":url, 

    }  
    while True : 
        c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"+oid+"%2C"+aid+"&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page="+str(page)+"&refresh=false&sort=FAVORITE"  
    # 파싱하는 단계입니다.
        r=requests.get(c_url,headers=header) 
        cont=BeautifulSoup(r.content,"html.parser")     
        total_comm=str(cont).split('comment":')[1].split(",")[0] 

        match=re.findall('"contents":([^\*]*),"userIdNo"', str(cont)) 
    # 댓글을 리스트에 중첩합니다.
        List.append(match) 
    # 한번에 댓글이 20개씩 보이기 때문에 한 페이지씩 몽땅 댓글을 긁어 옵니다.
        if int(total_comm) <= ((page) * 20): 
            break 
        else :  
            page+=1
    final = flatten(List)
    AA= "댓글(" + str(len(final)) + ")"
    final = "".join(final)
    final = re.sub('[a-zA-Z]', '', final)
    final = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(]','', final)
    return [AA] + [final]

def flatten(l): # 여러 리스트들을 하나로 묶어 주는 함수입니다.
        flatList = [] 
        for elem in l: 
            # if an element of a list is a list 
            # iterate over this list and add elements to flatList  
            if type(elem) == list: 
                for e in elem: 
                    flatList.append(e) 
            else: 
                flatList.append(elem) 
        return flatList


def crawler(query, s_date, e_date,f, news_office):
    page = 1
    while page <5000:    
        #print(page)
        if news_office:
            url = "https://search.naver.com/search.naver?where=news&query=" + \
            query +"&sm=tab_opt&sort=2&photo=0&field=0&reporter_article=&pd=3&ds=" + \
            s_date+"&de="+e_date+ "&docid=&mynews=1&start="+str(page)+"&refresh_start=0&related=0"+\
            "office_section_code=1&news_office_checked="+news_office
        else:
            url = "https://search.naver.com/search.naver?where=news&query=" + \
            query +"&sm=tab_opt&sort=2&photo=0&field=0&reporter_article=&pd=3&ds=" + \
            s_date+"&de="+e_date+ "&docid=&mynews=1&start="+str(page)+"&refresh_start=0&related=0"
        #print(url)
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        req = requests.get(url,headers=header)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')
        i=0 #한 페이지당 네이버 뉴스의 개수
        for urls in soup.select("a.info"):
            try :
                article=urls['href']
            
                #남은 것중 네이버 뉴스를 골라낸다
                if article.startswith("https://news.naver.com"):
                    i+=1
                    print("네이버 뉴스",page,"-", i,":")
                    print(article)
                
                    AD = article.split("aid=")[1]  # 기사의 고유 아이디값
                
                    news_detail = get_news(article)  # 기사의 고유 아이디 값 컬럼 추가
                    # title, content

                    CA=comments(article)

                    CA= [AD]+news_detail+CA   #가독성을 위해..
            
                    wr=csv.writer(f)
                    wr.writerow(CA)
            
                #네이버 뉴스 링크가 없는 것
                # else:
                #     print("네이버 뉴스 X")
        
            #오류 출력
            except Exception as e:
                print(e)
                break
                        
        page += 10
        i=0
    
    f.close()
    print("크롤링이 종료되었습니다.")
