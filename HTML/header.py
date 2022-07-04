# import
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pymongo import MongoClient

# 페이지 추출함수
def pageExtraction(url1):
  webpage = requests.get(url1)
  soup = BeautifulSoup(webpage.content, "html.parser")
  # #논문 제목,링크 추출
  df_data1 = []
  df_name = []
  df_link = []
  df_link1 = []
  division = []
  data1s = soup.select('#main > div > div > div > a > div')
  data2s = soup.select('#main > div > div > div > a > h3 > div')

  for i, data in enumerate(data1s):
    if i%2 == 0:
      st = str(data1s[i]).find('>')
      end = str(data1s[i]).find('</')
      df_link1.append((str(data1s[i])[st+1:end]))

  for i, data in enumerate(data2s):
    st = str(data2s[i]).find('>')
    end = str(data2s[i]).find('</')
    df_name.append((str(data2s[i])[st+1:end-1]))

  #링크에서 외국어처리되는 부분 삭제
  for link in df_link1:
    if link.find('?')!=-1:
      df_link.append(link[:-6])
    else :
      df_link.append(link)

  # #특허번호와 국가코드 추출
  df_patent = []
  df_code = []
  if (df_link[0].find('www.google.com') != -1):
    for link in df_link:
      df_patent.append(link.replace('www.google.com/patents/',''))
      df_code.append(link.replace('www.google.com/patents/','')[0:3])
  elif (df_link[0].find('www.google.co.kr') != -1):
    for link in df_link:
      df_patent.append(link.replace('www.google.co.kr/patents/',''))
      df_code.append(link.replace('www.google.co.kr/patents/','')[0:3])
    #국가코드 3자리인 경우도 포함하기 위하여 3자리에서 숫자아닌경우 slicing
  for i,code in enumerate(df_code):
   if str.isdigit(code[2:3]):
      df_code[i]=(code[0:2])
   else :
      df_code[i]=(code[0:3])

  #for dataframe
  df = pd.DataFrame(index=range(0,len(df_data1)), columns=['특허제목', '링크', '특허번호','국가코드'])
  df['특허제목'] = df_name
  df['링크'] = df_link
  df['특허번호'] = df_patent
  df['국가코드'] = df_code
  return df

# 적용국가 추출함수
def application(url):
  data = requests.get(url)
  soup = BeautifulSoup(data.content, 'html.parser')  
  country = soup.find_all('span', attrs={'itemprop': 'countryCode'})
  Date = soup.find_all('span', attrs={'itemprop': 'filingDate'})
  nation_name = []
  nation_date = []
  # ----------------특허 적용 국가 리스트----------------
  for n in country:
       nation_name.append(n.get_text())
  country_name =  [] 
  for i in nation_name:
     country_name.append(i)
  for n in Date:
     nation_date.append(n.get_text())
  country_date =  [] 
  for i in nation_date:
      country_date.append(i)
  del country_date[0]

  new_contryName = []
  new_contryDate = []
  for i,v in enumerate(country_date):
    new_contryDate.append(v[:4])
  for i in range(len(new_contryDate)):
    new_contryName.append(country_name[-1-i])
  new_contryName.reverse()

  df_application = []
  for i in range(len(new_contryName)):
    df_application.append(new_contryName[i]+'('+new_contryDate[i]+')')

  df_output = []
  df_output.append(' / '.join(df_application))

  inventor = soup.find_all('dd',{'itemprop':'inventor'})
  assigneeCurrent = soup.find_all('dd',{'itemprop':'assigneeCurrent'})  
  patent_inventor = []
  patent_assignee = []

  for n in inventor:
      patent_inventor.append(n.get_text())

  df_patent_inventor = []
  for i in range(len(patent_inventor)):
    if i == 0:
      df_patent_inventor.append(patent_inventor[i])
    else :
      df_patent_inventor.append(' / '+patent_inventor[i])
  df_patent_inventor= "".join(df_patent_inventor)

  for n in assigneeCurrent:
      patent_assignee.append(n.get_text())
  df_patent_assignee = []
  for i in range(len(patent_assignee)):
    if i ==0:
      df_patent_assignee.append(patent_assignee[i])
    else :
      df_patent_assignee.append(' / '+patent_assignee[i])

  Str_assignee = "".join(df_patent_assignee)
  Str_assignee = Str_assignee.replace("\n","")
  Str_assignee = Str_assignee.lstrip()
  new_list_assignee = Str_assignee.split("   ")
  new_list_assignee= "".join(new_list_assignee)

  df1 = pd.DataFrame(index=range(0,1), columns=['적용국가','Inventor','assignee'])
  df1['적용국가'] = df_output
  df1['Inventor'] = df_patent_inventor
  df1['assignee'] = new_list_assignee
  return df1

