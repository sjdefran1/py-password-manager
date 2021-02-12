# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 13:06:28 2020

@author: sjdef
"""

#password manager using sqlite3 with 2fa using smtplib

#nec imports
import string
import random
import smtplib
import config
import sqlite3
from email.message import EmailMessage
from getpass import getpass



#generate multifactorkey
def getMFA():
    n = 5
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
    return password
#send text to my phone then calls checkCode()
def sendtext():
    mailat = config.mailat
    mail_password = config.mail_password
    
    body = getMFA()
    msg = EmailMessage()
    msg.set_content(body)
    
   
    msg['From'] = mailat
    msg['To'] = '5155054146@vtext.com'
    try:
        #send emails code 
        server_ssl = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
        server_ssl.login(mailat, mail_password)
        server_ssl.send_message(msg)
        server_ssl.quit()
        print("Email sent ->>>")
    except:
        print('Something has failed')
    
    res = checkCode(body)
    return res
    
#checks multfa code
def checkCode(passw):
    inputCheck = input('Enter code sent to (***-**5-4146) ->')
    inputCheck = inputCheck.upper()
    
    if inputCheck == passw:
        return True
    else:
        return False
    
def enterNew():
    #connect to sqlite
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    
    siteName = input('What is the site/program name? -> ')
    sitePass = input('What is the site/program password? -> ')
    
    cursor.execute("INSERT INTO pw (siteName, pass) VALUES (?, ?)", (siteName, sitePass))
    connection.commit()
    connection.close()

def retrieve():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    
    target = input('What is the site/program name? -> ')
    cursor.execute("select * from pw WHERE siteName = ?", (target,))
    results = cursor.fetchall()
    
    connection.commit()
    connection.close()
    
    return results

def viewList():
    #connect to sqlite
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    
    #select all names within siteName
    cursor.execute("SELECT siteName FROM pw")
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data

def run(a):  
    if a == True: #we passed all password tests
        runCheck = True
    else:
        runCheck = False
        
    #loop to allow user to do multiple things in this instance
    while runCheck == True: 
        #what does user want to do
        userAction = input('What would you like to do?\n(1)Enter New Passowrd\n(2)Retrieve Passowrd\n(3)View list of stored apps\nEnter 1/2/ -> ')
        #using a try except if the user accidently enters a char it doesn't crash program
        try:
            if int(userAction) == 1: #entering new pass
                enterNew()
                runagain = input('Would you like to do something else?(y/n) -> ')
                if(runagain == 'y'):
                    runCheck = True
                else:
                    runCheck = False
            elif int(userAction) == 2: #retrieving a pass
                foundRes = retrieve()
                for x in foundRes:
                    print('Site/app -> ' + x[0] + '\n' + 'Pass -> ' + x[1])
                
                runagain = input('Would you like to do something else?(y/n) -> ')
                if(runagain == 'y'):
                    runCheck = True
                else:
                    runCheck = False
            elif int(userAction) == 3:
                allNames = viewList()
                for name in allNames:
                    print('-' + name[0] + '\n')
                
            else: #entered integer that wasn't 1 or 2 or 3
                print('Incorrect command, try again')
                runCheck = True
        except ValueError: #entered a char or something that isn't a int
            print('You entered a character not 1/2/3')



#start building interface
# -----------------------------
# -
# -
# -
# -
# -----------------------------
mk = config.master
a = False

#check mainkey

while a == False:
    mk_attempt = getpass('Enter Main PASS: ')
    if mk_attempt == mk:
         a = sendtext()
    else:
        print('Access denied')
        a = False
   
run(a)





    








    

