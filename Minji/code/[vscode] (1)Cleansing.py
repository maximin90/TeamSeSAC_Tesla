# 파일 불러오기
# 열 삭제_신문사, 주소
import pandas as pd

df = pd.read_csv('news_data_Feb2020.csv')
df.drop(['media', 'url'], axis=1, inplace = True)
df

# 본문 확인
df['content'][0]

# 바이라인 제거
'''
...했다. 지역=ㅇㅇㅇ 기자, 이메일 주소, ⓒ©, www.example.com
'''

# 본문 전처리
# 1. 이메일과 url을 먼저 제거
# 2. 마지막 문장 중 바이라인으로 추정되는 것을 찾아 제거
# TODO 바이라인 제거가 깔끔하게 되지 않음. 예외 찾아 추가 작업 필요
# r'\.([^\.]*(?:(?#email)(?:[-_0-9a-z]+(?:\.[\+0-9a-z]+)*@[0-9a-z]+\.[-_0-9a-z]+(?:\.[0-9a-z]+)*)|(?#url)(?:(?:https?:\/\/)?[0-9a-z]+\.[-_0-9a-z]+(?:\.[0-9a-z]+)*)|기자|특파원|교수|작가|대표|논설|팀장|장관|원장|연구원|이사장|위원|실장|차장|에세이|화백|사설|소장|단장|과장|기획자|큐레이터|저작권|평론가|©|©|ⓒ|@|\/|=|▶|무단|전재|재배포|금지)[^\.]*)$'

def clean_byline(text):
    # byline
    pattern_email = re.compile(r'[-_0-9a-z]+@[-_0-9a-z]+(?:\.[0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_url = re.compile(r'(?:https?:\/\/)?[-_0-9a-z]+(?:\.[-_0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_others = re.compile(r'\.([^\.]*(?:기자|특파원|교수|작가|대표|논설|고문|주필|부문장|팀장|장관|원장|연구원|이사장|위원|실장|차장|부장|에세이|화백|사설|소장|단장|과장|기획자|큐레이터|저작권|평론가|©|©|ⓒ|\@|\/|=|▶|무단|전재|재배포|금지||)[^\.]*)$')
    result = pattern_email.sub('', text)
    result = pattern_url.sub('', result)
    result = pattern_others.sub('.', result)

    # 본문 시작 전 꺽쇠로 쌓인 바이라인 제거
    pattern_bracket = re.compile(r'^((?:)|(?:【.+】)|(?:<.+>)|(?:◆.+◆)\s)')
    result = pattern_bracket.sub('', result).strip()

    return result

df['content'] = df['content'].map(clean_byline)

# 전처리된 본문 확인

df['content'][0]

# 전처리한 데이터 csv 파일로 저장

df['content'].to_csv('news_data_Feb2020_preprocessing..csv', index=False, encoding='utf-8-sig')