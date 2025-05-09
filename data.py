#온도, 습도, 강수량
import requests  # requests 모듈 임포트

# URL과 저장 경로 변수를 지정합니다.
url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?&stn=131&help=1&authKey=xxxxxxxxxxxxxxxx'
save_path = './OpenSourceBasicProj_Ass/teamproj/output_file.txt'

try:
    with open(save_path, 'w', encoding='utf-8') as f: # 저장할 파일을 쓰기 모드로 열기
        response = requests.get(url) # 파일 URL에 GET 요청 보내기
        f.write(response.text) # 응답의 내용을 파일에 쓰기
except Exception as e1:
    print("데이터 받아오기 실패[1]")

def extract_lines_in_range(file_path, linenum):
    with open(file_path, 'r', encoding='utf-8') as f:
        line = f.readlines()[linenum - 1]  # 리스트 슬라이싱으로 특정 범위 라인 x`읽기
        return line.strip()

def finalarr(shared_list):
    try:
        data = extract_lines_in_range(save_path, 55)

        finalData = {'temp' : data[64:68], 'humidity' : data[76:80], 'rain' : data[89:93]}
        if float(finalData['rain']) <= 0:
            finalData['rain'] = '0.0'
        
        shared_list.append(finalData)
    
    except Exception as e2:
        print(f"[data] 오류 발생: {e2}")
        shared_list.append({})
