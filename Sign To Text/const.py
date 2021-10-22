import numpy as np
import os
from PIL import ImageFont

classes = [ 'aleff',  'bb', 'ta', 'thaa', 'jeem', 'haa', 'khaa', 'dal', 'thal', 'ra', \
         'zay' , 'seen', 'sheen',  'saad', 'dhad','taa', 'dha', 'ain', 'ghain','fa', \
          'gaaf', 'kaaf','laam', 'meem', 'nun', 'ha', 'waw','ya']

actions = np.array(['Hello', 'I', 'How are you', 'Brother','Sister','Father','Mother','Egypt','Front of'])

test_actions = np.array(['test'])
sequence_length = 30
no_sequences = 1 
offset = 0

test_label_map = {label:num for num, label in enumerate(test_actions)}
test_label_map

DATA_PATH = os.path.join('MP_Data_Videos') 
DATA_PATH_KEYPOINTS = os.path.join('MP_Data_KEYPOINTS') 


eng_ara_mapping ={
' ':' ',
"ain":'ع',
"aleff":'أ',
"bb":'ب',
"dal":'د',
"dha":'ط',
"dhad":"ض",
"fa":"ف",
"gaaf":'ق',
"ghain":'غ',
"ha":'ه',
"haa":'ح',
"jeem":'ج',
"kaaf":'ك',
"laam":'ل',
"meem":'م',
"nun":"ن",
"ra":'ر',
"saad":'ص',
"seen":'س',
"sheen":"ش",
"ta":'ت',
"taa":'ط',
"thaa":"ث",
"thal":"ذ",
"waw":'و',
"ya":"ى",
"zay":'ز',
"khaa":'خ' ,
'Hello': 'السلام عليكم',
'I': 'انا',
'How are you': 'كيف حالك ',
'Brother':'اخ ',
'Sister':' اخت',
'Father':' اب',
'Mother':' ام',
'Egypt':'مصر ',
'Front of':' امام'}

WORD_MODE = False
n_frames= 0
margin = 20
threshold= 95
allpreds=[]
frame_counter = 0
sequence = ['']
fontFile = "fonts/Sahel.ttf"
font = ImageFont.truetype(fontFile, 20)
score =0 
Record = False # Record Pose
frames_of_pose = 0
ptime = 0
seconds = 0