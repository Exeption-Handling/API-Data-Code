import requests

url = 'http://apis.data.go.kr/6430000/realtimeStandbyInfoService/getRealtimeStandbyInfo'
params ={'serviceKey' : 'L8/lsHDixFmS2p34yAH8Q9glQii9ughw2dcw5Hu6SH4gO0rrtNOPEevNbd3nbvW8NzCbwuPPxBHUTqs7aFzLww==', 'currentPage' : '1', 'perPage' : '10', 'CODE' : '533112' }

save_path = './OpenSourceBasicProj_Ass/teamproj/output_file3.txt'
with open(save_path, 'w', encoding='utf-8') as f:
    response = requests.get(url, params=params)
    f.write(response.text)
print(response.content)