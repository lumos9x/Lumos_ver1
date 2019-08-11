import os
import settings
from Collecting.Crawling import MapCrawling   # Crawling을 class로 묶지 않으면 import하는 순간에 크롬이 실행된다.
from Collecting.Loading import LoadingCSV, LoadingSHP
import LightsOnStreets.Map
import LightsOnStreets.PathFinding
import pandas as pd

if __name__ == "__main__":
    print(__name__)
## 1. Collecting
    # 1-1. 크롤링으로 데이터 수집
    mcr = MapCrawling() # 한 화면 당 페이지수
    polices = mcr.crawling("역삼1동", "파출소")
    polices.to_csv("polices.csv", mode='w', encoding='ms949')
    stores = mcr.crawling("역삼1동", "편의점")
    stores.to_csv("stores.csv", mode='w', encoding='ms949')

## 2. 파일 로드해서 데이터 수집
    # 2-1. csv
    ld_csv = LoadingCSV()
    lights = ld_csv.load_light('3220000', '역삼1동')   #code, 동이름
    lights.to_csv("lights.csv", mode='w', encoding='ms949')
    cctvs = ld_csv.load_cctv('역삼동')               # 동이름
    cctvs.to_csv("cctvs.csv", mode='w', encoding='ms949')

#    2-2. shp
    file = os.path.join(settings.BASE_DIR, 'data', '서울특별시_강남구_도로정보', '11680', 'TL_SPRD_MANAGE.shp')
    rd_shp = LoadingSHP()
    road_coords = rd_shp.load_shp_by_region(file, '역삼동')
    print(road_coords.head(30))
    road_coords.to_csv(f"COORDS_IN_역삼동.csv", mode='w', encoding='ms949')  # edge(=link) list

## 3. Total Table 만들기.
#     3-1.total_facilities
    total_without_road = pd.concat([polices,stores,lights,cctvs]).reset_index(drop=True)
    total_without_road.to_csv("total_without_road.csv", mode='w', encoding='ms949')

# # ## 4. 밝기지도 로직
# # ## 5. 길찾기 로직
