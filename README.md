# Lumos_ver1

[**목표**](#목표)

  [1.기존 .ipynb로 작성된 코드 .py로 이관하기](#목표1)
  
  [2. 데이터 저장소 및 Spark 이용 속도 개선해보기](#목표2)
  
  [3. 안전지도 앱을 목표로 하는 것을 기반에 두고 Web버전으로 만들기](#목표3)
  
  [4. 기존 역삼 1동 -> 강남 또는 서울로 지역 확장하기](#목표4)
  
[**완료 작업**](#완료-작업)

[**작업 일지**](#작업-일지)


![밝기지도](https://github.com/lumos9x/DEV/blob/master/4_%EC%9D%B4%EA%B4%80%EB%8C%80%EC%83%81%EC%BD%94%EB%93%9C/Lumos_ver0/6_%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3_%EB%B0%9D%EA%B8%B0%EC%A7%80%EB%8F%84zoom.PNG?raw=true)

[그림 1 : Lumos_ver0 : 밝기지도]





## 목표 
<a name="목표1"></a>
### 1.기존 .ipynb로 작성된 코드 .py로 이관하기


<a name="목표2"></a>
### 2. 데이터 저장소 및 Spark 이용 속도 개선해보기

- **슈가맨워크에 있는 동안 해야하니 빠른 진행 필요함!**

- 노트북 2개로 일단 돌려보고 Azure(or AWS)에서 구성하여 돌려보는 것까지

  
<a name="목표3"></a>
### 3. 안전지도 앱을 목표로 하는 것을 기반에 두고 Web버전으로 만들기

- 후에 react native 공부하여 완성하는 것이 목표

  
<a name="목표4"></a>
### 4. 기존 역삼 1동 > 강남 또는 서울로 지역 확장하기.




## 완료 작업  

**[목표 1. 기존 .ipynb로 작성된 코드 .py로 이관하기] - ing** 

1.  Collecting   .py로 변환 & 모듈화 작업 완료
   - [fin_distance_by_giseok.ipynb](https://github.com/lumos9x/DEV/blob/master/4_%EC%9D%B4%EA%B4%80%EB%8C%80%EC%83%81%EC%BD%94%EB%93%9C/fin_distance_by_giseok.ipynb) -> [Collecting](https://github.com/lumos9x/Lumos_ver1/tree/master/Collecting)



[목표 2. 데이터 저장소 및 Spark 이용 속도 개선해보기]

[목표 3. 안전지도 앱을 목표로 하는 것을 기반에 두고 **Web버전으로** 만들기]

[목표 4. 기존 역삼 1동 -> 강남 또는 서울로 지역 확장하기.]




## 작업 일지 

### 2019-08-06

- 편의점 및 경찰서 데이터 크롤링을 유저가 위치 선택할때마다 하기? 저장해놓기?

  - 매번 크롤링하는데 너무 시간이 오래걸림 -> 배치성으로 생각하고 저장해놓자. (일주일?)

  - 후에 [POI]("[https://developers.kakao.com/docs/restapi/local#%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC-%EA%B2%80%EC%83%89](https://developers.kakao.com/docs/restapi/local#카테고리-검색)")이용해서 위치 중심으로 실시간 크롤링을 하는 방안도 연구해보기. 하지만 지금은 저장소에 저장하고 Spark 돌리는게 목표니까 한번에 가져와서 저장해놓자 

    

### 2019-08-07

- **Collecting**

  - Crawling.py

  ```
  * line 23 : while (page <= 21): # 역삼1동의 경우 21 페이지까지(하드코딩) 수정 필요. -수정완료
  * line 97 : 최종 결과를 storage에 연결/저장 코드 추가 필요
  ```

  - ReadingFile.py

    - **원본 데이터의 문제를 명시해 놓은 파일을 따로 관리할 필요성**이 있어보임. 

      -> 보안등 데이터의 문제 정리하기.

    - 제공기관코드 어떻게 가져올 것인가? (원하는 지역 어떻게 추출할 것인가?)



- git에 대용량 데이터 업로드에 문제가 있었던 것 해결

  <https://medium.com/@stargt/github에-100mb-이상의-파일을-올리는-방법-9d9e6e3b94ef>



### 2019-08-08

- **Collecting**  

  -  .py로 변환 & 모듈화 작업 완료.

    - original source :

      - [fin_distance_by_giseok.ipynb](https://github.com/lumos9x/DEV/blob/master/4_이관대상코드/fin_distance_by_giseok.ipynb)

      - [1_크롤링_cv_store_gangnam.ipynb](https://github.com/lumos9x/DEV/blob/master/4_이관대상코드/Lumos_ver0/1_Data 수집 및 가공/1_크롤링_cv_store_gangnam.ipynb)
      - [2_보안등_light_seoul.ipynb](https://github.com/lumos9x/DEV/blob/master/4_이관대상코드/Lumos_ver0/1_Data 수집 및 가공/2_보안등_light_seoul.ipynb)

  

- 밝기 지도 

- AStar

  
