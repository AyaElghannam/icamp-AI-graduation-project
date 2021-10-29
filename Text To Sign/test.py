import tkinter as tk
import subprocess
import os,shutil
from spell_checker import spell_checker
from ner import ner_recognizer
from PIL import ImageTk, Image

def save():
    
    file_name = entry.get()
    with open('input' + '.txt', 'w',encoding='utf-8') as file_object:
        file_object.write(file_name)   # it is unclear if writing the file_name in the newly created file is really what you want.

    try:
        shutil.rmtree('./rendering')
        os.remove('./outputs/output.mp4')
    except:
        pass
    subprocess.call("python main.py", shell=True)

def prepocess():
    text = entry.get()
    processed = spell_checker(text)
    processed = ner_recognizer(processed)
    processed_text = []
    for key in processed.keys():
        if(processed[key] != 'B-PERS'):
            processed_text.append(key)
        else:
            for char in key:
                processed_text.append(char)

    
    entry_field_variable2.set(' '.join(processed_text))



if __name__ == '__main__':
    top = tk.Tk()
    top.geometry('300x300')

    img = ImageTk.PhotoImage(Image.open("logo.png"))
    panel = tk.Label(top, image = img)
    panel.pack(side = "top", fill = "both", expand = "yes")


    top.title('Signara: Text To Sign')
    entry_field_variable = tk.StringVar()
    entry = tk.Entry(top, textvariable=entry_field_variable,width= 60)
    entry.pack()

    entry_field_variable2 = tk.StringVar()
    entry2= tk.Entry(top, textvariable=entry_field_variable2,width= 60)
    entry2.pack()
    tk.Button(top, text="preprocess", command=prepocess).pack()
    tk.Button(top, text="Anime", command=save).pack()

    
    top.mainloop()

