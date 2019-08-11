# the Light(Safety) Map

# input_data : all_df.csv
# | point_ID  | 거리 | 밝기 | 총밝기 | 분류 | 명칭 | 위도 | 경도 | 경유여부 |

# 이관 대상 코드 :
# 3_save_score_on_the_loads_points.ipynb	lumos ver0	3 months ago
# 4_map.ipynb
# ver1 추가분 -> 각 시설물(road 좌표 제외) 표시하는 레이어 추가하기 ( map에서 레이어 개념 )

import os, settings
import numpy as np
import pandas as pd
from haversine import haversine


# 1. 데이터 불러오기
# total_df : 밝기가 있는 주변 시설물
# load_df : 도로 위의 좌표
base_dir = settings.BASE_DIR
total_df = pd.read_csv(os.path.join(base_dir,'data', "total_without_road.csv") , encoding = 'ms949')
total_df.drop('Unnamed: 0', axis=1, inplace=True)

load_df = pd.read_csv(os.path.join(base_dir,'data', "COORDS_IN_역삼동.csv"), encoding = 'ms949')
load_df.drop('Unnamed: 0', axis=1, inplace=True)
load_df.reset_index(inplace =True,drop = True)

print(total_df.head(5))
print(load_df.head(5))



# 2. 시설물마다 점수 주기 -> 함수화 시킬 수 있을 듯.
all_df = pd.DataFrame(columns=['feature_ID', '밝기', '분류', '명칭', '위도', '경도'])

# 밝기 : 설문 조사를 통한 밤길에서 시설물 선호도에 따른 점수
# 설문지 결과 : 파출소 > 보안등 > 편의점 > cctv

for i in range(len(total_df)):
    score = 0
    if total_df['분류'][i] == '파출소':
        score += 25.471
    elif total_df['분류'][i] == '보안등':
        score += 28.397
    elif total_df['분류'][i] == '편의점':
        score += 21.774
    elif total_df['분류'][i] == 'CCTV':
        score += 24.357
    else :
        print("who are you?")

    tmp = {'feature_ID': 'Point_%d' % i, # point numbering
           '밝기': score,
           '분류': total_df.loc[i, '분류'], '명칭': total_df.loc[i, '명칭'],
           '위도': total_df.loc[i, '위도'], '경도': total_df.loc[i, '경도']
           }
    all_df = all_df.append(all_df.from_dict(tmp, orient='index').T)

all_df.reset_index(inplace=True, drop=True)
# all_df   # 1722 rows × 6 columns
all_df.head(50)
print("end-scoring")
print(load_df.head(5))
print("end-scoring")


# 3. 도로 좌표에 밝기 점수 계산하기 ( 교차점 정보에 주변 시설물들의 밝기 점수를 더함)
scores = []
for i in range(len(load_df)) :
    score = 0
    s_point = (load_df.loc[i,'LAT'], load_df.loc[i,'LNG']) # 시작점
    for n in range(len(all_df)) :
        t_point = (all_df.loc[n,'위도'], all_df.loc[n,'경도']) # 타겟
        d_m = haversine(s_point, t_point, unit='m') #  시작점과 타겟의 거리 단위 미터
        # 반경 30M 를 범위로 잡음
        if d_m <= 30 :
            score += all_df.loc[n, '밝기']
    # print(i, score) # 잘나옴
    scores.append(score)

lights = pd.DataFrame()    # load_lux에 적용하는 것들 고대로 load_df에 -> 개념 다시 확인할 것.
lights = load_df.iloc[:,:]
lights['밝기'] = scores

print(lights.head(5))
print(load_df.head(5))
lights.to_csv("3_load_with_light.csv", mode='w', encoding='ms949')


# 4. 포인트(node) 연결하여 링크 만들기.
all_coords = load_df.iloc[:,0:-1]
print(all_coords.head(1))

# 4_1_도로 순서대로 정렬
test = lights.sort_values(by = [ 'RN_CD' , 'RDS_MAN_NO', 'RDS_MAN_NO2' ])
test.reset_index(inplace = True,drop = True)
print(test.head(5))

np.mean( np.array(test.loc[0, '밝기'],   test.loc[1, '밝기'] ) )   # 0.0


# 4_2_링크 정보 만들기 & 평균 밝기 계산
link_df = pd.DataFrame(columns = [ 'LINK_NO','RDS_MAN_NO', 'RN', 'RN_CD', 'SP','EP', 'LUX']  )
n = 0

for i in range(1, len(test)-1):
    # 위아래가 같다는 것은 서로 같은 도로, 이것을 연결해서 Link를 만들 수 있음.
    if test.loc[i, 'RDS_MAN_NO'] == test.loc[i+1, 'RDS_MAN_NO'] :
        tmp = { 'LINK_NO' : 'LINK_%d' % n
              ,'RDS_MAN_NO' : test.loc[i,'RDS_MAN_NO']
              , 'RN' : test.loc[i,'RN']
              , 'RN_CD' : test.loc[i,'RN_CD']
              , 'SP' : [test.loc[i, 'LAT'], test.loc[i, 'LNG']]
              , 'EP' : [test.loc[i+1, 'LAT'],test.loc[i+1, 'LNG']]
               ##두 점의 평균값으로 링크의 밝기를 계산한다.
              , 'LUX' : np.mean( np.array(test.loc[i, '밝기'], test.loc[i+1, '밝기'] ) )
              }

        link_df = link_df.append( link_df.from_dict(tmp, orient = 'index').T)
        n += 1

# 원하는 정보만 가져와서 저장
link_df = link_df.loc[:,['LINK_NO','RDS_MAN_NO', 'RN', 'RN_CD','SP','EP','LUX']].reset_index(drop = True)
link_df.to_csv("links_with_lux.csv", mode='w', encoding='ms949') # edge(=link) list
link_df.head()



# display on Map
import folium

#필요한 열만 가져오기
nodes = test[['RN_CD','RN', 'RDS_MAN_NO','LAT','LNG']]
links = link_df[['SP','EP','LUX']]

std_point = (nodes.loc[0,'LAT'], nodes.loc[0,'LNG'])
map_osm = folium.Map(location=std_point, width='100%', height='100%', zoom_start=17)

for ix, row in links.iterrows():
    start = (row['SP'])  # 위도, 경도 튜플
    end = (row['EP'])
    kw = {'opacity': 1, 'weight': row['LUX'] / 10}

    # print(kw['weight']) #lux 범위가 0~16사이로 나옴.  우선 3등분 함
    if kw['weight'] < 5:
        folium.PolyLine(
            locations=[start, end],
            color='#FF00CC',  # 노락색(yellow)은 잘 안보임, 주황색(orange)도 그닥인듯
            line_cap='round',
            **kw,
        ).add_to(map_osm)
    elif kw['weight'] < 10:
        folium.PolyLine(
            locations=[start, end],
            color='#FF6633',
            line_cap='round',
            **kw,
        ).add_to(map_osm)
    else:
        folium.PolyLine(
            locations=[start, end],
            color='#FF0000',
            line_cap='round',
            **kw,
        ).add_to(map_osm)

# it takes some time.....
map_osm