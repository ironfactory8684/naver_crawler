import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import date, timedelta,datetime

def get_news(article): 
    news_detail = [] 
    #print(article) 
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


def crawler(query, s_date, e_date, news_office, maxpage, sort, printed):
#     news_compnay = {"1032": "경향신문", "1005": "국민일보", "2312": "내일신문",
#                     "1020": "동아일보", "2385":"매일일보", "1021": "문화일보",
#                     "1081": "서울신문", "1022": "세계일보", "2268": "아시아투데이",
#                     "2844": "전국매일신문", "1023": "조선일보", "1025": "중앙일보",
#                     "2041": "천지일보", "1028": "한겨레", "1469": "한국일보"}
#     if news_office:
#         news_office = news_compnay[news_office]
       
    
    f = open("./" + query+news_office  + '.csv', 'a', encoding='utf-8', newline='')
    wr=csv.writer(f)
    wr.writerow(["기사_아이디","날짜","신문사","제목","내용","댓글갯수","댓글내용"])
    
    page = 1
    maxpage_t =(int(maxpage)-1)*10+1 # 11= 2페이지 21=3페이지 31=4페이지 ...81=9페이지 , 91=10페이지, 101=11페이지
    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    
#     if maxpage=="400":
#         url = "https://search.naver.com/search.naver?where=news&query=" + \
#             query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + \
#             "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(maxpage_t)
#         header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
#             }
#         req = requests.get(url,headers=header)
#         cont = req.content
#         soup = BeautifulSoup(cont, 'html.parser')
#         check = soup.select_one("#main_pack > div.api_noresult_wrap > div.not_found02")
#         if not check:
#             print("검색결과가 4000개를 넘습니다. 기간을 짧게 설정하세요")
#             main()
              
    
    while page <=maxpage_t:    
        #print(page)
        if news_office:
            url = "https://search.naver.com/search.naver?where=news&query=" + \
            query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + \
            "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + \
            str(page) + "&office_section_code=1&news_office_checked="+news_office
        else:
            url = "https://search.naver.com/search.naver?where=news&query=" + \
            query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + \
            "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        if printed =="1":
            print(url)
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
                    if printed=="1":
                        print("네이버 뉴스",page,"-", i,":")
                        print(article)
                
                    AD = article.split("aid=")[1]  # 기사의 고유 아이디값
                
                    news_detail = get_news(article)  # 기사의 고유 아이디 값 컬럼 추가
                    # title, content

                    CA=comments(article)

                    CA= [AD]+news_detail+CA   #가독성을 위해..
            
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

def main_crawler(query,s_date, e_date, news_office, maxpage, sort, printed):
    print(s_date, e_date)
    y,m,d = s_date.split(".")
    ey,em,ed = e_date.split(".")
    first_date = "%s.%s.%s"%(y,m,d)
    today = datetime(int(y),int(m),int(d))
    endday = datetime(int(ey),int(em),int(ed))

    while today <endday:
        print(first_date)
        crawler(query, first_date, first_date, news_office, maxpage, sort, printed)
        y,m,d = first_date.split(".")
        today = datetime(int(y),int(m),int(d))
        next_day = today + timedelta(days=1)
        ny, nm, nd = next_day.year,next_day.month,next_day.day
        first_date = "%s.%02d.%02d"%(ny,int(nm),int(nd))    
    
def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    maxpage = input("최대 크롤링할 페이지 수 입력\n"+"="*20+"\n"+"최대 400페이지까지 가능합니다\n"+"만약 검색결과가 4000개를 넘으면 다시 실행됩니다\n"+"페이지수를 입력해주세요 :")
    query = input("검색어 입력: ")
    sort = input("뉴스 검색 방식 입력(관련도순=0 최신순=1 오래된순=2): ") #관련도순=0 최신순=1 오래된순=2
    s_date = input("시작날짜 입력(2019.01.04):") #2019.01.04
    e_date = input("끝날짜 입력(2019.01.05):") #2019.01.05
    news_office = input("""특정 신문사를 원할경우 숫자를 입력해주세요\n 
만약 원하지 않는다면 Enter를 눌러주세요\n
1032: 경향신문, 1005: 국민일보, 2312: 내일신문\n
1020: 동아일보, 2385:매일일보, 1021: 문화일보\n
1081: 서울신문, 1022: 세계일보, 2268: 아시아투데이
2844: 전국매일신문, 1023: 조선일보, 1025: 중앙일보 \n
2041: 천지일보, 1028: 한겨레, 1469: 한국일보 \n
신문사 숫자를 입력해주세요 원하시지 않으면 enter를 입력해주세요:""") 
    printed = input("진행되는 결과물 출력(출력=1 비출력=0): ")
    main_crawler(query, s_date, e_date, news_office, maxpage, sort,printed)

if __name__ == '__main__':
    main()
