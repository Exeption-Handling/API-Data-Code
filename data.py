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
url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?&stn=131&help=1&authKey=lCL7eoqyTzGi-3qKst8xEQ'
save_file_path = './OpenSourceBasicProj_Ass/teamproj/output_file.txt'

# 파일 다운로드 함수를 호출합니다.
download_file(url, save_file_path)

def finalarr(shared_list):
    try:
        # 원래 하던 데이터 수집 및 파싱 작업
        data = extract_lines_in_range(save_file_path, 55)

        finalData = {'temp' : data[64:68], 'humidity' : data[76:80], 'rain' : data[89:93]}
        if float(finalData['rain']) <= 0:
            finalData['rain'] = '0.0'
        
        shared_list.append(finalData)
    
    except Exception as e:
        print(f"[data] 오류 발생: {e}")
        shared_list.append({})  # 원하면 빈 dict라도 넣기
