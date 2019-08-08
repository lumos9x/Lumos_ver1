# naver에서 편의점 목록을 크롤링하고, 해당 목록으로 google에서 경위도 좌표를 가져온다.
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# 재사용성 생각해서 다시 로직 짜보기
class MapCrawling:
    # This version of ChromeDriver supports Chrome version 76
    # Get a dataframe of convenience store in the area(dong)
    def crawling_naver(self, dong, facility, num = 5):
        driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
        driver = webdriver.Chrome(driver_path)

        numPages = num # 세트 하나당 page수
        def preprocessing(cs_name, cs_address):
            data = {'csName': cs_name,  # 편의점명
                    'csAddress': cs_address}  # 편의점주소

            df = pd.DataFrame(data)
            df2 = df['csAddress'].values.tolist()

            # '서울특별시 강남구 테헤란로 201 아주빌딩 지번' 형태로 출력되어 오른쪽의 지번을 제거해준다.
            df3 = []
            for i in range(0, len(df2)):
                df3.append(df2[i].rstrip(' 지번'))

            # '서울특별시 강남구 논현로95길 29-13 1층 (역삼동 644-3)'와 같은 형태는 '(' 뒤로 모두 삭제해야 google맵에서 좌표 찾을때 제대로 찾음.
            df4 = []
            for i in df3:
                if i.find("(") > 0:
                    df4.append(i[0:i.find("(")])
                else:
                    df4.append(i)

            return df4

        driver.get('https://map.naver.com/')
        driver.find_element_by_id('search-input').send_keys(dong + " " + facility) # '역삼1동 편의점'
        driver.find_element_by_css_selector('#header > div.sch > fieldset > button').click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        page, cs_name, cs_address  = 1, [], []

        while(True):
            # 1. 현재 페이지의 모든 주소 가져오기
            cs_list = soup.select('.lsnx_det')
            for data in cs_list:
                title = data.select_one('a').text
                cs_name.append(title)
                address = data.find('dd', 'addr').get_text()
                cs_address.append(address[:100])

            # 2. 페이지 넘기기
            # print(page)
            page = page + 1
            page_mod = page % numPages

            if page_mod == 1: #다음 페이지가 새로운 묶음이면
                try:
                    driver.find_element_by_class_name('next').click()
                except:
                    break
            else:
                # css selector에서 페이지 클릭을 위한 nth-child는 2,3,4,5,6 이다. 따라서 다음에 클릭할 페이지가 묶음의 마지막이라면 0+1 = 1이 아닌 6이되어야한다.
                num=numPages+1 if page_mod==0 else page_mod + 1
                try :
                    driver.find_element_by_css_selector(f'div.search_result > div > div > a:nth-child({str(num)})').click()
                except:
                    break
            time.sleep(1.5) # 로딩 시간 기다려야 데이터 누락이 없음.

        driver.close() # 드라이버 닫아주기

        # 데이터 전처리
        res_df = preprocessing(cs_name, cs_address)
        return res_df


    def crawling_google(self, df):
    # Get a dataframe of convenience store's coordinates.
        import googlemaps
        import settings

        gmaps_key = settings.get_secret("GOOGLE_MAP_KEY")
        gmaps = googlemaps.Client(key = gmaps_key)

        cs_lat = []
        cs_lng = []

        for i in range(0,len(df)):
        # 위의 코드에서 'geometry'가 가지고 데이터('location'의 'lat', 'lng')를 모두 가져옴
            e = gmaps.geocode(df[i], language = 'ko')[0].get('geometry')
            cs_lat.append(e['location']['lat'])
        # tmp_loc에 있는 'location'에서 'lng' 경도 데이터를 가져옴
            cs_lng.append(e['location']['lng'])


        cs_df = pd.DataFrame(df)
        cs_df['lat'] = cs_lat
        cs_df['lng'] = cs_lng

        return cs_df


## 저장소에 연결/저장 코드 추가 필요

if __name__ == '__main__':
    cr = MapCrawling()
    print(cr.crawling_google(cr.crawling_naver("역삼1동", "편의점")))

# div.search_result > div > div > span
#  div.search_result > div > div > a.next