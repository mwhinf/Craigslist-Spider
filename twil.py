from twilio.rest import Client
from functionFile import resetTables


def textFunc():
    accountSID = 'ACbebd1021a7922ea89230ac4f8b804a5f'
    authToken = 'afd3069f2703dcda418f4ad22bd15f78'

    twilioClient = Client(accountSID, authToken)

    myTwilioNumber = '+16572422061'
    myCellPhone = '+13104998149'

    post = 'https://images.craigslist.org/00i0i_htzxW1Xsuz1_300x300.jpg'

    message = twilioClient.messages.create(
        body='- - - - - - - - - - \n\n\n' + post + '\n\nAhhh', from_=myTwilioNumber, media_url='https://i.imgur.com/yOyG5r4.jpg', to=myCellPhone)


resetTables()
