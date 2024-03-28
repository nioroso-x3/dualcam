from picamera2 import Picamera2, MappedArray
import cv2
import numpy as np
import time
out_send = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=4 bitrate=3000 speed-preset=1 key-int-max=40 ! rtph264pay config-interval=-1 ! udpsink host=192.168.1.82 port=5600',cv2.CAP_GSTREAMER,0, 20, (1920,720), True)

camIR = Picamera2(0)
camRGB = Picamera2(1) 


camIR.configure(camIR.create_still_configuration(main={"size": (1456, 1088),"format": "RGB888"},lores={"size": (960, 720),"format": "RGB888"},controls={"ExposureTime":3000, "Saturation": 0.0,"Sharpness":1.2},buffer_count=3))
camRGB.configure(camIR.create_still_configuration(main={"size": (1456, 1088),"format": "RGB888"},lores={"size": (960, 720),"format": "RGB888"},controls={"ExposureTime":3000, "Sharpness":1.2},buffer_count=3))

cams = [camIR,camRGB]

res = [cam.start() for cam in cams]

#jobs = [cam.capture_array(wait=False) for cam in cams]

#for cam, job in zip(cams,jobs):
#    array = cam.wait(job)
#    print(array.shape)

cnt=0
still = np.zeros((1088,2912,3),np.uint8)
vid = np.zeros((720,1920,3),np.uint8)
frametimes = []
while(cnt < 2000):
    st = time.time()
    requests = [cam.capture_request() for cam in cams]
    if(cnt % 10 == 0):
        still[:1088,:1456] = requests[0].make_array("main")
        still[:1088,1456:2912] = requests[1].make_array("main")
        cv2.imwrite("test_{}.png".format(str(cnt)),still)
        print("image {} written".format(str(cnt)))
    vid[:720,:960] = requests[0].make_array("lores")
    vid[:720,960:1920] = requests[1].make_array("lores")
    requests[0].release()
    requests[1].release()
    out_send.write(vid)
    cnt+=1
    frametimes.append(time.time()-st)
print(np.median(frametimes),np.average(frametimes))
res = [cam.stop() for cam in cams]
