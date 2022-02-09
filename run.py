import jinja2
from os import getcwd, environ
from tkinter.filedialog import askopenfilename
import csv
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

templateLoader = jinja2.FileSystemLoader(searchpath="C:/")

templateEnv = jinja2.Environment(loader=templateLoader)


def getTemplateFile():
    curr_file = askopenfilename(
        filetypes=[('Template Files (*.jinja)', '*.jinja')],
        initialdir=getcwd(),
        title='Select template'
    )
    return curr_file


def getCSVData():
    curr_file = askopenfilename(
        filetypes=[('Template Files (*.csv)', '*.csv')],
        initialdir=getcwd(),
        title='Select data'
    )

    with open(curr_file, mode='r', encoding="utf-8") as data_file:
        reader = csv.reader(data_file)
        rows = [row for row in reader]
        keys = rows[0]
        data = rows[1:]
        assert 'email' in keys, 'The email key is required'
        templateEntries = []
        for entry in data:
            currVars = dict()
            assert len(entry) >= len(keys), 'One of the rows of data has missing data'
            for i in range(0, len(keys)):
                currVars[keys[i]] = entry[i]
            templateEntries.append(currVars)
        return templateEntries


def sendEmails(templateFile, variables):
    def templateLoader(var):
        template = templateEnv.get_template(templateFile)
        text = template.render(var)
        return text

    htmlDatas = []
    for entry in variables:
        htmlDatas.append(templateLoader(entry))

    if len(htmlDatas) < 1:
        return True

    # Initialise mail server
    emailSender = environ['EMAIL_SENDER']
    emailPassword = environ['EMAIL_PASSWORD']
    emailServer = environ.get('EMAIL_SERVER','smtp.office365.com')
    mailserver = smtplib.SMTP(emailServer, 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(emailSender, emailPassword)
    subject = input("Please enter an email subject (not templated):")

    # Send sample email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = emailSender
    msg['To'] = emailSender
    text = htmlDatas[0]
    part = MIMEText(text, 'html')
    msg.attach(part)
    mailserver.sendmail(emailSender, emailSender, msg.as_string())
    print("Sent sample email to " + emailSender)
    reply = input("Please view check sample email and press Y if this looks okay (Y/N):")
    if reply.upper() != "Y":
        print("Email sending cancelled")
        return

    emails = [entry['email'] for entry in variables]
    print('Sending emails to:', emails)

    for idx, email in enumerate(emails):
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = emailSender
            msg['To'] = email
            text = htmlDatas[idx]
            part = MIMEText(text, 'html')
            msg.attach(part)
            # Adding a newline before the body text fixes the missing message body
            mailserver.sendmail(emailSender, email, msg.as_string())
            print('Successfully sent to ' + email)
        except Exception as e:
            print('Failed to send to ' + email + " because " + e)

    mailserver.quit()


if __name__ == '__main__':
    load_dotenv()
    templateFile = getTemplateFile()
    data = getCSVData()
    sendEmails(templateFile, data)
