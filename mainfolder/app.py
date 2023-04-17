

# from unicodedata import name
from flask import Flask, jsonify,render_template,request,Response,redirect,flash
import os
import cv2
# import numpy as np
from werkzeug.utils import secure_filename
import detector
import serial
# import time


imLen = 0
def clearImage():
    cd = os.path.join(os.getcwd(),"static\\images\\imageIN")
    files = os.listdir(cd)
    for f in files:
        try:
            os.remove(os.path.join(cd, f))
        except:
            pass
ser = 0
'''def check_port():
    global ser
    for i in range(0,256):
        try:
            ser = serial.Serial('COM'+str(i),9600,timeout=1)
            print('COM'+str(i))
            com = 'COM'+str(i)
        except :
            pass
            #print("Connect the device")
    print(ser)
def sendData(x):
    global ser
    try:
        x = str(x).encode("utf-8")
        ser.write(x)
    except Exception as e:
        print(e)
        #check_port()
        #ser.write(x)'''
def save_file(name,path,obj):
    f_path = os.path.join(path, name)
    if not os.path.exists(f_path):
        os.makedirs(f_path)
    for file in obj:
        filename = secure_filename(file.filename)  
        f_path1 = f_path
        f_path1 = os.path.join(f_path1, filename)
        if not os.path.exists(f_path1):
            file.save(f_path1)
        return filename
########################################################################################
video = cv2.VideoCapture(0)
app = Flask(__name__)

########################################################################################
@app.route('/',methods=["get","post"])
def server_app():
    #check_port()
    return render_template("home.html")
########################################################################################
#REAL TIME
@app.route('/realtime',methods=["get","post"])
def main():
    global imLen
    if request.method == "GET":
        return render_template("realTime.html")
    else:
        return jsonify({"status":imLen})
########################################################################################
def gen(video):
    global imLen
    cam=cv2.VideoCapture(0)
    cam.set(3,1080)
    cam.set(4,1024)
    while True:
        try:
            _,image=cam.read()
            image = cv2.flip(image, 1)
            image = detector.get_count(image)[0]
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        except Exception as e:
            print("Error : ",e)
########################################################################################
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
########################################################################################
########################################################################################
#IMAGE INPUT
@app.route('/form',methods=["get","post"])
def form():
    try:
        if request.method == 'POST':
            if len(request.files) < 4:
                if request.data.decode('utf-8')=="check":
                    print("no file")
                    return jsonify({"status":"1"})                    
            else:
                clearImage()
                # print(request.files)
                imgFile1 = request.files.getlist("Image1")
                imgFile2 = request.files.getlist("Image2")
                imgFile3 = request.files.getlist("Image3")
                imgFile4 = request.files.getlist("Image4")
                


                a_path = os.path.join(os.getcwd(), 'static\\images')


                imName1 = save_file("imageIN",a_path,imgFile1)
                imName2 = save_file("imageIN",a_path,imgFile2)
                imName3 = save_file("imageIN",a_path,imgFile3)
                imName4 = save_file("imageIN",a_path,imgFile4)

                a_path1 = os.path.join(os.getcwd(), 'static\\images\\imageIN\\'+imName1)
                a_path2 = os.path.join(os.getcwd(), 'static\\images\\imageIN\\'+imName2)
                a_path3 = os.path.join(os.getcwd(), 'static\\images\\imageIN\\'+imName3)
                a_path4 = os.path.join(os.getcwd(), 'static\\images\\imageIN\\'+imName4)


                img1 = cv2.imread(a_path1)
                img2 = cv2.imread(a_path2)
                img3 = cv2.imread(a_path3)
                img4 = cv2.imread(a_path4)

                img1,c1 = detector.get_count(img1)
                img2,c2 = detector.get_count(img2)
                img3,c3 = detector.get_count(img3)
                img4,c4 = detector.get_count(img4)

                vc_list = [c1,c2,c3,c4]
                vc = max(vc_list)
                vl = vc_list.index(vc)

                print("List :",vc_list)
                print("Maximum Count :",vc)
                print("Location :",vl)
                #sendData(vl+1)


                cv2.imwrite(a_path1,img1)
                cv2.imwrite(a_path2,img2)
                cv2.imwrite(a_path3,img3)
                cv2.imwrite(a_path4,img4)

                return jsonify({"status":"0","image":
                ["static\\images\\imageIN\\"+imName1,
                "static\\images\\imageIN\\"+imName2,
                "static\\images\\imageIN\\"+imName3,
                "static\\images\\imageIN\\"+imName4
                ],
                "vcl":vc_list,
                "vl":vl,"vc":vc})
        else:
            return render_template("imageIn.html")
    except Exception as e:
        print("error",e)
    return jsonify({"status":"1"})
    
########################################################################################


if __name__ == '__main__':
    app.run( host='0.0.0.0',port=5000,debug=True) 
    # app.run(host="0.0.0.0",port= 6000,debug=True)
    image = 0
    # dataOccured = 