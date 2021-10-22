from models import *
import cv2
import numpy as np
import mediapipe as mp
import arabic_reshaper
from bidi.algorithm import get_display
from const import *

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities

# Create DataPaths for Keypoints
for action in test_actions: 
    for sequence in range(offset,offset+no_sequences):
        try: 
            os.makedirs(os.path.join(DATA_PATH_KEYPOINTS, action, str(sequence)))
        except:
            pass
        
# Create DataPaths for Videos
for action in test_actions: 
    for sequence in range(offset,offset+no_sequences):
        try: 
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
        except:
            pass

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable to Improve Perf.
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION) # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

def draw_styled_landmarks(image, results):
    # Draw face connections

    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             ) 
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             ) 
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             ) 
                             
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

def detect_chars(image,frame,hands):
    margin = 20
    img_cropped =None
    res = None
    score = 0
    if(len(hands)>0 and hands[0]['type'] == 'Right'):
        bbox = hands[0]['bbox']
        if(len(hands)>1 and hands[1]['type'] == 'Right'):
            bbox = hands[1]['bbox']
        
        pt1,pt2 = (bbox[0] - 20, bbox[1] - 20), (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20)
        img_cropped = image[bbox[1] - 20:bbox[1] + bbox[3] + 20,bbox[0] - 20:bbox[0] + bbox[2] + 20]
        if(len(img_cropped)):
            img_cropped= process_image(img_cropped)
            cv2.rectangle(frame, pt1, pt2, color = (0, 0, 0), thickness=5)
            preds = model.predict(img_cropped)[0]
            mx = np.argmax(preds)
            score = preds[mx] * 100
            res = classes[mx]
    
    return res,score,frame


def process_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224,224), interpolation= cv2.INTER_LINEAR)
    img = np.expand_dims(img, 0)
    return img


def detect_words():
    
        # Set mediapipe model 
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

        # NEW LOOP
        # Loop through actions
        for action in test_actions:
            # Loop through sequences aka videos
            for sequence in range(1):
                # Loop through video length aka sequence length
                for frame_num in range(61,91):


                    # Read feed
                    jpg_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num) + str('.jpg'))
                    # Read Frame
                    frame = cv2.imread(jpg_path)
                    # Make detections
                    image, results = mediapipe_detection(frame, holistic)
                    # NEW Export Keypoints
                    keypoints = extract_keypoints(results)
                    npy_path = os.path.join(DATA_PATH_KEYPOINTS, action, str(sequence), str(frame_num))
                    np.save(npy_path, keypoints)
                    
    test_sequences, test_labels = [], []
    for action in test_actions:
        for sequence in range(offset , offset+no_sequences):
            window = []
            for frame_num in range(61,91,1):
                res1 = np.load(os.path.join(DATA_PATH_KEYPOINTS, action, str(sequence), "{}.npy".format(frame_num)))
                lh_rh = res1[1536:]
                for z in range(2,lh_rh.shape[0],3):
                        lh_rh[z] = None
                lh_rh = lh_rh[np.logical_not(np.isnan(lh_rh))]
                window.append(lh_rh)
            test_sequences.append(window)
            test_labels.append(test_label_map[action])
    X = np.array(test_sequences)
    res = model_conv1d.predict(X)
    return actions[np.argmax(res)]

def convert_ara(sequence):
    sequence = ''.join(list(map(lambda x: eng_ara_mapping.get(x,'') , sequence)))
    reshaped_text = arabic_reshaper.reshape(sequence)   
    bidi_text = get_display(reshaped_text) 
    return  bidi_text