def search(keywords, N):
  keywords.replace(' ','+')
  keyword = keywords.split(',')
  baseUr1 = 'https://www.google.com/search?q='

  #데이터 프레임 concat 기능
  whole_df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
  plusUr1 = ''
  ur1 = ''
  for i in range(int(N/10)):
    for key in keyword:
      if(key != 'end'):
        plusUr1 = plusUr1 + '%22' + key +'%22+'
      else:
        plusUr1 = plusUr1[:-1]
    ur1 = baseUr1 + plusUr1 + '&tbm=pts&start=' + str(i*10)
    plusUr1 = ''
    df = pageExtraction(ur1)
    whole_df = pd.concat([whole_df,df], ignore_index=True)
  return keywords, whole_df

def search_advanced(df):
  df_app = []
  df2 = pd.DataFrame(columns=['적용국가','Inventor','assignee'])
  for link in df['링크']:
    df1 = application('http://'+link)
    df2 = pd.concat([df2, df1], ignore_index=True)

  df_out = pd.concat([df,df2],axis=1)
  return df_out

def field_search(df):
  index = df.columns.tolist()
  print('검색가능한 field들 :',index)
  index.append('end')

  df_output = df
  field = input('검색할 field를 입력하세요(끝내고싶으면 end 입력) : ')
  while(field != 'end'):
      while (field not in index):
        field = input('검색할 field를 다시 입력하세요(끝내고싶으면 end 입력) : ')
      key = input('검색할 키워드를 입력하세요 : ')
      df_output = df[df[field].str.contains(key)]
      df = df_output
      field = input('검색할 field를 입력하세요(끝내고싶으면 end 입력) : ')
    
  return df_output

def paper_citation(df):
  keyword = []
  keyword.append(input('특허번호 입력 :')) 
  str_keyword ="".join(keyword)
  keyowrd_url = 'https://patents.google.com/patent/'+ str_keyword

  data = requests.get(keyowrd_url)
  soup = BeautifulSoup(data.content, 'html.parser')
  country = soup.find_all('tr',{'itemprop':'backwardReferences'})
  information = []
  non_patent_citation = soup.find_all('tr',{'itemprop':'detailedNonPatentLiterature'}) 
  NPC = []

  for n in non_patent_citation:
       NPC.append(n.get_text())
  
  non_patent = "".join(NPC)
  non_patent = non_patent.replace("\n","")
  new_non_patent = non_patent.split("*")
  del new_non_patent[len(new_non_patent)-1]

  for n in country:
    information.append(n.get_text())

  indexlist = []
  for i,data in enumerate(information):
    index = 0
    while index > -1:
      index = data.find('\n',index)
      if index > -1:
        indexlist.append(index)
        index += len('\n')

  publication_number = []
  priority_date = []
  publication_date = []
  assignee = []
  title = []
  line = ''
  count = 0

  for i,index in enumerate(indexlist):
    if index == 0:
      line = information[count]
      publication_number.append(line[indexlist[i+2]+1:indexlist[i+3]])
      if line.find('*')==-1:
        priority_date.append(line[indexlist[i+6]+1:indexlist[i+7]])
        publication_date.append(line[indexlist[i+7]+1:indexlist[i+8]])
        assignee.append(line[indexlist[i+8]+1:indexlist[i+9]])
        title.append(line[indexlist[i+9]+1:indexlist[i+10]])
      else :
        priority_date.append(line[indexlist[i+7]+1:indexlist[i+8]])
        publication_date.append(line[indexlist[i+8]+1:indexlist[i+9]])
        assignee.append(line[indexlist[i+9]+1:indexlist[i+10]])
        title.append(line[indexlist[i+10]+1:indexlist[i+11]])
      count = count + 1
    


  df2 = pd.DataFrame(index=range(0,len(publication_number)), columns=['Publication number', 'Priority date', 'Publication date','Assignee','Title'])
  df2['Publication number'] = publication_number
  df2['Priority date'] = priority_date
  df2['Publication date'] = publication_date
  df2['Assignee'] = assignee
  df2['Title'] = title

  df3 = pd.DataFrame(index=range(0,len(new_non_patent)), columns=['Non-Patent Citations title'])
  df3['Non-Patent Citations title'] = new_non_patent
  return df2, df3


