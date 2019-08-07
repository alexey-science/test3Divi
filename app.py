from flask import Flask, make_response, redirect, url_for, jsonify, request
import cv2

app = Flask(__name__)
cascadPath = "haarcascade_frontalface_default.xml"
video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cascadPath)

@app.route('/')
def index():
    return 'Use /get_result?type={json|image} for result'

def gen_face_json():
    rval, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    faces_json = []
    for (xx,yy,w,h) in faces:
        faces_json.append({
            "x": int(xx),
            "y": int(yy),
            "width": int(w),
            "height": int(h)
        })
      
    return faces_json

def gen_face_image():
    rval, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    res, img = cv2.imencode('.jpg', frame)
    return img.tobytes()

@app.route('/getResult/')
def get_result(): 
    if request.args.get('type', '').lower() == 'json':
        return jsonify(gen_face_json())
    elif request.args.get('type', '').lower() == 'image':
        response = make_response(gen_face_image())
        response.headers.set('Content-Type', 'image/jpeg')
        #response.headers.set(
        #'Content-Disposition', 'attachment', filename='faces.jpg')
        return response
    else:
        return redirect(url_for('index'))
    return redirect(url_for('index'))
