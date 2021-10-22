from PIL import Image
from PIL import ImageDraw
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time,copy
from models import *
from helper import *
from const import *

detector = HandDetector(mode=False, maxHands=2, detectionCon=0.9, minTrackCon=0.9)

# define a video capture object
vid = cv2.VideoCapture(3)
width  = vid.get(3)   # float `width`
height = vid.get(4)  # float `height`

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.2) as holistic:
    while(True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()  
        if(not ret):
            continue
        # Copy Original Image without any Draw
        img = copy.deepcopy(frame)
        # Detect Hands , Drawn Frame
        hands_,frame = detector.findHands(frame, flipType=False,draw=True)

        # New Word Option
        frame, _bbox_newword = cvzone.putTextRect(frame, "New Word", [116, 50], 2, 2, offset=5, border=5,colorR=(61,33,21),
                                     colorB = (17,163,252))
        # Switch Between Words and Chars Mode
        frame, _bbox_switch = cvzone.putTextRect(frame, "Switch", [412, 50], 2, 2, offset=5, border=5,colorR=(61,33,21),
                                     colorB = (17,163,252))
        # To Show Current Mode
        frame, _ = cvzone.putTextRect(frame, 'Current Mode: ' + ['CharMode','WordMode'][WORD_MODE], [110, 20], 2, 2, 
                                      offset=2, border=0,colorR=(29,29,29), colorB = (29,29,29),colorT= (0,0,255))
        
        # To delete predication
        frame, _bbox_backspace = cvzone.putTextRect(frame, "BackSpace", [280, 340], 1, 1, offset=5, border=5,colorR=(61,33,21),
                                     colorB = (17,163,252))
        

        
        
        if (hands_ and n_frames%15==0):
            n_frames = 0
            lmList = hands_[0]['lmList']
            cursor = lmList[8]
            length, info = detector.findDistance(lmList[8], lmList[12])

            #print(length)            
            if( (_bbox_switch[0]<cursor[0]<_bbox_switch[2]) and (_bbox_switch[1]<cursor[1]<_bbox_switch[3]) and length< 20):
                WORD_MODE = [True,False][WORD_MODE]
                if(sequence[-1] != ' '):
                    sequence.append(' ')
                #print(WORD_MODE)



        
            # if Click on Backspace
            if( (_bbox_backspace[0]<cursor[0]<_bbox_backspace[2]) and (_bbox_backspace[1]<cursor[1]<_bbox_backspace[3]) and length< 20):
                if(n_frames%15==0):

                    if(len(sequence) > 1):
                        sequence.pop()




        if(WORD_MODE):
            if( (not Record and _bbox_newword[0]<cursor[0]<_bbox_newword[2]) and (_bbox_newword[1]<cursor[1]<_bbox_newword[3]) and length< 20):               
                Record = True
                frames_of_pose = 0
                seconds = 3
                print('waitng')
                if(sequence[-1] != ' '):
                    sequence.append(' ')

            if(Record):
                # Waiting 3 Seconds
                if((seconds != 0 ) and frames_of_pose % 20 == 0 ):
                    # each second get into this Function
                    seconds -= 1
                    
                # Display Seconds on Screen
                if((seconds != 0) and (frames_of_pose<= 60)):
                    frame, _ = cvzone.putTextRect(frame, str(seconds) , [0, int(height-300)], 5, 1, 
                                      offset=2, border=0,colorR=(29,29,29), colorB = (29,29,29),colorT= (0,0,255))

                # Record Video Now
                if((seconds == 0) and (60<frames_of_pose <=90)):
                    jpg_path = os.path.join(r'MP_Data_Videos\test\0\\', str(frames_of_pose) + str('.jpg'))
                    frame, results = mediapipe_detection(img, holistic)
                    draw_styled_landmarks(frame, results)
                    cv2.imwrite(jpg_path,img)
                    cv2.waitKey(1)

                # Report it's Done
                elif((seconds == 0) and (frames_of_pose >90)):
                    Record = False
                    ress = detect_words()
                    sequence.append(ress)
                    print("Done")



        else:
            # Each n_frames predict
            if(n_frames%2==0):
                # detect Chars function is return > the predicted Character, Score, Drawn Frame with Black Box
                res , score , frame = detect_chars(image= img,frame=frame,hands=hands_)
                # append this results to allPreds
                allpreds.append(res)
            # Show The Score for Each Frame
            cv2.putText(frame, 'score = %.1f' % (float(score)), (0,468), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255))
            # if last 10frames*n_frames Same, Save it to Sequence
            if(res and len(set(allpreds[-10:])) == 1 and score > threshold):
                # to Don't Write successive Same Char 
                if(sequence[-1] != res):
                    sequence.append(res)

        
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        bidi_text = convert_ara(sequence)
        draw.text((250, 400), bidi_text, (255,255,255),font =font,align = 'center')
        frame = np.array(img_pil)

        
        
        #Update Frames
        n_frames += 1
        frames_of_pose +=1
        
        # Display FPS
        ctime = time.time()
        fps = 1/(ctime-ptime)
        cv2.putText(frame,f'FPS: {int(fps)}', (0,12), 
                       cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 2, cv2.LINE_AA) 
        ptime = ctime
        
        
        # insert Logo
        logo = cv2.imread('logo.png',cv2.IMREAD_UNCHANGED)
        cv2.imshow('frame', frame)

        # desired button of your choice
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


    ##After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()