def Data_File(keyword,df):
  file_name = ''
  for i in range(len(keyword)):
    file_name = file_name + keyword[i] + ' '
  file_name = file_name+'.xlsx'
  excel_name = ''
  excel_name = file_name.replace('end','')
    # print(excel_name)
  df.to_excel(excel_name,index =False)
  
  
def Search_patent_news():
  #검색할 키워드 입력
  query = input('검색할 키워드를 입력하세요: ')


  #크롬드라이버로 원하는 url로 접속
  url = 'https://www.patentlyapple.com/patently-apple/'
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
  driver.get(url)
  time.sleep(3)

  #검색창에 키워드 입력 후 엔터

  search_box = driver.find_element_by_css_selector("#search-blog > div > input")
  search_box.send_keys(query)
  search_box.send_keys(Keys.RETURN)
  time.sleep(3)

  Apple_Patent_news = []
  Apple_Patent_link = []
  for k in range(0,100):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    Patent__apple_title = soup.find_all('h3', attrs={'class': 'entry-header font-entryheader'})
    for i in Patent__apple_title:
      Apple_Patent_news.append(i.get_text())

    Patent__apple_link = soup.select('h3 > a')
    for i in Patent__apple_link:
        Apple_Patent_link.append(i.attrs['href'])

    try:
      if(k==0):
        driver.find_element_by_xpath('//*[@id="post-container"]/div/div[1]/div[1]/div/div/div[3]/div[11]/div/span').click()
      if(k > 0):
        driver.find_element_by_xpath('//*[@id="post-container"]/div/div[1]/div[1]/div/div/div[3]/div[11]/div/span[3]/a').click()
    except NoSuchElementException :
      print("Maximum page is ", k+1)
      break
  time.sleep(2)
  driver.close()

  df = pd.DataFrame(index=range(0,len(Apple_Patent_news)), columns=['News_Title','News_Link'])
  df['News_Title'] = Apple_Patent_news
  df['News_Link'] = Apple_Patent_link

  return df

