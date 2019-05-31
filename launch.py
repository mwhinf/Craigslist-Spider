import scrapydo
import logging
import os
import time
from CraigslistSpider.spiders import CraigSpider
from functionFile import alertFunc
from functionFile import buildBase
from functionFile import resetTables
from Tkinter import *
import ttk
import re


def clicked():

    scrapydo.setup()

    # set up duration of crawl in hours
    duration = (daysBTN.get())*24 + hoursBTN.get()

    timer = duration*20

    os.environ['SCRAPY_SETTINGS_MODULE'] = 'CraigslistSpider.settings'

    scrapydo.default_settings.update({
        'LOG_LEVEL': 'DEBUG',
        'CLOSESPIDER_PAGECOUNT': 10,
    })

    logging.basicConfig(level=logging.DEBUG)
    logging.root.setLevel(logging.INFO)

    priceLimits = [priceMinBox.get(), priceMaxBox.get()]

    locationFull = locationBox.get()
    locationLower = locationFull.lower()
    location = re.sub(" ", "", locationLower)

    baseURL = 'https://' + location + '.craigslist.org/search/sss?sort=date&query='

    keyString = keyBox.get()
    keyList = keyString.split()

    for key in keyList:
        baseURL += key + '+'

    else:
        URL = baseURL[0:-1]
        if chkState.get() == True:
            URL += '&sort=rel&hasPic=1&postedToday=1'
        if priceLimits[0]:
            URL += '&min_price=' + str(priceLimits[0])
        if priceLimits[1]:
            URL += '&max_price=' + str(priceLimits[1])

    base = scrapydo.run_spider(CraigSpider.LongboardsSpider, settings={
                               'CLOSESPIDER_ITEMCOUNT': 500}, start_url=URL)

    time.sleep(3)

    buildBase()

    j = 0

    while j < timer:
        items = scrapydo.run_spider(CraigSpider.LongboardsSpider, settings={
                                    'CLOSESPIDER_ITEMCOUNT': 500}, start_url=URL)

        time.sleep(5)

        chkEmail = chkStateEmail.get()
        chkText = chkStateText.get()
        phonenum = '13104998149'
        emailadd = 'mwimf123@gmail.com'

        alertFunc(chkEmail, chkText, emailadd, phonenum)

#print('5 minutes')
#time.sleep(50)
#print('4 minutes')
#time.sleep(60)
#print('3 minutes')
#time.sleep(60)
#print('2 minutes')
#time.sleep(60)
        print('1 minute')
        time.sleep(60)

        j += 1

    resetTables()


# setup app window
window = Tk()
window.geometry('1000x500')


# create widgets
window.title("EarlyBird")
title = Label(window, text="EarlyBird", bg="#98fb98", font=("Ariel Bold", 30))
searchLabel = Label(window, text="Search:", font=("Ariel", 16, "bold"))
locationBox = ttk.Combobox(window)
locationBox['values'] = ('Los Angeles', 'Orange County', 'San Diego')
locationBox.current(0)
keyBox = Entry(window, width=55)
searchBTN = Button(window, text="Find Deals", command=clicked)
priceMinLabel = Label(window, text="Min. Price:")
priceMinBox = Entry(window, width=10)
priceMaxLabel = Label(window, text="Max. Price:")
priceMaxBox = Entry(window, width=10)
chkState = BooleanVar()
chkState.set(True)
hasPicBTN = Checkbutton(window, text="has pic", var=chkState)
durationLabel = Label(window, text="Duration:")
hoursBTN = Spinbox(window, from_=0, to=24, width=5)
hoursLabel = Label(window, text="Hours")
daysBTN = Spinbox(window, from_=0, to=7, width=5)
daysLabel = Label(window, text="Days")
emailLabel = Label(window, text='Email Alerts:')
emailBox = Entry(window, width=25)
phoneLabel = Label(window, text='Text Alerts:')
phoneBox = Entry(window, width=25)
chkStateText = BooleanVar()
chkStateText.set(True)
sendTextBTN = Checkbutton(window, text="Send Text Alert", var=chkStateText)
chkStateEmail = BooleanVar()
chkStateEmail.set(True)
sendEmailBTN = Checkbutton(window, text="Send Email Alert", var=chkStateEmail)

# place widgets
title.grid(column=0, row=0)
locationBox.grid(column=1, row=2, pady=(150, 30), padx=(5, 0))
searchLabel.grid(column=0, row=2, pady=(150, 30), sticky="e")
keyBox.grid(column=2, row=2, pady=(150, 30), padx=(3, 0), columnspan=15)
searchBTN.grid(column=17, row=2, pady=(150, 30), padx=(3, 0))
priceMinLabel.grid(column=1, row=4, sticky="e")
priceMinBox.grid(column=2, row=4, sticky="w")
priceMaxLabel.grid(column=1, row=5, sticky="e")
priceMaxBox.grid(column=2, row=5, sticky="w")
hasPicBTN.grid(column=3, row=4)
durationLabel.grid(column=5, row=3)
hoursBTN.grid(column=5, row=4)
hoursLabel.grid(column=6, row=4, sticky="w")
daysBTN.grid(column=5, row=5)
daysLabel.grid(column=6, row=5, sticky="w")
emailLabel.grid(column=1, row=6, pady=(50, 20), sticky="e")
emailBox.grid(column=2, row=6, pady=(50, 20), sticky="w")
phoneLabel.grid(column=1, row=7, sticky="e")
phoneBox.grid(column=2, row=7, sticky="w")
sendEmailBTN.grid(column=4, row=6, pady=(50, 20), sticky='w')
sendTextBTN.grid(column=4, row=7, sticky='w')


window.mainloop()
