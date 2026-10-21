import cv2, sys, json
cap = cv2.VideoCapture(sys.argv[1])
det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
fps = cap.get(cv2.CAP_PROP_FPS); out = []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i % int(fps/2) == 0:
        h, w = f.shape[:2]
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        fs = det.detectMultiScale(g, 1.1, 6, minSize=(w//5, w//5))
        if len(fs):
            x, y, fw, fh = max(fs, key=lambda r: r[2]*r[3])
            out.append([round(i/fps,1), round(x/w,3), round(y/h,3), round((x+fw)/w,3), round((y+fh)/h,3)])
    i += 1
json.dump(out, open(sys.argv[2], "w"))
ys=[o[2] for o in out]; ye=[o[4] for o in out]; xs=[o[1] for o in out]; xe=[o[3] for o in out]
print(len(out), "detections; top", min(ys), max(ys), "bottom", min(ye), max(ye), "left", min(xs), "right", max(xe))