def search_details(wholeurl):
  driver = webdriver.Chrome('./chromedriver')
  patent_name = []
  inventor = []
  assignee = []
  summary = []

  # 첫 페이지에 접속
  tempurl = wholeurl.replace('&page=*','')
  driver.get(tempurl)
  time.sleep(1)

  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')
  notices = soup.select('#htmlContent')
  try:
    count = soup.select_one('#count > div.layout.horizontal.style-scope.search-results > span.flex.style-scope.search-results > span:nth-child(3)').text
  except:
    count = 300
  count = count.replace(',','')

  # 논문제목, inventor, assignee추출
  for i, n in enumerate(notices):
      if i%4 == 0:
          patent_name.append(n.text.strip())
      elif i%4 == 1:
          inventor.append(n.text.strip())
      elif i%4 == 2:
          assignee.append(n.text.strip())
      else :
          summary.append(n.text.strip())
  # 적용국가, 특허코드 추출
  object = soup.select('#resultsContainer > section > search-result-item > article > div > div > div > div.flex.style-scope.search-result-item > h4.metadata.style-scope.search-result-item > span')
  ob = []
  for o in object:
      ob.append(o.text)  
  applied_country = ''
  country = []
  patent_code = []
  for o in ob:
      count1 = o.count('\n')
      if count1 == 0:
          applied_country = applied_country + o + ', '
      if count1 == 4:
          applied_country = applied_country[:-2]
          country.append(applied_country)
          applied_country = ''
          patent_code.append(o.replace('\n',''))

  # 검색결과가 1000개이상 나오지않아서 오래걸리는 것을 방지
  page = int(count)/10
  if page > 99:
      page = 99

  # 첫 페이지에서 확인한 정보로 나머지 페이지 확인
  for i in range(1,int(page)+1):
      tempurl = wholeurl.replace('&page=*','&page=')+str(i)
      driver.get(tempurl)
      time.sleep(1)
      
      html = driver.page_source
      soup = BeautifulSoup(html, 'html.parser')
      notices = soup.select('#htmlContent')   
      
      object = soup.select('#resultsContainer > section > search-result-item > article > div > div > div > div.flex.style-scope.search-result-item > h4.metadata.style-scope.search-result-item > span')
      ob = []
      for o in object:
          ob.append(o.text)  

      applied_country = ''
      for o in ob:
          count = o.count('\n')
          if count == 0:
              applied_country = applied_country + o + ', '
          if count == 4:
              applied_country = applied_country[:-2]
              country.append(applied_country)
              applied_country = ''
              patent_code.append(o.replace('\n',''))

      for i, n in enumerate(notices):
          if i%4 == 0:
              patent_name.append(n.text.strip())
          elif i%4 == 1:
              inventor.append(n.text.strip())
          elif i%4 == 2:
              assignee.append(n.text.strip())
          else :
              summary.append(n.text.strip())

  driver.close()
  return patent_name, patent_code, inventor, assignee ,country

# 데이터 프레임 생성
def search_details_df(patent_name, patent_code, inventor, assignee ,country):
    output = pd.DataFrame({'특허제목':patent_name, '특허코드':patent_code, 'inventor':inventor, 'assignee':assignee, '적용국가':country})
    return output

# google patent 링크 생성함수 (en:english, kr:korean) 제목또한 해당 언어로 return
def google_link(list,language):
    base_link = 'https://patents.google.com/patent/'
    output_link = []
    for l in list:
        output_link.append(base_link+l+'/'+language)
    
    return output_link

def whole_name(link):
    whole_names = []
    for l in link:
        data = requests.get(l)
        soup = BeautifulSoup(data.content, 'html.parser')
        title = soup.select_one('body > search-app > article > h1').text
        
        st = title.find(' - ')
        end = title.rfind(' - ')
        whole_names.append(title[st+3:end-9])

    return whole_names

def change_ptname(df):
    google_links = google_link(df['특허코드'],'en')
    whole_names = whole_name(google_links)
    
    df['특허제목'] = whole_names
    return df

def Search_patent_news():
  #검색할 키워드 입력
  query = input('검색할 키워드를 입력하세요: ')


  #크롬드라이버로 원하는 url로 접속
  driver = webdriver.Chrome('./chromedriver')
  url = 'https://www.patentlyapple.com/patently-apple/'
  driver.get(url)
  time.sleep(2)

  #검색창에 키워드 입력 후 엔터

  search_box = driver.find_element_by_css_selector("#search-blog > div > input")
  search_box.send_keys(query)
  search_box.send_keys(Keys.RETURN)
  time.sleep(2)

  Apple_Patent_news = []
  Apple_Patent_link = []
  for k in range(0,100):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    Patent__apple_title = soup.find_all('h3', attrs={'class': 'entry-header font-entryheader'})
    for i in Patent__apple_title:
      Apple_Patent_news.append(i.get_text())

    Patent__apple_link = soup.select('h3 > a')
    for i in Patent__apple_link:
        Apple_Patent_link.append(i.attrs['href'])

    try:
      if(k==0):
        driver.find_element_by_xpath('//*[@id="post-container"]/div/div[1]/div[1]/div/div/div[3]/div[11]/div/span').click()
      if(k > 0):
        driver.find_element_by_xpath('//*[@id="post-container"]/div/div[1]/div[1]/div/div/div[3]/div[11]/div/span[3]/a').click()
    except NoSuchElementException :
      print("Maximum page is ", k+1)
      break
  driver.close()

  df = pd.DataFrame(index=range(0,len(Apple_Patent_news)), columns=['News_Title','News_Link'])
  df['News_Title'] = Apple_Patent_news
  df['News_Link'] = Apple_Patent_link

  return df

