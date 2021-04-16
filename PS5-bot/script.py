import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import os
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv



class CheckStock:

    def __init__(self):
        self.browser = webdriver.Firefox()
        # go to target's URL for the PS5
        self.target()
        # self.bestbuy()
        # self.send_sms("HI, this is a test")



        # close the process
        # self.browser.close()

    def target(self):
        # get the current time for status updates
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # self.browser.get("https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596#lnk=sametab")
        self.browser.get("https://www.target.com/p/dualsense-wireless-controller-for-playstation-5/-/A-81114477") # controller link
        time.sleep(5) # wait 5 seconds

        # try:
        stock = self.browser.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[3]/div[1]/div/div/div')
        in_stock = stock.get_attribute('innerHTML') # should say 'Sold Out'

        if in_stock == "Sold out":
            print("Status: Sold Out \n"
                  "Last Checked: "+ current_time )
            time.sleep(15)
            self.browser.refresh()
            self.target()

        else:
            # the PS5 is in stock
            # print("Status: IN STOCK \n"
            #       "Last Checked: "+ current_time )

            msg = ("Status: PS5 is IN STOCK @ Target\n"
            "Last Checked: "+ current_time +"\n" + self.browser.current_url)

            self.send_sms(msg)
            self.browser.close()









        # have to add condition if it is IN STOCK

    def send_sms(self, msg ):
        load_dotenv(find_dotenv())
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        my_phone = os.environ.get("MY_PHONE")
        auth_token = os.environ.get("AUTH_TOKEN")

        client = Client(account_sid,auth_token)
        client.messages.create(
            to=my_phone,
            from_="+18082154128",
            body=msg
        )

    def bestbuy(self):
        self .browser.get("https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161")

CheckStock()