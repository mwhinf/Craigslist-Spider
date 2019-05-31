import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sqlite3 as lite
import datetime
import pytz
from twilio.rest import Client
import re


def buildBase():

    resultsList = []
    checkList = []

    conn = lite.connect('/Users/michaelwhinfrey/desktop/scrapyapp/CraigslistSpider/boards.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS checkTable (ID INTEGER PRIMARY KEY, \
                                                    Temp TEXT );")

    cursor = cur.execute("SELECT ID, ImageURL, Message, ImgHash from resultsTable")
    
    for row in cursor:
        resultsList.append({'ID': row[0], 'Message': row[2], 'ImgHash': row[3]})

    info = cur.execute("SELECT ID, Temp from checkTable")

    for row in info:
        checkList.append({'Temp': 'Temp'})

    print('\n')
    print('*****************')
    print('Results List: ' + str(len(resultsList)))
    print('Check List: ' + str(len(checkList)))
    print('*****************')
    print('\n')

    r = len(checkList)+1

    while r <= len(resultsList):

        cur.execute("INSERT INTO checkTable (Temp) \
                VALUES('ONE')")

        conn.commit()

        r += 1


def resetTables():
    conn = lite.connect('/Users/michaelwhinfrey/desktop/scrapyapp/CraigslistSpider/boards.db')
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS resultsTable")
    cur.execute("DROP TABLE IF EXISTS checkTable")
    conn.commit()


def textFunc():
    accountSID = 'ACbebd1021a7922ea89230ac4f8b804a5f'
    authToken = 'afd3069f2703dcda418f4ad22bd15f78'

    twilioCli = Client(accountSID, authToken)

    myTwilioNumber = '+15109240854'
    myCellPhone = '+13104998149'

    message = twilioCli.messages.create(body='Hello der fren', from_=myTwilioNumber, to=myCellPhone)


def alertFunc(chkEmail, chkText, emailadd, phonenum):

    eAlert = chkEmail
    tAlert = chkText
    emailAdd = emailadd
    phoneNum = phonenum

    htmlBody = ''
    j = 1
    resultsList = []
    checkList = []

    conn = lite.connect('/Users/michaelwhinfrey/desktop/scrapyapp/CraigslistSpider/boards.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS checkTable (ID INTEGER PRIMARY KEY, \
                                                    Temp TEXT );")

    cursor = cur.execute("SELECT ID, ImageURL, Message, ImgHash from resultsTable")

    for row in cursor:
        resultsList.append({'ID': row[0], 'ImageURL': row[1], 'Message': row[2], 'ImgHash': row[3]})

    info = cur.execute("SELECT ID, Temp from checkTable")

    for row in info:
        checkList.append({'Temp': 'Temp'})

    print('\n')
    print('*****************')
    print('Results List: ' + str(len(resultsList)))
    print('Check List: ' + str(len(checkList)))
    print('*****************')
    print('\n')

    r = len(checkList)+1
    k = -1

    while r <= len(resultsList):

        cur.execute("INSERT INTO checkTable (Temp) \
                VALUES('ONE')")

        conn.commit()

        filepath = '/Users/michaelwhinfrey/desktop/scrapyapp/CraigslistSpider/CraigslistSpider/outputImages/full/' + \
            resultsList[k]['ImgHash']

        today = datetime.datetime.now(pytz.utc) - datetime.timedelta(hours=7)

        # send text message
        accountSID = 'ACbebd1021a7922ea89230ac4f8b804a5f'
        authToken = 'afd3069f2703dcda418f4ad22bd15f78'

        twilioCli = Client(accountSID, authToken)

        myTwilioNumber = '+15109240854'
        myCellPhone = '+' + phoneNum

        textBody = re.sub('<br>', '', resultsList[k]['Message'])

        message = twilioCli.messages.create(
            body='- - - - - - - - - - \n\n\n' + textBody, from_=myTwilioNumber, media_url=resultsList[k]['ImageURL'], to=myCellPhone)

        # set up email account
        MY_ADDRESS = 'pythonmail310@gmail.com'
        PASSWORD = 'pythonmail'

#s = smtplib.SMTP(host='smtp.gmail.com', port=587)
#s.starttls()
#s.login(MY_ADDRESS, PASSWORD)

        msg = MIMEMultipart()       # create a message

        # set up the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = emailAdd
        msg['Subject'] = "LongboardPost " + \
            str(resultsList[k]['ID']) + " -- " + str(today.strftime('%X'))

        # print(filepath)
        #attachment = open(filepath, 'rb')
        #msgImage = MIMEImage(attachment.read())
        #attachment.close()
        #contID = '<image' + str(j) + '>'

        print("Post " + str(j) + " sent.")
        print('\n')

#msgImage.add_header('Content-ID', contID)
#msg.attach(msgImage)
        htmlBody = """<p>""" + resultsList[k]['Message'] + """<br>
                        </p>
                        <img src="cid:image""" + str(j) + """">"""

        r += 1
        k -= 1
        j += 1

        # build & attach final message
        msg.attach(MIMEText("""\
        <html>
            <body>""" + htmlBody +

                            """</body>
        </html>
        """, 'html'))

        # send email
        text = msg.as_string()
        #s.sendmail(MY_ADDRESS, 'mwimf123@gmail.com', text)

        # Terminate the SMTP session and close the connection
#s.quit()