def detail_search(keyword, inventor, assignee, country):
    baseurl = 'https://patents.google.com/?q='
    # wholeurl = baseurl + keyword + '&inventor=' + inventor + '&assignee=' + assignee + '&country=' + country + '&page=*'
    wholeurl = baseurl + keyword + '&inventor=' + inventor + '&assignee=' + assignee + '&page=*'
    
    patent_name, patent_code, inventor, assignee ,country = search_details(wholeurl)
    output = search_details_df(patent_name, patent_code, inventor, assignee ,country)
    output2 = change_ptname(output)
    
    return output2
  
# 제목과 링크 추출
def extractlink(url):
  # url = 'https://www.patentlyapple.com/patently-apple/autonomous-vehicle-technology/'
  driver = webdriver.Chrome('./chromedriver')
  driver.get(url)
  time.sleep(3)

  Apple_Patent_news = []
  Apple_Patent_link = []
  title_index=0
  for k in range(0,10):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    Patent__apple_title = soup.find_all('h2', attrs={'class': 'entry-header font-entryheader'})

    for i in Patent__apple_title:
      Apple_Patent_news.append(i.get_text()[2:-2])
    Patent__apple_link = soup.select('h2 > span > a')
    for i in Patent__apple_link:
        Apple_Patent_link.append(i.attrs['href'])

    try:
      if(len(Apple_Patent_link)==25*(k+1)):
        # page_str = 'https://www.patentlyapple.com/patently-apple/autonomous-vehicle-technology/' + 'page/'+ str(k+1) + '/'
        page_str = url + 'page/'+ str(k+1) + '/'
        driver.get(page_str)
      if(len(Apple_Patent_link)<25*(k+1)):
        raise Exception
    except Exception:
      print("Maximum page is ", k)
      break
  time.sleep(2)
  driver.close()

  df1 = pd.DataFrame(index=range(0,len(Apple_Patent_news)), columns=['News_Title','News_Link'])
  df1['News_Title'] = Apple_Patent_news
  df1['News_Link'] = Apple_Patent_link
  return df1

