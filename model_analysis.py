import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.models import load_model

import numpy as np
import cv2 as cv
from notification import notify


model = load_model("my_model.h5")

model_classes = ['fight', 'nofight']
# pose
model_pose = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model_pose.signatures['serving_default']


def prepare(img):
    # Resize image
    img = img.copy()
    img = np.resize(img, (360, 480, 3))
    img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 192,256)
    input_img = tf.cast(img, dtype=tf.int32)

    # Detection section
    results = movenet(input_img)
    keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))


    #make a blank img to render pose on it
    blank = np.zeros((360, 480, 3),dtype=np.uint8)

    # Render keypoints 
    loop_through_people(blank, keypoints_with_scores, EDGES, 0.1)

    return blank
# Function to loop through each person detected and render
def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
    for person in keypoints_with_scores:
        draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)

def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv.circle(frame, (int(kx), int(ky)), 3, (0,255,0), -1)

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}
def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
            cv.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 4)



# get video and analyze

def analyze(cam_id):
    
    cap = cv.VideoCapture(cam_id)
    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video stream or file")

    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            img_arr = prepare(frame)
            img_arr = np.resize(frame, (224, 224, 3))
            img_arr = np.expand_dims(img_arr, axis=0)
            # print(img_arr)
            # print(img_data)
            predictions = model.predict(img_arr)[0]
            print(predictions)
            print(model_classes[np.argmax(predictions)])
            if(model_classes[np.argmax(predictions)] != 'nofight'):
                notify(cam_id)
        else:
            break
    
    cap.release()
