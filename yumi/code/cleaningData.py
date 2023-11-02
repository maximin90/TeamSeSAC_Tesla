import re, unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = ['월', '위', '일', '억', '년', '원', '지난해', '를', '것', '등','차','올해','챗'
              '위', '가', '조', '의', '및','약','수','주','기자','만','이','중','말','마하','미','거','게','고','분','때문','때','더','점','씨',
              '전','개','디','은','론','닉','키','김','책','그',
              '팀','스케','용','닉스', '이번', '그룹', '현지', '로이터', '전국', '하나', '루', '중이', '경찰', '자기', '확인', '운동', '남성',
              '확', '집', '전달', '토크', '륜', '의학', '거주', '곳', '소', '기', '재', '하이', '초', '공간', '배포', '총',
              '무단', '이마트', '대구', '저작권', '강동', '수다', '뉴스', '줌', '텍사스', '헬', '대신', '이름', '텍', '텍사스주',
              '플로리다', '캘리포니아주', '약관', '본사', '건', '장기', '감염증', '캐릭터', '달이', '김혜민', '청원', '창',
              '마스터', '산', '강원도', '부분', '주인', '알렉스', '제', '좀', '네', '보', '로직', '루다', '중산', '생수', '엠씨',
              '선', '타이', '커피', '에브리싱', '명의', '베이커', '크루', '스프링', '완', '타고', '세션', '순', '발', '스틱'
              '개사', '만점', '대성', '데일리안', '킥', '수단', '부문', '플라잉', '별', '날', '장', '대한', '기업', '뉴욕', '가장',
              '로', '달', '대표', '업체', '사업', '미래','계획', '세계', '회사', '업계',
              '기존', '통해', '관련', '현재', '지난', '시장', '카','그룹', '차량', '협업', '행차', '기록', '백화점', '대비',
              '대로', '전체', '고객', '공개', '서울', '이상', '아이오', '적용', '예정', '시간', '예상', '사', '로',
              '예스', '교수', '게임', '아이', '선', '대비', '며', '업종', '뉴시스', '서명', '바이', '산', '파이낸셜 뉴스',
              '이후', '보도', '제','총', '가장', '제프', '억만장자', '최고', '부자','창업', '조스', '최대', '지급',
              '국고', '차등', '위해', '미만', '이상', '경우', '개편', '일부', '지금', '생각', '우리', '요', '또', '앵커',
              '상황', '얘기', '정도', '안', '사실', '사람', '하나', '좀', '경우', '재개', '부분', '가지', '계속', '오늘',
              '볼', '걸', '수도', '저','왜', '회장', '박', '대해', '며', '영상', '자신', '에스', '명', '이메일', '사업자',
              '최근', '응답', '리움', '정부', '대표', '대통령', '국민', '면', '부산', '정치', '후보', '오늘', '안',
              '문', '장관', '회의', '사회', '주택', '제', '힘', '민주당', '오', '최근', '요', '와이드', '지리', '목표']


#공백제거
def trim_pattern_whitespace(df) :
    pattern_whitespace = re.compile(r'[\s]+')
    df = df.replace(pattern_whitespace, ' ').map(lambda x: unicodedata.normalize('NFC', x)).str.strip()
    return df

#정규화 처리
def clean_byline(text):
    # byline
    pattern_email = re.compile(r'[-_0-9a-z]+@[-_0-9a-z]+(?:\.[0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_url = re.compile(r'(?:https?:\/\/)?[-_0-9a-z]+(?:\.[-_0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_others = re.compile(r'\.([^\.]*(?:기자|특파원|지난해|교수|서울|사진|작가|뉴스|대표|논설|고문|주필|부문장|팀장|장관|원장|연구원|이사장|위원|실장|차장|부장|에세이|화백|사설|소장|단장|과장|기획자|큐레이터|저작권|평론가|©|©|ⓒ|\@|\/|=|:앞쪽_화살표:|무단|전재|재배포|금지|\[|\]|\(\))[^\.]*)$')
    pattern_onlyKorean = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기만 추출
    result = pattern_email.sub('', text)
    result = pattern_url.sub('', result)
    result = pattern_others.sub('.', result)
    result = pattern_onlyKorean.sub('',result)
    
    # 본문 시작 전 꺽쇠로 쌓인 바이라인 제거
    pattern_bracket = re.compile(r'^((?:\[.+\])|(?:【.+】)|(?:<.+>)|(?:◆.+◆)\s)')
    result = pattern_bracket.sub(' ', result).strip()
    return result

#한글 불용화 처리
def remove_korean_stopwords(nouns_list):
    return [word for word in nouns_list if word not in stop_words]

#트위터 이모티콘 제거
def remove_emoji(text):
    # 이모티콘 패턴 정의
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # 스마일리 이모티콘
                               u"\U0001F300-\U0001F5FF"  # 기호 이모티콘
                               u"\U0001F680-\U0001F6FF"  # 트랜스포트 및 심볼 이모티콘
                               u"\U0001F700-\U0001F77F"  # 알파벳 보완 및 심볼 이모티콘
                               u"\U0001F780-\U0001F7FF"  # 기호 보충 이모티콘
                               u"\U0001F800-\U0001F8FF"  # 기호 보충 이모티콘
                               u"\U0001F900-\U0001F9FF"  # 기호 보충 이모티콘
                               u"\U0001FA00-\U0001FA6F"  # 게임 이모티콘
                               u"\U0001FA70-\U0001FAFF"  # 게임 이모티콘
                               u"\U0001F004-\U0001F0CF"  # 추가 기호 이모티콘
                               u"\U0001F004-\U0001F0CF"  # 추가 기호 이모티콘
                               u"\U00002702-\U000027B0"  # 도서 및 표지 이모티콘
                               u"\U000024C2-\U0001F251" 
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               "]+", flags=re.UNICODE)
    # 이모티콘 제거
    text_without_emoji = emoji_pattern.sub(r'', text)
    return text_without_emoji

#축약어 처리
def expand_contractions(text):
    # 축약형 패턴 정의
    contractions = {
        "won’t": "will not",
        "can’t": "cannot",
        "I’m" : "I am",
        "you’re" : "you are",
        "it’s" : "it is",
        "didn’t" : "did not",
        "doesn't" : "does not",
        "we’re" : "we are",
        "shouldn’t" : "should not",
        "they’re" : "they are",
        "haven’t" : "have not",
        "should’ve" : "should have",
        "would’ve" : "would have",
        "could’ve" : "could have"
    }
    
    # 축약형을 확장
    for contraction, expansion in contractions.items():
        text = re.sub(contraction, expansion, text)
    
    return text

#트위터 처리
def clean_tweet(tweet):
    # URL 제거
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    # 해시태그(#)와 멘션(@) 제거
    tweet = re.sub(r'\B#\w+', '', tweet)
    tweet = re.sub(r'\B@\w+', '', tweet)
    # 소문자 변환
    tweet = tweet.lower()
    #이모티콘 제거
    tweet = remove_emoji(tweet)
    #축약어 없애기
    tweet = expand_contractions(tweet)
    #특수문자 제거
    tweet = re.sub(r'[^a-zA-Z0-9\s]', '', tweet)
    #영어만 추출
    #tweet = re.sub(r'[^a-zA-Z]', ' ', tweet)
    return tweet

#불용어 처리
#각 텍스트에 대해 불용어 제거와 토큰화 수행
#text : 입력값, stop_word_list : 불용어 리스트
#불용어 리스트 불려오기
stop_word_list = stopwords.words('english')
def remove_stopwords_and_tokenize(text):
    #단어 토큰화
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in stop_word_list]
    return filtered_tokens