# 첫번째필터
def filter1(df):
    driver = webdriver.Chrome('./chromedriver')
    patents_list = []
    link_list = []
    for i in df.index:
        # 웹페이지 가져오기
        link = df['News_Link'][i]
        driver.get(link)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        contents = soup.select('#post-container > div.container > div.row.pagebody > div.col-sm-8.col-sm-push-4.col-md-6.col-md-push-3 > div > div > article > div.entry-more.font-entrybody > p')
        contents_list = []
        befor_list = patents_list[:]
        patents_list_un = []
        for c in contents:
            contents_list.append(c.text)
        # html의 한 구조체마다 반복문
        for j, con in enumerate(contents_list):
            # 첫번째 필터를 통해 데이터 추출
            c = ','
            lst = []
            # 구조체에서의 ,위치 return
            for pos,char in enumerate(con):
                if(char == c):
                    lst.append(pos)
            for i, l in enumerate(lst):
                before = 0
                now = l
                if i!=0:
                    before = lst[i-1]
                if (now - before) == 4:
                    patents_list_un.append(contents_list[j][before-3:now+4])
            
            # 두번째 필터를 통해 데이터 추출
            pos1 = con.find('20210')
            if pos1 != -1:
                patents_list.append(con[pos1:pos1+11])
            pos2 = con.find('20200')
            if pos2 != -1:
                patents_list.append(con[pos2:pos2+11])
            pos3 = con.find('20190')
            if pos3 != -1:
                patents_list.append(con[pos3:pos3+11])
            pos4 = con.find('20180')
            if pos4 != -1:
                patents_list.append(con[pos4:pos4+11])
      
        
        for code in patents_list_un:
            try:
                if ((code[0]==' ')&code[1:3].isdigit()&code[4:7].isdigit()&code[8:11].isdigit()):
                    # print(code[1:])
                    patents_list.append(code[1:].replace(',',''))
                # print(patents_list)
            except IndexError:
                a=0
        
        # 세번째 필터를 통해 데이터 추출
        Patent_title_number= soup.select('div > p > a')
        Patent_title_here = soup.select('div > p > span > a')
        
        for k in Patent_title_number:
            if k.attrs['href'].find('uspto') != -1:
                if k.find('patentnumber') != -1:
                    patents_list.append(k.attrs['href'].replace(',','')[-8:])
                else: 
                    patents_list.append(k.attrs['href'].replace(',','')[-11:])
        for k in Patent_title_here:
            if k.attrs['href'].find('uspto') != -1:
                if k.find('patentnumber') != -1:
                    patents_list.append(k.attrs['href'].replace(',','')[-8:])
                else: 
                    patents_list.append(k.attrs['href'].replace(',','')[-11:])
        
        if (len(befor_list) == len(patents_list)):
            link_list.append(link)
            # print(link)

    return patents_list

def applelink(codes):
    links = []
    for code in codes:
        links.append('https://patents.google.com/patent/US'+code)
    return links

def application2(url):
  data = requests.get(url)
  soup = BeautifulSoup(data.content, 'html.parser')
  country = soup.find_all('span', attrs={'itemprop': 'countryCode'})
  Date = soup.find_all('span', attrs={'itemprop': 'filingDate'})
  nation_name = []
  nation_date = []
  # ----------------특허 적용 국가 리스트----------------  
  for n in country:
    try:
      nation_name.append(n.get_text())
    except:
      nation_name.append('')
  country_name =  [] 
  for i in nation_name:
    try:
      country_name.append(i)
    except:
      country_name.append('')
  for n in Date:
    try:
      nation_date.append(n.get_text())
    except:
      nation_date.append('')
  country_date =  [] 
  for i in nation_date:
      country_date.append(i)
  
  new_contryName = []
  new_contryDate = []
  for i,v in enumerate(country_date):
    new_contryDate.append(v[:4])
  for i in range(len(new_contryDate)):
    try:
      new_contryName.append(country_name[-1-i])
    except:
      new_contryName.append('')
  new_contryName.reverse()

  df_application = []
  for i in range(len(new_contryName)):
    df_application.append(new_contryName[i]+'('+new_contryDate[i]+')')

  df_output = []
  df_output.append(' / '.join(df_application))

  inventor = soup.find_all('dd',{'itemprop':'inventor'})
  assigneeCurrent = soup.find_all('dd',{'itemprop':'assigneeCurrent'})  
  patent_inventor = []
  patent_assignee = []

  for n in inventor:
      patent_inventor.append(n.get_text())

  df_patent_inventor = []
  for i in range(len(patent_inventor)):
    if i == 0:
      df_patent_inventor.append(patent_inventor[i])
    else :
      df_patent_inventor.append(' / '+patent_inventor[i])
  df_patent_inventor= "".join(df_patent_inventor)

  for n in assigneeCurrent:
      patent_assignee.append(n.get_text())
  df_patent_assignee = []
  for i in range(len(patent_assignee)):
    if i ==0:
      df_patent_assignee.append(patent_assignee[i])
    else :
      df_patent_assignee.append(' / '+patent_assignee[i])

  Str_assignee = "".join(df_patent_assignee)
  Str_assignee = Str_assignee.replace("\n","")
  Str_assignee = Str_assignee.lstrip()
  new_list_assignee = Str_assignee.split("   ")
  new_list_assignee= "".join(new_list_assignee)
  try:
    title = soup.select_one('body > search-app > article > h1').text
    st = title.find(' - ')
    end = title.rfind(' - ')
    df1 = pd.DataFrame(index=range(0,1), columns=['특허제목','특허코드','적용국가','Inventor','assignee'])
    df1['특허제목'] = title[st+3:end-9]
    df1['특허코드'] = title[:st]
    df1['적용국가'] = df_output
    df1['Inventor'] = df_patent_inventor
    df1['assignee'] = new_list_assignee
  except AttributeError:
    df1 = pd.DataFrame(index=range(0,1), columns=['특허제목','특허코드','적용국가','Inventor','assignee'])
    df1['특허제목'] = 'Withdrawn'
    df1['특허코드'] = url[-10:]
    df1['적용국가'] = '-'
    df1['Inventor'] = '-'
    df1['assignee'] = '-'
  return df1

