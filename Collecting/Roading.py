import pandas as pd
import settings
import os

class Roading:
    def preprocessing(self, df, category_nm):
        # 공통 전처리 부분 / df 넘기기 전에 df 컬럼 [명칭,주소, 위도, 경도] 로 통일할 것.
        df1 = df.dropna()                               # 1. NaN 값이 하나라도 들어가 있는 행은 그 행 전체를 제거
        df1['분류'] = category_nm                        # 2. 분류 추가하기.
        df2 = df1.drop_duplicates(keep='first')         # 3. 중복되는 행 하나만 남기고 제거하기(부정확한 데이터)
        # ex) [1599 rows x 4 columns] => [1231 rows x 4 columns]

        res = df2.reset_index(drop=True)                # 4. reset index를 통해 index를 0부터 새롭게 지정.
        return res

    def load_Light(self, prvd_code,dong):
        ### 보안등 - 원본 자료 부정확
        ### 정확한 보안등 데이터를 위해서 실제로 돌아보며 정확한 위치 기록하는 수작업 필요함.
        file = os.path.join(settings.BASE_DIR, 'data', '전국보안등정보표준데이터.csv')
        light_df = pd.read_csv(file, encoding='ms949', engine='python')

        # 2-1. 지역필터링 gu > dong
        # prvd_name_df = light_df[light_df.제공기관명.str.contains(gu)] # gu = 강남구
        gu_df = light_df[light_df.제공기관코드 == prvd_code]          # prvd_code = '3220000'
        dong_df = gu_df[gu_df.보안등위치명.str.contains(dong)]        # dong='역삼1동'

        # 2-2. 위도,경도 결측치 확인하고 결측치 제거.
        # print(dong_df.isnull().sum())     # Null 값 20개
        # dong_df[dong_df.위도.isnull()]
        dong_df2 = pd.DataFrame()
        dong_df2['명칭'] = dong_df['보안등위치명']
        dong_df2['주소'] = dong_df['소재지지번주소']
        dong_df2['위도'] = dong_df['위도']
        dong_df2['경도'] = dong_df['경도']
        return self.preprocessing(dong_df2,'보안등')

    def load_CCTV(self, dong):
        file = os.path.join(settings.BASE_DIR, 'data', '서울특별시_강남구_CCTV_20190312.csv')
        gucc_df = pd.read_csv(file, encoding='ms949', engine='python')
        dongcc_df = gucc_df[gucc_df.소재지지번주소.str.contains(dong)]
        dong_df2 = pd.DataFrame()
        dong_df2['명칭'] = dongcc_df['소재지지번주소']
        dong_df2['주소'] = dongcc_df['소재지지번주소']
        dong_df2['위도'] = dongcc_df['위도']
        dong_df2['경도'] = dongcc_df['경도']

        # 명칭은 동부터 기록하기
        address = []
        for name in dong_df2['명칭']:
            nm = name[10:]
            address.append(nm)
        dong_df2['명칭'] = address

        return self.preprocessing(dong_df2,'CCTV')




if __name__ == '__main__':
    rd = Roading()
    print(rd.load_Light('3220000', '역삼1동').head(5)) #code, 동이름
    print(rd.load_CCTV('역삼동').head(5))  # 동이름

