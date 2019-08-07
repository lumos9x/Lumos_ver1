# naver에서 편의점 목록을 크롤링하고, 해당 목록으로 google에서 경위도 좌표를 가져온다.

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

# This version of ChromeDriver supports Chrome version 76
driver = webdriver.Chrome('./chromedriver.exe')

# Get a dataframe of convenience store in the area(dong)
def crawling_naver(dong, facility):

    driver.get('https://map.naver.com/')
    driver.find_element_by_id('search-input').send_keys(dong + " " + facility) # '역삼1동 편의점'
    driver.find_element_by_css_selector('#header > div.sch > fieldset > button').click()

    page = 1
    cs_name = []
    cs_address = []


    while (page <= 21): # 역삼1동의 경우 21 페이지까지(하드코딩) 수정 필요.
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        cs_list = soup.select('.lsnx_det')
        for data in cs_list:
            title = data.select_one('a').text
            cs_name.append(title)
            address = data.find('dd', 'addr').get_text()
            cs_address.append(address[:100])

        # print(page)
        page = page + 1

        try:
            if page % 5 == 1:
                driver.find_element_by_class_name('next').click()
            else:
                driver.find_element_by_xpath('//a[text()=' + str(page) + ']').click()
        except:
            break

        # 로딩 시간 기다려야 데이터 누락이 없음.
        time.sleep(3)


    data = {'csName': cs_name,          # 편의점명
            'csAddress': cs_address}    # 편의점주소
    df = pd.DataFrame(data)
    df2 = df['csAddress'].values.tolist()


    # '서울특별시 강남구 테헤란로 201 아주빌딩 지번' 형태로 출력되어 오른쪽의 지번을 제거해준다.
    df3 = []
    for i in range(0, len(df2)):
        df3.append(df2[i].rstrip(' 지번'))

    # '서울특별시 강남구 논현로95길 29-13 1층 (역삼동 644-3)'와 같은 형태는 '(' 뒤로 모두 삭제
    # -> google맵에서 좌표 찾을때 제대로 찾아지지 않는 문제 해결
    df4 = []
    for i in df3:
        if i.find("(") > 0 :
            df4.append(i[0:i.find("(")])
        else:
            df4.append(i)

    return df4

def crawling_google(df):
# Get a dataframe of convenience store's coordinates.
    import googlemaps
    from settings import Secrets

    secrets = Secrets()
    gmaps_key = secrets.get_secret("GOOGLE_MAP_KEY")
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
    print(crawling_google(crawling_naver("역삼1동", "편의점")))
