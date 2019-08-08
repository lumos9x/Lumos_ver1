from Collecting.Crawling import MapCrawling   # Crawling을 class로 묶지 않으면 import하는 순간에 크롬이 실행된다.
from Collecting.Roading import Roading

import settings

if __name__ == "__main__":

    # 1. Collecting
        # 1-1. 크롤링으로 데이터 수집
    mcr = MapCrawling() # 한 화면 당 페이지수
    polices = mcr.crawling_google(mcr.crawling_naver("역삼1동", "파출소"))
    # polices.to_csv("polices.csv", mode='w', encoding='ms949')
    stores = mcr.crawling_google(mcr.crawling_naver("역삼1동", "편의점"))
    # stores.to_csv("stores.csv", mode='w', encoding='ms949')


    # 2. 파일 로드해서 데이터 수집
    rd = Roading()
    lights = rd.load_Light('3220000', '역삼1동')   #code, 동이름
    # lights.to_csv("lights.csv", mode='w', encoding='ms949')
    cctv = rd.load_CCTV('역삼동')               # 동이름
    # cctv.to_csv("cctv.csv", mode='w', encoding='ms949')
    #
    # print(stores.head(5))
    # print(polices.head(5))
    # print(lights.head(5))
    # print(cctv.head(5))








