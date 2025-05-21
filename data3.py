import requests
import json
from collections import defaultdict

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
params ={'serviceKey' : 'L8/lsHDixFmS2p34yAH8Q9glQii9ughw2dcw5Hu6SH4gO0rrtNOPEevNbd3nbvW8NzCbwuPPxBHUTqs7aFzLww==', 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : '20250520', 'base_time' : '2300', 'nx' : '68', 'ny' : '107' }

save_path = './OpenSourceBasicProj_Ass/teamproj/output_file3.json'
try:
    with open(save_path, 'w', encoding='utf-8') as f:
        response = requests.get(url, params=params)
        formatted_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
        f.write(formatted_json)
except Exception as e1:
    print("데이터 받아오기 실패[3]")

def finalarr(shared_list2):
    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
            items = data['response']['body']['items']['item']
            grouped = defaultdict(list)
            for item in items:
                if item['category'] == 'TMP':
                    grouped['temp'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
                elif item['category'] == 'TMN':
                    grouped['mintemp'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
                elif item['category'] == 'TMX':
                    grouped['maxtemp'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
                elif item['category'] == 'SKY':
                    grouped['sky'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
                elif item['category'] == 'REH':
                    grouped['humidity'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
                elif item['category'] == 'PTY':
                    grouped['raintype'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
                elif item['category'] == 'WSD':
                    grouped['wind'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
                elif item['category'] == 'PCP':
                    if item['fcstValue'] == '강수없음':
                        item['fcstValue'] = 0.0
                    elif item['fcstValue'] == '1mm 미만':
                        item['fcstValue'] = 0.5
                    elif item['fcstValue'] == '30.0~50.0mm':
                        item['fcstValue'] = 40.0
                    elif item['fcstValue'].endswith('mm'):
                        item['fcstValue'] = float(item['fcstValue'].replace('mm', ''))
                    else:
                        item['fcstValue'] == 50.0
                    grouped['rain'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
            shared_list2.append(grouped)
    except Exception as e2:
        print(f"[data3] 오류 발생: {e2}")
        shared_list2.append({})

shared_list2 = []
with open(save_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

    items = data['response']['body']['items']['item']
    grouped = defaultdict(list)
    for item in items:
        if item['category'] == 'TMP':
            grouped['temp'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
        elif item['category'] == 'TMN':
            grouped['mintemp'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
        elif item['category'] == 'TMX':
            grouped['maxtemp'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
        elif item['category'] == 'SKY':
            grouped['sky'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
        elif item['category'] == 'REH':
            grouped['humidity'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
        elif item['category'] == 'PTY':
            grouped['raintype'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
        elif item['category'] == 'WSD':
            grouped['wind'].append([item['fcstDate']+item['fcstTime'], item['fcstValue']])
    shared_list2.append(grouped)
    print(shared_list2[0]['grouped'])