import requests  # requests 모듈 임포트
from datetime import datetime

def download_file(file_url, save_path):
    with open(save_path, 'w', encoding='utf-8') as f: # 저장할 파일을 바이너리 쓰기 모드로 열기
        response = requests.get(file_url) # 파일 URL에 GET 요청 보내기
        f.write(response.text) # 응답의 내용을 파일에 쓰기

def get_current_date_string():
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

def extract_lines_in_range(file_path, linenum):
    with open(file_path, 'r', encoding='utf-8') as f:
        line = f.readlines()[linenum - 1]  # 리스트 슬라이싱으로 특정 범위 라인 x`읽기
        return line.strip()

# URL과 저장 경로 변수를 지정합니다.
url = f'https://apihub.kma.go.kr/api/typ01/url/fct_afs_dl.php?&stn=131&reg=11C10301&disp=0&help=1&authKey=lCL7eoqyTzGi-3qKst8xEQ'
save_file_path = './OpenSourceBasicProj_Ass/teamproj/output_file5.txt'

# 파일 다운로드 함수를 호출합니다.
download_file(url, save_file_path)

# 사용 예시: 3번째부터 6번째 라인까지 추출
finalData = []
for i in range(24, 25): #24, 31
    data = extract_lines_in_range(save_file_path, i)
    finalData.append({'rainchance' : data[82:84]}) #'datetime' : data[22:34],
#print(f'NOW - time: {data[:12]}, temp: {data[65:68]}, rain: {data[89:93]}')
#print(finalData)

def finalarr(shared_list):
    try:
        # 원래 하던 데이터 수집 및 파싱 작업
        finalData = []
        for i in range(24, 25): #24, 31
            data = extract_lines_in_range(save_file_path, i)
            finalData.append({'rainchance' : data[82:84]})

        shared_list.append(finalData)
    except Exception as e:
        print(f"[data5] 오류 발생: {e}")
        shared_list.append({})  # 원하면 빈 dict라도 넣기
