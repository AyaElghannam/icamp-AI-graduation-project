from anime import make_anime_transition
from maps import *
import os, glob
import asyncio
import cv2
import argparse


#parser = argparse.ArgumentParser(description='Process sentence.')
#parser.add_argument('--input', action='store', type=str, required=True)
#args = parser.parse_args()

with open('input.txt',encoding='utf-8') as f:
    lines = f.readlines()
    
#print(lines)
ss = [file_move.get(eng_ara.get(w)) for w in lines[0].split()]
print(ss)

sentence = ','.join(ss)
f.close()
#print(sentence)

Status = None
nframes = make_anime_transition(ss)#file_move['hello'])#,file_move['live'],file_move['egypt'])

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))


    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main(nframes):
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = str(nframes)

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.3', 8888)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main(nframes))





# Save anim to disk
# get all Filenames of Frames
path = "./rendering/*.jpg"
files = sorted(glob.glob(path), key= lambda x : int(x.split("\\")[1][:-4]) )

# load all Frame in This Array
img_array = []
for filename in files:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
#Output Path
vid_path = './outputs/output.mp4'
out = cv2.VideoWriter(vid_path,cv2.VideoWriter_fourcc(*'XVID'), 10, size)

# Write Video
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
  

## Displaying
cap = cv2.VideoCapture('./outputs/output.mp4')
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == True:
        frame = cv2.resize(frame, (1344,756), interpolation =cv2.INTER_AREA)
        # Display the resulting frame
        winname = "Signara"
        cv2.namedWindow(winname)        # Create a named window
        cv2.moveWindow(winname, 0,0)  # Move it to (40,30)
        cv2.imshow(winname, frame)
        

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else: 
        break

    #to Slow Down The FPS
    cv2.waitKey(50)
while(1):
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

