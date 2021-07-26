import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import os
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
import requests
import json



class CheckStock:


    def __init__(self):
        """
        Initialization method, this starts the instance of Firefox and run the script
        """
        self.browser = webdriver.Firefox()
        self.check_sites()
        # self.send_sms("HI, this is a test")
        # self.check_bestBuy()

    def check_sites(self):
        """
        A selenium script that goes to target.com and performs an IF-Else on whether the Playstation5 is in stock or not
        IF its not in stock it keeps refreshing the page and posts status updates on the console
        Else it sends a SMS on my phone using Twilio API

        """
        # get the current time for status updates
        in_stock_flag = False
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        self.browser.get("https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596#lnk=sametab")
        # self.browser.get("https://www.target.com/p/dualsense-wireless-controller-for-playstation-5/-/A-81114477") # controller link

        time.sleep(7) # wait 5 seconds OR Check BestBuy

        # print(self.check_bestBuy())

        stock = self.browser.find_element_by_xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[3]/div[1]/div/div/div')
        in_stock = stock.get_attribute('innerHTML')
        keyword = "Out of stock in stores near you"
        if keyword in in_stock:
            in_stock_flag = False
        else:
            in_stock_flag = True


        if not in_stock_flag and self.check_bestBuy() == False:
            print("Status: Sold Out \n"
                  "Last Checked: "+ current_time )
            time.sleep(15)
            self.browser.refresh()
            self.check_sites()

        # Just target check (uncomment only for target)
        # if not in_stock_flag:
        #     print("Status: Sold Out \n"
        #           "Last Checked: "+ current_time )
        #     time.sleep(15)
        #     self.browser.refresh()
        #     self.check_sites()

        elif self.check_bestBuy():
            link = "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161"
            msg = ("Status: PS5 is IN STOCK @ BestBuy\n"
                       "Last Checked: "+ current_time +"\n" + link)
            self.send_sms(msg)
            self.browser.close()

        else:
            msg = ("Status: PS5 is IN STOCK @ Target\n"
            "Last Checked: "+ current_time +"\n" + self.browser.current_url)
            self.send_sms(msg)
            self.browser.close()

    def send_sms(self, msg ):
        """
        The Twillio Function, This method creates a Client using the API and send a text message to my phone
        :param msg: the body of the message
        """
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
        call = client.calls.create(
            to=my_phone,
            from_="+18082154128",
            twiml="<Response><Say>PS5 is in stock!</Say></Response>",
        )

    def check_bestBuy(self):
        """
        This will send an API Call to bestBuy and return the send_sms() method if the ps5 is in stock
        :return:
        """
        load_dotenv(find_dotenv())
        api_key = os.environ.get("BEST_BUY_API_KEY")
        url = "https://api.bestbuy.com/v1/products(sku=6430161)?apiKey="+api_key+"&sort=onlineAvailability.asc&show=onlineAvailability&format=json"

        payload={}
        headers = {}
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            time.sleep(5)
            response = response.json()
            available = response["products"][0]['onlineAvailability']
            return available

        except KeyError:
            print("Key Error, Trying again")
            self.check_bestBuy()







CheckStock()