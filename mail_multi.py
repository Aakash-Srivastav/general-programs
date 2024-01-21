"""
This is Task Specific Code created for a particular usecase.
This can send maultiple mails.
"""


import smtplib 
import pandas as pd
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from datetime import date

file_path_name = input('Enter file path to get dispatch data with extension : ')

def variables(file_path):
    """
    This function will store all the variables in a function

    """
    global months_dic
    global dataframe
    global receiver_mail
    global sender_mail
    global sender_pass
    global folder_path
    global subject
    global body
    global month
    global result_dict

    months_dic = {'JAN': 1,'FEB': 2,'MAR': 3,'APR': 4,'MAY': 5,'JUN': 6,'JUL': 7,'AUG': 8,'SEP': 9,'OCT': 10,'NOV': 11,'DEC': 12}
    dataframe = pd.read_excel(rf'{file_path}')
    receiver_mail = list(dict.fromkeys(list(dataframe['Mail'])))
    sender_mail = input('Enter Sender Mail ID : ')
    sender_pass = input('Enter Sender Mail ID Password : ')
    folder_path = input('Enter Dispatch Folder Path : ')
    subject = 'Subject'
    body = 'Body'
    month = input('Enter Data Month like Aug : ')
    result_dict = dataframe_to_dict(dataframe)

def dataframe_to_dict(df):
    """
    This function will store the dataframe in a dictionary with all the unique E-Mail as Key 
    and all the data as there respective Values.
    """

    result_dict = {}

    for col, row in df.iterrows():
        key = row['Mail']
        values = row.drop('Mail').to_dict()
        
        # If the key already exists, append the values to the existing list
        if key in result_dict:
            result_dict[key].append(values)
        else:
            result_dict[key] = [values]
    return result_dict

def message(sender_mail,receiver_mail,subject,month,body,folder_path,result_dict,months_dic,session):

    """
    This function create the message and will also support files with extenxion '.zip' and '.rar' 
    """

    for elem in range(len(receiver_mail)):
        attachment_count = 0
        zip_list = ['zip','rar']
        msg = MIMEMultipart() 
        msg['From'] = sender_mail
        msg['To'] = receiver_mail[elem]
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain')) 
        for num in range(len(result_dict[receiver_mail[elem]])):
            if int(result_dict[receiver_mail[elem]][num]['To_Year'])>=int(date.today().year):
                if int(months_dic.get(result_dict[receiver_mail[elem]][num]['To_Month'].upper()[:3]))>=int(months_dic.get(month.upper()[:3])):
                    if result_dict[receiver_mail[elem]][num]['File'].split(".")[-1].lower() not in zip_list:
                        attachment_name = rf"{folder_path}\{result_dict[receiver_mail[elem]][num]['File']}.xlsx"                
                    else:
                        attachment_name = rf"{folder_path}\{result_dict[receiver_mail[elem]][num]['File']}"
                    attachment = open(attachment_name, "rb")
                    app = MIMEBase('application', 'octet-stream')
                    app.set_payload((attachment).read())
                    encoders.encode_base64(app)
                    app.add_header('Content-Disposition', "attachment; filename= %s" % attachment_name.split("\\")[-1]) 
                    msg.attach(app)
                    attachment_count = attachment_count+1
        text = msg.as_string()
        if attachment_count > 0:
            session.sendmail(sender_mail, receiver_mail[elem], text)

def session_func(path):

    variables(file_path=path)

    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls()
    session.login(sender_mail, sender_pass)

    message(sender_mail,receiver_mail,subject,month,body,folder_path,result_dict,months_dic,session)
    
    session.quit()

if __name__ == "__main__":
    session_func(path=file_path_name)