def search_from_googlelinks(links):
    df2 = pd.DataFrame(columns=['특허제목','특허코드','적용국가','Inventor','assignee'])
    for link in links:
        df1 = application2(link)
        df2 = pd.concat([df2, df1], ignore_index=True)

    return df2
  
def Search_patent_news():
  #검색할 키워드 입력
  query = input('검색할 키워드를 입력하세요: ')


  #크롬드라이버로 원하는 url로 접속
  driver = webdriver.Chrome('./chromedriver')
  url = 'https://www.patentlyapple.com/patently-apple/'
  driver.get(url)
  time.sleep(2)

  #검색창에 키워드 입력 후 엔터

  search_box = driver.find_element_by_css_selector("#search-blog > div > input")
  search_box.send_keys(query)
  search_box.send_keys(Keys.RETURN)
  time.sleep(2)

  Apple_Patent_news = []
  Apple_Patent_link = []
  for k in range(0,100):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    Patent__apple_title = soup.find_all('h3', attrs={'class': 'entry-header font-entryheader'})
    for i in Patent__apple_title:
      Apple_Patent_news.append(i.get_text())

    Patent__apple_link = soup.select('h3 > a')
    for i in Patent__apple_link:
        Apple_Patent_link.append(i.attrs['href'])

    try:
      if(k==0):
        driver.find_element_by_xpath('//*[@id="post-container"]/div/div[1]/div[1]/div/div/div[3]/div[11]/div/span').click()
      if(k > 0):
        driver.find_element_by_xpath('//*[@id="post-container"]/div/div[1]/div[1]/div/div/div[3]/div[11]/div/span[3]/a').click()
    except NoSuchElementException :
      print("Maximum page is ", k+1)
      break
  driver.close()

  df = pd.DataFrame(index=range(0,len(Apple_Patent_news)), columns=['News_Title','News_Link'])
  df['News_Title'] = Apple_Patent_news
  df['News_Link'] = Apple_Patent_link

  return df

def applepatent(url):
    # 제목과 링크 추출
    dflink = extractlink(url)
    
    # 필터들을 통해 얻어낸 코드리스트와 걸러지지않은 링크들
    list2 = filter1(dflink)
    
    # 코드 링크로의 구글 링크로의 변환
    links = applelink(list(set(list2)))
    
    # 구글에서 검색을 통한 데이터프레임생성
    df_output = search_from_googlelinks(links)
    
    return df_output
  
def applepatent_keyword():
    # 제목과 링크 추출
    dflink = Search_patent_news()
    
    # 필터들을 통해 얻어낸 코드리스트와 걸러지지않은 링크들
    list2 = filter1(dflink)
    
    # 코드 링크로의 구글 링크로의 변환
    links = applelink(list(set(list2)))
    
    # 구글에서 검색을 통한 데이터프레임생성
    df_output = search_from_googlelinks(links)
    
    return df_output

def df_to_db(keyword, df, client):
    items = df.to_dict("records")
    mydb = client['data']
    mycol = mydb[keyword]
    
    mycol.insert_many(items)