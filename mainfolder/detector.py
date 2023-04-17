import cv2
from cvlib.object_detection import draw_bbox
import os
import cvlib as cv



vehicle = ["car","motorcycle","bus","truck","bicycle"]

def retLSdr(im_dir):
    ls = os.listdir(im_dir)
    ls.sort()
    list_data = []
    for img_name in ls[:]:
        if ".jpg" in img_name or ".jpeg" in img_name or ".png" in img_name: 
            img_name = os.path.join(im_dir,img_name)
            list_data.append(img_name)
    return list_data
inputIm = retLSdr("Input_images")
conf_level = 0.24

def get_count(In_img):
    bbox, label, conf = cv.detect_common_objects(In_img,confidence=conf_level, nms_thresh=0.3, model='yolov4')#'yolov3-tiny','yolov4'
    for j in label:
        if j in vehicle:
            pass
        else:label.remove(j)
    output_image = draw_bbox(In_img, bbox, label, conf)
    return [output_image,len(label)]
if __name__ == '__main__':
    for i in inputIm:
        i= cv2.imread(i)
        im,vCount = get_count(i)
        print('Vehicl count : ' ,vCount)