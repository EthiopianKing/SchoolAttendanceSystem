import qrcode   
import time
import datetime
import random
import string
import cv2
from fileinput import filename
import os
import smtplib
import imghdr
from email.message import EmailMessage
import numpy as np
from pyzbar.pyzbar import decode

student_list =[]
random_number = []
email_list = []
time_list = []
location_list = []
file_list = []

def email():
    q = 0
    tday = datetime.date.today()
    for x in email_list:
        msg = EmailMessage()
        msg['Subject'] = 'QR code for the day'
        msg['From'] = ""
        msg['To'] = x
        msg.set_content("Dear "+student_list[q]+', this is your QR code for the day. Please scan at QR code station located near teacher\'s desk. This QR code is only viable for the date '+str(tday))
        with open(file_list[q], "rb") as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
        msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=f.name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("", "")
            smtp.send_message(msg)
        q=q+1

def expand():
    name = input("What is the student's name?(Firstname Lastname)\n")
    email = input("What is student's email?\n")
    num = random.randint(1000,10000)
    r = name+"-"+str(num)
    email_list.append(email)
    student_list.append(name)
    random_number.append(r)
    time_list.append("_")
    location_list.append("_")


    img = qrcode.make(r)
    k = str(random.randint(1,100000000))
    imgName = name + "-" +k +".jpeg"
    file_list.append(imgName)
    img.save(imgName)

x = 1
while x == 1:
    user = input("What would you like to do?\nexpand lists, email codes, or end\n")
    if user == "expand lists":
        expand()
    elif user == "email codes":
        email()
    elif user == "end":
        x = 2
