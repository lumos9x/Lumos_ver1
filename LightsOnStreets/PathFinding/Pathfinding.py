# Find the safetest path
# 이관대상코드 : 3_find_way_Astar/finding_path_2.ipynb

# ver1 추가분 -> https://www.redblobgames.com/grids/hexagons/#field-of-view redblobgames 이용해서 좌표변환
# -> link 만들 수 있찌 않을까.

import settings, os
import googlemaps
import folium
import pandas as pd
import numpy as np
from haversine import haversine #거리구하기
from sklearn.preprocessing import minmax_scale #정규화



base_dir = settings.BASE_DIR
total_df = pd.read_csv(os.path.join(base_dir,'output', "total_without_road.csv") , encoding = 'ms949')
df = total_df.rename(index=str, columns={"Unnamed: 0" : "ID"})
print(len(df))

l_max = 125
df  = df[df['총밝기'] < l_max]

print("2. ", len(df))

##출발지, 도착지
sp = (37.506059, 127.036863) #출발지 37.506059, 127.036863
ep = (37.509122, 127.043816) #도착지 37.509122, 127.043816


df = df.append(df.from_dict({'ID' : -1,'point_ID':'Point_SP', '위도':sp[0], '경도':sp[1], '밝기':-l_max
                             , '분류':'출발지', '명칭':'출발지', '총밝기' : -l_max }, orient = 'index').T)

df = df.append(df.from_dict({'ID' : len(df), 'point_ID':'Point_EP', '위도':ep[0], '경도':ep[1], '밝기':l_max
                             , '분류':'도착지', '명칭':'도착지', '총밝기' : l_max}, orient = 'index').T)

df = df.sort_values(by='ID').reset_index(drop=True)
print(df.head(5))
# #df['ID'] = df.index.valuesd
# df = df.set_index('ID')