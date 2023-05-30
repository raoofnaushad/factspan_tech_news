import os
# from  configparser import SafeConfigParser
# import logging.config
from datetime import date
from time import sleep
from pymongo import MongoClient
import requests
import json

from src.config import *

today = str(date.today()) ## Getting date for each day
# today = "2022-10-20"

# def get_logger(name="root"):
#     '''
#     This function used for logging the error and other information
#     '''
#     base_path = os.path.join(os.getcwd(), 'logs')
    
#     ## Create logs folder if not present
#     log_file = os.path.join(base_path, 'log.conf')
#     logging.config.fileConfig(fname=log_file, disable_existing_loggers=False)

#     return logging.getLogger(name)

        

def connect_mong():

    try:
        conn = MongoClient()
        print("Connected successfully to MongoDB")
    except:  
        print("Could not connect to MongoDB. Quitting the program!!")
        exit()

    # database
    db = conn.social_media_automation
    return db


def get_html_content(site):
    content = requests.get(site).text
    return content

def string_present(str1, str2):
    if str1.find(str2) > 0:
        return True
    
    
def user_download(url, filename):
    r = requests.get(url)
    base_path = '/'.join(os.path.abspath(os.getcwd()).split('/')[:-1]) + IMG_PATH
    # filename = filename.replace('/', '_')
    # filename = filename.replace(' ', '')
    out_path = base_path + filename + ".png"
    with open(out_path, 'wb') as f:
        f.write(r.content)
    return out_path


