from flask import Flask, render_template, Response
import cv2
import numpy as np
import dotenv
import os
import sys

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)

app = Flask(__name__)

# 영상 파일 경로 지정
VIDEO_PATH = 'http://172.21.4.223:8081/0/stream'

def gen_size_frames():
	cap = cv2.VideoCapture(VIDEO_PATH)
	while True:
		success, frame = cap.read()
		if not success:
			break
		else:
			x=int(os.environ['X'])
			y=int(os.environ['Y'])
			w=int(os.environ['W'])
			h=int(os.environ['H'])
			# Load image, grayscale, Gaussian blur, Otsu's threshold
			img = cv2.imread('/var/log/motion/image.jpg')

			roi = img[y:y+h, x:x+w]     # roi 지정
			image = roi.copy()           # roi 배열 복제 ---①

			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(gray, (5, 5), 0)
			edged = cv2.Canny(gray, 0, 180)

			# Find bounding box
			x,y,w,h = cv2.boundingRect(edged)
			cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
			cv2.putText(image, "w={},h={}".format(round(w*2.54/96, 1),round(h*2.54/96, 3)), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)
			
			ret, buffer = cv2.imencode('.jpg', image)
			image = buffer.tobytes()
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
            
	cap.release()

def gen_frames():
	cap = cv2.VideoCapture(VIDEO_PATH)
	while True:
		# 프레임 읽기
		ret, frame = cap.read()

		if not ret:
			break

		# JPEG 인코딩
		ret, buffer = cv2.imencode('.jpg', frame)

		# 스트리밍 데이터 생성
		frame = buffer.tobytes()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	# 리소스 해제
	cap.release() 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/size_feed')
def size_feed():
	return Response(gen_size_frames(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
	return Response(gen_frames(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
