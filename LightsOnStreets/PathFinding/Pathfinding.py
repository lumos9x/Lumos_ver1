# Find the safetest path
# 이관대상코드 : 3_find_way_Astar/finding_path_2.ipynb

# ver1 추가분
# -> https://www.redblobgames.com/grids/hexagons/#field-of-view redblobgames 이용해서 좌표변환 -> 길찾기 위한 Node간의 Edge(Link) 만들 수 있찌 않을까.
# -> 1차 속도 개선 위해서 dataframe 말고 기본 자료형 사용하기.

# 함수정리
# get_points_in_range : 중심점에서 범위 내 포함되는 점들 검색
# get_gf : G, H 구하기. return 은 F
# get_scaled_f : F scaling


import folium
import pandas as pd
import numpy as np
import heapq
from haversine import haversine #거리구하기
from sklearn.preprocessing import minmax_scale #정규화

##data 불러오기
total_df = pd.read_csv("all_df.csv", encoding = "EUC-KR" )
df = total_df.rename(index=str, columns={"Unnamed: 0" : "ID"})
df = df.drop(columns = ['경유여부','거리'])
print(len(df))

l_max = 125
df  = df[ df['총밝기'] < l_max]

print(len(df))

##출발지, 도착지
sp = (37.506059, 127.036863) #출발지 37.506059, 127.036863
ep = (37.509122, 127.043816) #도착지 37.509122, 127.043816


df = df.append(df.from_dict({'ID' : -1,'point_ID':'Point_SP', '위도':sp[0], '경도':sp[1], '밝기':-l_max
                             , '분류':'출발지', '명칭':'출발지', '총밝기' : -l_max }, orient = 'index').T)
df = df.append(df.from_dict({'ID' : len(df), 'point_ID':'Point_EP', '위도':ep[0], '경도':ep[1], '밝기':l_max
                             , '분류':'도착지', '명칭':'도착지', '총밝기' : l_max}, orient = 'index').T)
df = df.sort_values(by='ID').reset_index(drop=True)


#총 거리
d_m = haversine(sp, ep, unit='m') # in meters
d_km = haversine(sp, ep,  unit='m')  # in kilometers

#block단위
# 경유지가 총 3개까지만 가능하니까 3개의 반경으로 나누자. 700 이상인 경우는 api다시 받기 (추후에)
dvd = d_m / 4
print( "단위거리(dvd) : ",  dvd, ", 총거리(d_m) : " , d_m)

# 초기화
point = sp
sel_pointID = 'Point_SP'
radius = 100  # 반경
closed_list = []
closed_list_id = []
closed_list_seq = []



# 반경 내 포함 points 검색
def get_points_in_range(df, point):
    rad = radius

    while True:
        res = df[df.apply(lambda x: haversine(point, [x['위도'], x['경도']], unit='m'), axis=1) < rad]
        res = res[~res['point_ID'].isin(closed_list_id)]  # 1-2 . 이미 선택했던 point들 제외
        if (len(res) == 0):
            rad += 10
        else:
            break
    return res


# 가중치 구하기
    # 1. F구하기
def get_f(df):
    g = np.array(df.apply(lambda x: haversine(sp, [x['위도'], x['경도']], unit='m'), axis=1)).reshape(-1, 1)
    h = np.array(df.apply(lambda x: haversine(ep, [x['위도'], x['경도']], unit='m'), axis=1)).reshape(-1, 1)
    return g + h


    # 2. Scaled_F : 밝기 0~100 에 맞추기
def get_scaled_f(df):
    X_MinMax_scaled = 110 - minmax_scale(df['F'], axis=0, copy=True, feature_range=(0, 110))
    return X_MinMax_scaled


    # 3. 밝기 이용한 가중치 추가 W(weight = 4F(거리) + 6L(밝기))
def get_w(df):
    w = np.array(df.apply(lambda x: (x['총밝기'] * 40) + (x['scaled_F'] * 80), axis=1)).reshape(-1, 1)
    return w


# 1. 해당 ID Close List에 추가
n = 0
heapq.heappush(closed_list_id, 'Point_SP')
heapq.heappush(closed_list_seq, n)
heapq.heappush(closed_list, point)

while (sel_pointID != 'Point_EP'):
    # print("시작포인트 : " , point)
    points = pd.DataFrame()
    points = get_points_in_range(df, point)  # 1. 반경 내 속하는 점들 검색
    points['F'] = get_f(points)  # 2. F=G+H : F구하기
    points['scaled_F'] = get_scaled_f(points)  # 3. F를 밝기에 맞춰 스케일링
    points['W'] = get_w(points)  # 4. 최종가중치 구하기

    points = points.sort_values('W', ascending=False).reset_index()  # 5. 정렬

    print(points.loc[0, 'point_ID'])
    sel_pointID = points.loc[0, 'point_ID']
    point = (points.loc[0, '위도'], points.loc[0, '경도'])

    # goodbye.append(points.loc[1:,'point_ID'].values)
    heapq.heappush(closed_list_id, sel_pointID)
    heapq.heappush(closed_list_seq, n)
    heapq.heappush(closed_list, (points.loc[0, '위도'], points.loc[0, '경도']))
    n += 1
# print(sel_pointID)

# 역삼동 중심 = 역삼역 /  좌표 : 37.500742, 127.036891
to_map1 = folium.Map(location= sp, zoom_start=18)
a = closed_list


for n in range(0, len(a)) :
      folium.CircleMarker([a[n][0], a[n][1]], popup= str(closed_list_seq[n]), radius = 3).add_to(to_map1)

# 구분하기 쉽게 스타팅 지역은 빨간색 마커로 표시
folium.Marker(sp, popup= 'SP', icon=folium.Icon(color='red')).add_to(to_map1)
folium.Marker(ep, popup= 'EP', icon=folium.Icon(color='black')).add_to(to_map1)

dd = total_df[ total_df['point_ID'].isin(closed_list_id) ].sort_values('총밝기', ascending = False)