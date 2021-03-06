import numpy as np
import cv2
import os

## KNN algorithm for matchinf faces
def distance(v1, v2):
    return np.linalg.norm(v1-v2)


def knn(train, test, k=3):
    dist=[]
    for i in range(train.shape[0]):
        ix =train[i, :-1]
        iy =train[i, -1]
        d=distance(ix, test)
        dist.append([d, iy])
    dk=sorted(dist, key=lambda x:x[0])[:k]    
    labels=np.array(dk)[:, -1]
    freq=np.unique(labels,return_counts=True)
    out=np.argmax(freq[1])
    return freq[0][out]
    
    
cap=cv2.VideoCapture(0)
face_cascade=cv2.CascadeClassifier('/anaconda3/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')

dataset_path='/Users/adityakumar/Desktop/Face Recognition/'
facedata=[]
labels=[]
class_id=0
names={}

for fx in os.listdir(dataset_path):
    if fx.endswith('.npy'):
        a, b=fx.split('.')
        names[class_id]=a
        data_item=np.load(dataset_path+fx)
        facedata.append(data_item)
        target=class_id*np.ones((data_item.shape[0],))
        labels.append(target)
        class_id+=1
face_dataset=np.concatenate(facedata, axis=0)
face_labels=np.concatenate(labels, axis=0).reshape((-1,1))#here -1 in reshape means it will figure out no.of rows on its own
print(face_labels.shape)
print(face_dataset.shape)

trainset=np.concatenate((face_dataset, face_labels), axis=1)
print(trainset.shape)




font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	ret, frame = cap.read()
	if ret == False:
		continue
	# Convert frame to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect multi faces in the image
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for face in faces:
		x, y, w, h = face

		# Get the face ROI
		offset = 7
		face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
		face_section = cv2.resize(face_section, (100, 100))

		out = knn(trainset, face_section.flatten())

		# Draw rectangle in the original image
		cv2.putText(frame, names[int(out)],(x,y-10), font, 1,(255,0,0),4,cv2.LINE_AA)
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

	cv2.imshow("Faces", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
