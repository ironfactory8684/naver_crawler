import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import csv
def newscompany_crwal(article, pcompany, pdate, news_office):
  if news_office == "2234":
    return cpbc_news(article, pcompany, pdate)
  elif news_office == "2545":
    return caps_news(article, pcompany, pdate)
  elif news_office == "2458":
    return catholicnews(article, pcompany, pdate)    
  elif news_office == "2252":
    return catholictimes(article, pcompany, pdate)  
  elif news_office == "2149":
    return ibulgyo(article, pcompany, pdate)       

def ibulgyo(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱
    journalist = bsoup.select("#user-container > div.float-center.max-width-960 > header > section > div > ul > li:nth-of-type(1)")[0].text.strip()
    news_detail.append(journalist) 

    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("div.article-head-title")[0].text
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#article-view-content-div")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 

    return news_detail

def catholictimes(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱
    journalist = bsoup.select("p.auth")[0].text.strip().split(" ")[0]
    news_detail.append(journalist) 

    
    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("#atitle")[0].text
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("p.main-story")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 

    return news_detail

def catholicnews(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    journalist = bsoup.select("#article-view > div > header > div > article:nth-of-type(1) > ul > li:nth-of-type(1)")[0].text.strip()
    news_detail.append(journalist)     
    
    
    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("h3.heading")[0].text
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#snsAnchor > div")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 

    return news_detail

def caps_news(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱
    journalist = bsoup.select("#contents > div.basicView > div.registModifyDate > ul > li:nth-of-type(1) > span")[0].text.strip().split(" ")[0]
    news_detail.append(journalist) 
    
    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("#contents > div.basicView > div.titleWrap.boxPointColor > strong")[0].text[2:] 
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#viewContent > div")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 

    return news_detail

def cpbc_news(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    journalist =bsoup.select("#container > div.article_content > div.article_writer > em:nth-of-type(1) > a:nth-of-type(1)")[0].text.strip().split(" ")[0]
    news_detail.append(journalist)   

    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("#article_title")[0].text 
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#articleBody")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 

    return news_detail
