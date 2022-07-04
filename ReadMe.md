# SV winter internship

## Acquisition of patent information through crawling

### 1. Introduction

이 repository는 2021년도 겨울방학에 진행된 인턴쉽에 관한 내용을 포함하고 있습니다. 해당 내용은 한동대학교 소속의 17학번 이준기와 송영원이 함께 진행한 내용입니다.



### 2. Purpose

 현재 기업에서는 자율주행에 관한 특허를 꾸준히 출원하고 있다. 특허 출원을 위하여 사용되는 특허 검색 프로그램은 많은 이용료를 필요로 한다고 한다. 하지만 비싼 이용료에도 불구하고, 사용환경이 불편하며, 필요한 정보들을 얻어내지 못한다고 한다. 그렇기에 본 프로젝트에서는 정적크롤링과 동적크롤링을 활용하여 기업에 필요한 특허에 관한 정보들을 얻어내고자 한다.



### 3. System overview

본 프로젝트의 개요는 다음과 같습니다.
![system flow chart](https://user-images.githubusercontent.com/84506968/177123147-ef50036b-df55-4852-84d8-f694aea4d0ed.png)
먼저 시스템의 flow chart는 위의 그림과 같습니다.
크게는 3개의 기능으로 구성되어있습니다.
Google patent의 단순검색, 세부검색 그리고 apple patent에 키워드 검색으로 구성되어 있습니다.
또한 각각의 함수들은 실행시에 더 많은 시간이 소요되기 때문에 선택적으로 필요한 함수들만을 실행할 수 있습니다.
![system activity diagram](https://user-images.githubusercontent.com/84506968/177123506-3730b11a-7273-4b3f-87fa-c0b8a94e2b55.png)
다음으로는 저희가 설계한 system activity diagram입니다.
User들은 webpage에 접속해서 해당 함수들을 사용할 수 있습니다.


### 4. File Description

![image](https://user-images.githubusercontent.com/84506968/177119727-ada8a70b-c538-41e4-98da-4f01499b5750.png)

​	**(1)** **Data** : 크롤링을 통해 얻은 데이터들

​	**(2)** **HTML** : HTML 렌더링을 위한 코드와 HTML파일들

​	**(3)** **PDF_document** : 인턴과정 중에 작성한 보고서

​	**(4)** **Source** : 본 프로젝트에 사용된 source file



### 5. Contents

​	**(1) Tutorial0 : Environment setting**

- [Reference Link](https://github.com/jw-park-980508/Digital-Twin-Automation/blob/main/Automation/mdfiles/Tutorial0_EnvironmentSetting.md)

  ​**(2) Tutorial1 : Classification of facial expressions**

- [Reference Link](https://github.com/jw-park-980508/Digital-Twin-Automation/blob/main/Automation/mdfiles/Tutorial1_ClassificationofFacialExpressions.md)

  **(3) Tutorial2 : Generate coordinate**

- [Reference Link](https://github.com/jw-park-980508/Digital-Twin-Automation/blob/main/Automation/mdfiles/Tutorial2_GenerateCoordinate.md)

  ​**(4) Tutorial3 : Drawing emoticons**

- [Reference Link](https://github.com/jw-park-980508/Digital-Twin-Automation/blob/main/Automation/mdfiles/Tutorial3_Drawing%20emoticons.md)

  ​**(5) Tutorial4 : End-effector**

- [Reference Link](https://github.com/jw-park-980508/Digital-Twin-Automation/blob/main/Automation/mdfiles/Tutorial4_EndEffector.md)

  ​**(6) Demo vedio & Furtherwork**

- [Reference Link](https://github.com/jw-park-980508/Digital-Twin-Automation/blob/main/Automation/mdfiles/DemoVideo_FutureWork.md)
