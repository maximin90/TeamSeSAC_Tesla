# <cvs file처리하는 모듈>
# 설명 : 2020 ~ 2023년으로 시작하는 csv 파일 전부 read, merge, save 하는 모듈
import pandas as pd
import os


# <테슬라 뉴스 파일 병합하기>
def merge_csv(dirpath):
    file_list = os.listdir(dirpath)
    file_list_csv = [file for file in file_list if file.endswith('.csv')]

    merged_df = pd.DataFrame()

    for file in file_list_csv:
        file_path = os.path.join(dirpath, file)
        df = pd.read_csv(file_path, dtype='object')
        merged_df = pd.concat([merged_df, df])

    # 병합된 데이터 프레임 반환
    return merged_df


#불려온 cvs 파일을 dataframe으로 리턴   
def read_csv(dirpath):
    merged_file = dirpath + '.csv'
    df = pd.read_csv(merged_file)
    return df

# csv 파일 저장
def save_csv(df, savepath, fileName) : # save_file -> save_csv
    fileFormat = '.csv'
    df.to_csv(savepath + fileName + fileFormat ,index=False, encoding='utf-8-sig')



# <테슬라 주식 파일 병합하기>
# dirpath : 테슬라 파일 주식 위치
# savepath : 저장할 파일 위치
# fileName : 저장할 파일 이름
def stock_merge_csv(dirpath, savepath, fileName):
    
    file_list = os.listdir(dirpath)
    file_list_csv = [file for file in file_list if file.endswith('.csv')]

    merged_df = pd.DataFrame()
    
    for file in file_list_csv:
        # 파일명에서 연도 정보 추출 (예: "2022_01_news_data.csv")
        #2020 ~ 2023년도 daily가 포함된 파일명만 merge
        if 'daily' in file and ['2023','2022','2021','2020']:
            print(file)
            df = pd.read_csv(dirpath + file, dtype='object')
            merged_df = merged_df._append(df)
    #동일한 폴더에 병합한 csv 파일 저장
    merged_df.to_csv(savepath + fileName + ".csv", index=False, encoding='utf-8-sig')


# <twit 파일 병합하기>
# dirpath : 테슬라 파일 주식 위치
# savepath : 저장할 파일 위치
# fileName : 저장할 파일 이름
def twit_merge_csv(dirpath,savepath,fileName):
    
    file_list = os.listdir(dirpath)
    file_list_csv = [file for file in file_list if file.endswith('.csv')]

    merged_df = pd.DataFrame()
    
    for file in file_list_csv:
        # 파일명에서 연도 정보 추출 (예: "2022_01_news_data.csv")
        #2020 ~ 2023년도 twit이 포함된 파일명만 merge
        if 'twit' in file and ['2023','2022','2021','2020']:
            print(file)
            df = pd.read_csv(dirpath + file, dtype='object')
            merged_df = merged_df._append(df)
    #동일한 폴더에 병합한 csv 파일 저장
    merged_df.to_csv(savepath + fileName + ".csv", index=False, encoding='utf-8-sig')
