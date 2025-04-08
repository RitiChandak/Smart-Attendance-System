import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

from sms import send_sms
from voicetts import text_to_speech
from funct import assure_path_exists,check_haarcascadefile,clear,clear2,clear3
from password import save_pass,change_pass
from getimages import  getImagesAndLabels,TrainImages

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)
    
def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')
        
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations  : ' + str(ID[0]))
    
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME','','CONTACT NUMBER']
    assure_path_exists("FacultyDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("FacultyDetails\FacultyDetails.csv")
    if exists:
        with open("FacultyDetails\FacultyDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("FacultyDetails\FacultyDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    contactnumber= (txt3.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name,'',contactnumber]
        with open('FacultyDetails\FacultyDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("FacultyDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Some Data is Missing', message='Click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time','','Contact Number']
    exists1 = os.path.isfile("FacultyDetails\FacultyDetails.csv")
    if exists1:
        df = pd.read_csv("FacultyDetails\FacultyDetails.csv")
    else:
        mess._show(title='Details Missing', message='Faculty details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 70):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                cnc = df.loc[df['SERIAL NO.'] == serial]['CONTACT NUMBER'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                cc=str(cnc)
                cc=cc[3:-3]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp),'',cc]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
        if __name__ == "__main__":
            to_number = "+"+str(cnc)
            print(to_number)
            message_body = 'Thank you !  Your Attendance have been registered'
            send_sms(to_number, message_body)
    csvFile1.close()
    cam.release()
    if __name__ == "__main__":
        spevok = "Thank you! your attendance has been registered"
        text_to_speech(spevok, rate=130)
    cv2.destroyAllWindows()

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

window = tk.Tk()
window.geometry("1280x1080")
window.resizable(True,False)
window.title("Attendance System")

frame1 = tk.Frame(window, bg="#b0c4de")
frame1.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8)

frame2 = tk.Frame(window, bg="#b0c4de")
frame2.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8)

message3 = tk.Label(window, text="Smart Attendance System" ,fg="white",bg="#4682b4" ,width=55 ,height=1,font=('comic', 29, ' bold '))
message3.place(x=10, y=10)

def show_frame2():
    frame1.place_forget()  # Hide Frame 1
    frame2.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8)  # Show Frame 2

frame2.place_forget()

def show_frame1():
    frame2.place_forget()  # Hide Frame 2
    frame1.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8)

datef = tk.Label(frame1, text = day+"-"+mont[month]+"-"+year, fg="#00008B",bg="#b0c4de" ,width=15 ,height=1,font=('comic', 22, ' bold '))
datef.place(x=90, y=100)

clock = tk.Label(frame1 ,fg="#00008B",bg="#b0c4de" ,width=25 ,height=1,font=('comic', 22, ' bold '))
clock.place(x=10, y=150)
tick()

head2 = tk.Label(frame2, text="                               New Registrations                       ", fg="white",bg="#A0522D" ,font=('comic', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                               Already Registered                       ", fg="white",bg="#A0522D" ,font=('comic', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="#00008B"  ,bg="#b0c4de" ,font=('comic', 17, ' bold ') )
lbl.place(x=80, y=55)
txt = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="#00008B"  ,bg="#b0c4de" ,font=('comic', 17, ' bold '))
lbl2.place(x=80, y=140)
txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt2.place(x=30, y=173)

lbl3 = tk.Label(frame2, text="Contact Number",width=20  ,fg="#00008B"  ,bg="#b0c4de" ,font=('comic', 17, ' bold '))
lbl3.place(x=80, y=225)
txt3 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt3.place(x=30, y=258)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,fg="#00008B",bg="#b0c4de"   ,width=39 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message1.place(x=7, y=338)

message = tk.Label(frame2, text="" ,fg="black",bg="#b0c4de"   ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=7, y=500)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="#00008B"  ,bg="#b0c4de"  ,height=1 ,font=('comic', 17, ' bold '))
lbl3.place(x=100, y=200)

res=0
exists = os.path.isfile("FacultyDetails\FacultyDetails.csv")
if exists:
    with open("FacultyDetails\FacultyDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('comic', 29, ' bold '),menu=filemenu)

entrymenu = tk.Menu(menubar, tearoff=0)
entrymenu.add_command(label='New Entry', command=show_frame2)
entrymenu.add_command(label='Take Attendance', command=show_frame1)
menubar.add_cascade(label='Entry', font=('comic', 29, ' bold '), menu=entrymenu)

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(250,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="white"  ,bg="#cd5c5c"  ,width=11 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="white"  ,bg="#cd5c5c"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=335, y=172)
clearButton3 = tk.Button(frame2, text="Clear", command=clear3  ,fg="white"  ,bg="#cd5c5c"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton3.place(x=335, y=258)
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="#483d8b"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImg.place(x=30, y=400)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="#483d8b"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trainImg.place(x=30, y=480)

trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="white"  ,bg="#483d8b"  ,width=35  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="white"  ,bg="#cd5c5c"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=30, y=550)

window.configure(menu=menubar)
window.mainloop()
