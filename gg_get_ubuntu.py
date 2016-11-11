# coding=utf-8
# -*- coding:cp936 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import matplotlib.dates as mdates
import time
import datetime

# 启动浏览器
print("...开始加载浏览器")
driver = webdriver.Chrome()
print("...浏览器加载完成" + "\n")

# 输入网页
print("...输入网页 等待网页加载")
driver.get("http://www.ggbinary.com/Trading/")

# time.sleep(30)
# WebDriverWait(driver, 600).until(ec.presence_of_element_located((By.ID, "login")))
print("...网页加载完成" + "\n")

# 登入
print("...开始登入账号")

user_email = "???@???.com"
email_address = "//input[@class='input-field email'][@type='text']"
driver.find_element_by_xpath(email_address).send_keys(user_email)
print('find email address')

password = "123456"
password_address = "//input[@class='input-field password'][@type='password']"
driver.find_element_by_xpath(password_address).send_keys(password)
print('find password address')

login_address = "//input[@class='submit button'][@type='submit']"
driver.find_element_by_xpath(login_address).click()
print('find login-button address')

# time.sleep(30)
# WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "infomation")))
print("...账号登入完成")


# 跳转到子页面
time.sleep(1)
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@src='https://trading.ggbinary.com/?currency=1']"))

# 进入收藏页
xpath_shouc = "//a[@href='#'][@data-filter='starred']"
driver.find_element_by_xpath(xpath_shouc).click()
time.sleep(1)

# 网格视图
xpath_grid = "//div[@class='tpl-select-small-icon']"
driver.find_element_by_xpath(xpath_grid).click()

EURUSD, EURJPY, EURAUD, USDJPY = "0", "0", "0", "0"

count = 0

# WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.ID, "game-1")))
# time.sleep(30)  # 等待20S 以便数据加载 不产生空值

filetitle = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
while True:
    # 从网页获取数据
    EURUSD = driver.find_element_by_id("game-1").get_attribute("data-spot")
    EURJPY = driver.find_element_by_id("game-152").get_attribute("data-spot")
    EURAUD = driver.find_element_by_id("game-146").get_attribute("data-spot")
    USDJPY = driver.find_element_by_id("game-2").get_attribute("data-spot")
    now = datetime.datetime.now()
    time_unix = time.time()
    time_date2num = mdates.date2num(now)
    time_normal = now.strftime('%Y-%m-%d %H:%M:%S')+'.'+str(now.microsecond)

    infor = time_normal+',EUR/USD:'+EURUSD+',EUR/JPY:'+EURJPY+',EUR/AUD:'+EURAUD+',USD/JPY:'+USDJPY
    print(infor)

    # write to file
    f = open('/home/lin/ggprice/'+filetitle+'.csv', 'at')
    f.write(infor+'\n')
    f.close()

    count += 1
    time.sleep(0.2)
