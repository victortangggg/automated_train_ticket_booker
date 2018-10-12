from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
username = config['credentials']['username']
password = config['credentials']['password']
customer = config['credentials']['customer']

path = config['driver']['path']

options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = webdriver.Chrome(executable_path=path, chrome_options=options)
#driver = webdriver.Firefox(executable_path="C:/selenium_drivers/geckodriver-v0.20.1-win32/geckodriver.exe")
#driver = webdriver.PhantomJS("C:/selenium_drivers/phantomjs-2.1.1-windows/bin/phantomjs.exe")

driver.maximize_window()
driver.get("https://www.ktmb.com.my")

def select_options_click(option_key, option_value):
        element = Select(driver.find_element_by_id(option_key))
        element.select_by_value(option_value)

def input_field_text(input_key, input_value):
        element = driver.find_element_by_id(input_key)
        element.send_keys(input_value)

driver.implicitly_wait(5)
jb_sentral = "37500"
singapore = "37600"
time_period = "MO"

select_options_click("origin1", jb_sentral) # JB SENTRAL
select_options_click("destination1", singapore) # SINGAPORE
tomorrow_date = (datetime.today() + timedelta(1)).strftime("%d/%m/%Y")
input_field_text("selectDate", tomorrow_date)
select_options_click("oth", time_period)

driver.implicitly_wait(10)
driver.find_element_by_id("btnSearch").click()

position = 1
if time_period == "EM":
        selections = driver.find_elements_by_xpath("//div[@title='click to select']")
        position = (len(selections))

content_found = False

while content_found == False:
        try:
                driver.implicitly_wait(10)
                element = driver.find_element_by_id("content")
                element.find_element_by_id(str(position)).click()
                content_found = True
        except:
                driver.refresh()


driver.implicitly_wait(5)
driver.find_element_by_xpath("//input[@value='PROCEED »']").click()

time.sleep(1)
driver.find_element_by_xpath("//input[@ng-model='user.username']").send_keys(username)
time.sleep(1)
driver.find_element_by_xpath("//input[@ng-model='user.password']").send_keys(password)

driver.implicitly_wait(5)
driver.find_element_by_xpath("//button[@class='btn btn-success']").click()

time.sleep(1)
element = Select(driver.find_element_by_xpath("//select[@ng-model='favSelect']"))
element.select_by_value(customer)

time.sleep(1)
driver.implicitly_wait(5)
driver.find_element_by_xpath("//input[@value='Select Seat(s) »']").click()

# error = True

# while error:
#         try:
#                 element_test = driver.find_element_by_id( "%s_%s_%s_%s" % (jb_sentral, singapore, 1, 1) )
#                 print("proceed to next page to select seat")
#                 error = False
#         except:
#                 driver.refresh()

driver.implicitly_wait(5)

current_page = 1
seat_id = ""

def find_seat(current_page, driver):
        for i in range(1, 80):
                try:
                        element = driver.find_element_by_id( "%s_%s_%s_%s" % (jb_sentral, singapore, current_page, i) )
                        disable = element.get_attribute("disabled")
                        if(disable != 'true'):
                                print('click on seat')
                                seat_id = "%s_%s_%s_%s" % (jb_sentral, singapore, current_page, i)
                                driver.execute_script("document.querySelectorAll('label[for=\"%s\"]')[0].click()" % seat_id)
                                driver.implicitly_wait(1)
                                driver.find_element_by_xpath("//input[@value='Proceed »']").submit()

                                driver.implicitly_wait(10)
                                try:
                                        driver.find_element_by_xpath("//input[@type='radio' and @value='CC']").click()

                                        driver.implicitly_wait(1)
                                        driver.find_element_by_xpath("//button[@type='submit' and contains(text(), ' Pay »')]").click()

                                        driver.implicitly_wait(1)
                                        driver.find_element_by_xpath("//button[@ng-click='paymentGateway(channel)']").click()
                                        return "%s_%s_%s_%s" % (jb_sentral, singapore, current_page, i)
                                except:
                                        continue
                except:
                        continue
        
        return ""


while True:
        
        time.sleep(1)
        seat_id = find_seat(current_page, driver)
        if(seat_id != ""):
                break
        
        current_page = current_page - 1
        if(current_page == 5):
                current_page = 1
        if(current_page == 0):
                current_page = 4
        for element in driver.find_elements_by_xpath("//div[@id='coach']/ul/li/a[@href='#']"):
                if(element.text == str(current_page)):
                        driver.implicitly_wait(15)
                        element.click()

driver.execute_script("document.querySelectorAll('label[for=\"%s\"]')[0].click()" % seat_id)
driver.implicitly_wait(1)
driver.find_element_by_xpath("//input[@value='Proceed »']").submit()

driver.implicitly_wait(5)
driver.find_element_by_xpath("//input[@type='radio' and @value='CC']").click()

driver.implicitly_wait(1)
driver.find_element_by_xpath("//button[@type='submit' and contains(text(), ' Pay »')]").click()

driver.implicitly_wait(1)
driver.find_element_by_xpath("//button[@ng-click='paymentGateway(channel)']").click()