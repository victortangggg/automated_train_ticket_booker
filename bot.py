from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
username = config['credentials']['username']
password = config['credentials']['password']
customer = config['credentials']['customer']

path = config['driver']['path']

time_period = "MO"
the_date = "16/11/2018"
jb_sentral = "37500"
singapore = "37600"
time_slot = "%s 07:00" % the_date

if time_period == "EM":
        time_slot = "%s 06:30" % the_date

driver = webdriver.Chrome(executable_path=path)
driver.maximize_window()
url = "https://eticket.ktmb.com.my/guest/ticket/select?origin=%s&destination=%s&odate=%s&oth=%s&rdate=undefined&rth=undefined&adult=1&child=0&isreturn0&pcode=undefined" % (jb_sentral, singapore, the_date, time_period)
driver.get(url)

def waiting(func1):
    def action(*args, **kwargs):
        while True:
            try:
                if func1(*args, **kwargs):
                    break
            except:
                driver.get(url)
    return action

@waiting
def find_timeslot_and_click(driver):
    xpath =  "//div[@name='%s_%s_1']/div[@class='row']/div/div/span[@class='time ng-binding' and contains(text(), '%s')]" % (jb_sentral, singapore, time_slot)
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.click()
    driver.find_element_by_xpath("//input[@value='PROCEED »']").click()
    return True

def login(driver):
    time.sleep(1)
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='userModal']/div/form/div/div[2]/div/div/div[1]/div/input"))
    ).send_keys(username)
    time.sleep(1)
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='userModal']/div/form/div/div[2]/div/div/div[2]/div/input"))
    ).send_keys(password)
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-success']"))
    ).click()
    time.sleep(3)

def select_customer_profile(driver):
    xpath = "//select[@ng-model='favSelect']"
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
    )
    if element != None:
        Select(driver.find_element_by_xpath(xpath)).select_by_value(customer)

def proceed_to_seat_page(driver):
    time.sleep(1)
    driver.find_element_by_xpath("//input[@value='Select Seat(s) »']").click()

def find_seat(current_page, driver):
        for i in range(1, 80):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "%s_%s_%s_%s" % (jb_sentral, singapore, current_page, i)))
                )
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

if __name__ == "__main__":
    find_timeslot_and_click(driver)
    login(driver)
    select_customer_profile(driver)
    proceed_to_seat_page(driver)

    current_page = 1
    seat_id = ""
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
                        driver.implicitly_wait(10)
                        element.click()