## 소개
- 대구대학교 기숙사생들과 기숙사 관리 동아리 임원들이 말하는 몇 문제점이 있다. 해당 문제점을 해결하기 위해 기숙사 관련 챗봇을 제작하면 기숙사를 이용하는 학생의 만족도가 높아지며 기숙사 관련 동아리의 인원들도 편의성이 높아질 것이라 예상되어 기숙사 관리 동아리 임원과 협업하여 진행하였다.
- 기숙사에 생활하는 학생들이 말하는 불편한 점
1. 기숙사 관련 공지가 홈페이지에만 올라온다는 점이다. 이 경우 기숙사생들은 중요 공지사항을 실시간으로 확인하기 힘들다.
2. 기숙사 관련 질문사항이 생겼을 경우 질문하는 방법이 직접 방문 혹은 개인 번호를 가지고 있지 않는 이상 질문하는데에 어려움이 있다.
- 기숙사 관리 동아리 임원들이 말하는 불편한 점
1. 중요 공지사항을 기숙사생들에게 전달을 하였으나 해당 공지사항 확인이 늦거나 못보는 경우가 많다
2. 기숙사 관련 행정실에서 공지를 올려줄 경우 여러 페이지에서 각각 올라오기 때문에 매번 모든 페이지에 방문하여 공지사항이 올라왔는지 확인하는 경우 번거로움이 있다.

**위 기능은 기숙사 관리 동아리의 회장, 임원들과 컨택 후 기획, 설계, 개발을 진행하였습니다.**

## 프로젝트 주요 내용
- 기숙사를 이용하는 학생들에게 도움을 주기 위해서 텔레그램 챗봇 오픈소스와 파이썬 Flask를 활용하여 기숙사 챗봇을 제작한다.
- 기숙사 생활을 하는 학생들의 경우 실시간 공지를 텔레그램 메신저로  전송한다. 또한 추가적으로 링크를 전송해 자세한 내용 확인이 가능하다.
기숙사 관련 질문사항이 생겼을 경우 챗봇을 이용해 기숙사 관리 동아리 임원에게 내용이 전달된다
- 기숙사 관리 동아리 임원의 경우 임원만의 개인 아이디를 데이터베이스에 추가해 임원들만 이용할 수 있는 기능들을 임원들에게 제공한다. 이는 기숙사생 전체 및 임원들만 이용할 수 있는 기능들이 포함되어 있다.
기숙사 관련 행정실에서 전달하는 공지에 대해서 기숙사 동아리 임원들만 확인하는 공지 내용과 모든 기숙사생들을 대상으로 한 공지를 필터링해서 각자에게 전달한다.
- 공지사항 크롤링 및 관리자 아이디 정보 등 저장 데이터들은 json 파일의 입출력을 통해 별도 관리하였다.

## 기대효과
공지사항을 자주 확인하지 않는 학생들과 기숙사 관련 질문 및 기숙사를 관리하는 사람들의 업무 활용성을 높여주는데 많은 도움이 될 것이라 예상한다. 또한 기숙사 관리 동아리의 임원들과의 협업을 지속적으로 유지하여 성능 개선에도 많은 도움이 될 것이라 예상한다.

## 개발환경
- Python3
- BeautifulSoup
- Telegram API
- AWS EC2
- Rest API
- PyCharm IDE

## 실행 화면 (모바일 - iPhoneXS)
<img src="https://i.esdrop.com/d/f/eoVlczNHjw/4NmPrJTNG8.jpg"  width="200" height="400"/><img src="https://i.esdrop.com/d/f/eoVlczNHjw/goeg4PYGDB.jpg"  width="200" height="400"/>
<img src="https://i.esdrop.com/d/f/eoVlczNHjw/BmP3ewN7h2.png"  width="200" height="400"/><img src="https://i.esdrop.com/d/f/eoVlczNHjw/6F5KL8is7k.png"  width="200" height="400"/>
<img src="https://i.esdrop.com/d/f/eoVlczNHjw/tIqOnCE5Nt.png"  width="200" height="400"/><img src="https://i.esdrop.com/d/f/eoVlczNHjw/GrJ2f5KCx0.png"  width="200" height="400"/>
<img src="https://i.esdrop.com/d/f/eoVlczNHjw/NQW7TiFUtU.png"  width="200" height="400"/>

## 개발자 정보
대구대학교 컴퓨터공학과 [백대현](https://github.com/eogus65121)