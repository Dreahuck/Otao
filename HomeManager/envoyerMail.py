#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 18:45:46 2020

@author: Mymac
"""

import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


class MailInfo:
  def __init__(self):
    self.mdpMail = settings.EMAIL_PSWD
    self.email = settings.EMAIL_LOGIN
    self.port = "465"



mailInfo = MailInfo()

def envoieMailAvecPJ_devAwnTest(receiver_email,subject,body):
    infoMail = MailInfo()

    sender_email = infoMail.email
    password = infoMail.mdpMail

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "Carte20.jpg"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
        )
    
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)



def envoieMailAvec_devAwnTest(receiver_email,message):
    infoMail = MailInfo()

    sender_email = infoMail.email
    password = infoMail.mdpMail
    port = infoMail.port

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


    

def envoieMailEtPJ(sender_email,password,receiver_email,subject,body,filename):

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
        )
    
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", MailInfo().port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def envoieMailAvecObjet_devAwnTest(receiver_email,subject,body, html):
    infoMail = MailInfo()

    sender_email = infoMail.email
    password = infoMail.mdpMail
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(html, "html"))
    text = message.as_string()
    print('Lancement envoi mail par SMTP....')
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    print('Mail envoyé')




def envoieMailNouvelleTache(mailDestinataire, sujet, idTache, personneOrigine, commentaire):
    html = """\
    <html>
    <head></head>
    <body>
        <p>Bonjour, <br>
           """ + personneOrigine + """ vient de te créer une tâche ! <br>
         Tu peux la consulter <a href='http://192.168.1.13:8000/HomeManager/detailTache/"""+ str(idTache) + """'>ici</a> 
        </p>
        <br>
        <p> Commentaire sur la tâche : </p> <br> <p>
        """ + commentaire + """ </p>
    </body>
    </html>
    """
    return envoieMailAvecObjet_devAwnTest(mailDestinataire , sujet,' ',html)



