# -*- coding:utf-8 -*-
import time
import os
import pandas as pd
import re
import requests
import newspaper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
import logging
import jieba

import config

jieba.setLogLevel(logging.INFO)
dir = os.getcwd()


def option():
    options = Options()
    # options.add_argument('--start-maximized')
    options.set_capability('pageLoadStrategy', 'normal')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # prevent driver from closing automatically
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    return options

def login_system(options, url_login, username, password):
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 60)
    wait.until(EC.visibility_of_element_located((By.ID, "username")))
    wait.until(EC.visibility_of_element_located((By.ID, "password")))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    driver.find_element(by=By.ID, value='username').send_keys(username)
    driver.find_element(by=By.ID, value='password').send_keys(password)
    driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']").click() 
    time.sleep(3) # Wait session and token to be returned & stored in browser
    status_code = driver.get(url_login)
    return driver

from datetime import datetime, timedelta

def date_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.now()

    delta = end - start
    date_list = []

    for i in range(delta.days + 1):
        date = start + timedelta(days=i)
        date_list.append(date.strftime('%Y-%m-%d'))

    return date_list


def parse_full_content(wait, driver, page): 
    print('-'*50)  

    node = '//article[@class="art art-stack"]/header/hgroup/h1/a[@href="javascript:void(0)"]'    
    wait.until(EC.presence_of_element_located((By.XPATH, node)))
    links = driver.find_elements(By.XPATH, node)

    full_contents = []

    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-article-title="true"][-nd-tap-highlight-class-name="active"]')))
    # titles = driver.find_elements(By.CSS_SELECTOR, 'h1[data-article-title="true"][-nd-tap-highlight-class-name="active"]')
    wait.until(EC.presence_of_element_located((By.XPATH, '//article[@class="art art-stack"]/header/hgroup/h1')))
    titles = driver.find_elements(By.XPATH, '//article[@class="art art-stack"]/header/hgroup/h1')
    for item, title in enumerate(titles):
        print(f'item: {item+1}, title: {title.text}')

    # wait.until(EC.presence_of_element_located((By.XPATH, '//article[@class="art art-stack"]/header/ul[class="art-byline"]/li[class="art-date"]/a/time')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//article[@class="art art-stack"]/header/ul/li/a/time')))
    datetimes = driver.find_elements(By.XPATH, '//article[@class="art art-stack"]/header/ul/li/a/time')
    for item, datetime in enumerate(datetimes):
        print(f'item: {item+1}, datetime: {datetime.text}')

    wait.until(EC.presence_of_element_located((By.XPATH, '//article/header/ul/li[@class="art-author"]')))
    authors = driver.find_elements(By.XPATH, '//article/header/ul/li[@class="art-author"]')
    for item, author in enumerate(authors):
        print(f'item: {item+1}, author: {author.text}')

        # author = driver.find_element(By.CSS_SELECTOR, 'ul[class="art-byline"]/li[class="art-author"]').text

    for i in range(len(links)): 
        # print(f'page: {page}, item: {i+1}')
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="readmore"]')))
        links = driver.find_elements(By.XPATH, node)
        driver.execute_script("arguments[0].click();", links[i])
        # print('-'*50)
        wait.until(EC.presence_of_element_located((By.XPATH, '//article[@class="art"]')))
        url_page = driver.current_url  
        # titles = driver.find_elements(By.CSS_SELECTOR, 'h1[data-article-title="true"][-nd-tap-highlight-class-name="active"]/text()')
        # titles = driver.find_elements(By.XPATH, '//h1[data-article-title="true"]/text()')
        # titles = driver.find_elements(By.XPATH, "//h1[contains(@data-article-title, 'true')]")
        

        
        # full_content = driver.find_element(By.TAG_NAME, '//article[@class="art"]/div[2]/div/p')
        # print(f"titles: {title.text for title in titles}")

        


        # # try:
        # article = newspaper.Article(url_page, language='en')
        # # else:
        #     # article = newspaper.Article(url_page, language='ch')
        # article.download()
        # while article.download_state != 2:  
        #     article.download() 
        #     time.sleep(10)
        # if article.download_state == 2:
        #     article.parse()
        #     full_content = article.text
        #     print(f"full_content: {full_content}")
        #     full_contents.append(full_content)
        # else: print(article.download_state)
        # # break
    # return titles

def find_next_page(driver, wait):    

    node = '//article[@class="art art-stack"]/header/hgroup/h1/a[@href="javascript:void(0)"]'    
    wait.until(EC.presence_of_element_located((By.XPATH, node)))
    print('*'*50)
    niagara_falls = driver.find_element(By.CLASS_NAME, "toolbar-slider-right")
    print('*'*50)
    # driver.execute_script("arguments[0].scrollIntoView();", niagara_falls)
    niagara_falls = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "toolbar-slider-right")))

# 滚动到元素可见
    driver.execute_script("arguments[0].scrollIntoView();", niagara_falls)

    try:
        print('*'*50)
        # niagara_falls = driver.find_element(By.CSS_SELECTOR, 'div[class="toolbar-slider-right"]/a')
        # niagara_falls = driver.find_element(By.CLASS_NAME, "toolbar-slider-right")
        # if niagara_falls:             
        # driver.execute_script("arguments[0].scrollIntoView();", niagara_falls)
        # scheight = .1
        # while scheight < 9.9:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        #     scheight += .01
        # else:
        #     print('can not find the next page')
            # break
    except:
        print('can not find the next page')
        # break