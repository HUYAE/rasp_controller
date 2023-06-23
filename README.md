# 설치방법

## 1. git clone

## 2. pip install opencv-python paho-mqtt python-dotenv python-crontab motion

## 3. .env 파일 생성 후 db정보와 mqtt브로커 정보 입력

## 4. ./websocket/today.py 실행시 날씨정보 및 농산물 거래정보를 가져와 분석후 예측결과 도출

## 5. ./crontab/dht22.py 온도, 습도 등 환경센서 측정 후 DB에 저장

## 6. ./crontab/valve_mqtt.py 실행시 mqtt가 실행되면서 밸브 연결확인후 동작명령 수신 대기

## 7. ./crontab/size_roi.py를 통해 현재 motion에서 촬영중인 영상을 캡쳐 -> 작물의 위치를 설정하면 자동으로 .env파일에 저장
