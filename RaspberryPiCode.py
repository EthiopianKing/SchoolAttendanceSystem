import qrcode   
import time
from datetime import datetime
import random
import string
import cv2
from fileinput import filename
from openpyxl import Workbook
import os
import smtplib
import imghdr
from email.message import EmailMessage
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

student_list =[]
adminEmail = ""
time_list = []
location_list = []
file_list = []


def scan():
    time = int(now.strftime("%H%M"))
    x = 0
    myData=" "
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode("utf-8")
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        extract(myData)
    cv2.waitKey(1)
    x=x+1

def email():
    msg = EmailMessage()
    msg['Subject'] = '321 report'
    msg['From'] = "projectwhereabouts2022@gmail.com"
    msg['To'] = adminEmail
    msg.set_content("Dear Admin, this is your report code for class 321 at "+ now.strftime("%H:%M")+".")
    with open("321_Attendance.xlsx", "rb") as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=f.name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("projectwhereabouts2022@gmail.com", "e2W!+7@Z")
        smtp.send_message(msg)

def extract(qr):
    n = 0
    new = ""
    if "-" in qr:
        for x in qr:
            if qr[n] != "-":
                new = new + qr[n]
                n = n+1
    if new not in student_list:
        student_list.append(new)
        location_list.append("321")
        time_list.append(now.strftime("%H:%M"))
        print(student_list)
        print(location_list)
        print(time_list)


x = 0
now = datetime.now()

while x != 46:
    if x < 45:
        scan()
        time.sleep(1)
        x+=1
    elif x == 45:
        print("Done Scanning!")
        x = x+1
        time.sleep(1)

def create_workbook(path):
    workbook = Workbook()
    sheet = workbook.active
    a = 2
    b = 2
    c = 2
    for x in student_list:
        sheet["A"+str(a)] = x
        a+=1
    for x in time_list:
        sheet["B"+str(b)] = x
        b+=1
    for x in location_list:
        sheet["C"+str(c)] = x
        c+=1
    sheet["A1"] = "Name"
    sheet["B1"] = "Time"
    sheet["C1"] = "Room Number"
    workbook.save(path)

if __name__ == "__main__":
    create_workbook("321_Attendance.xlsx")
    email()
