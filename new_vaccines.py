# ワクチン予約自動処理ツール

from time import sleep
from selenium import webdriver
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import os
#from  import ToastNotifier

# Global variables, login information 

week_day = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

possible_marus = ["○", "◯", "〇", "⭕️", "⚪︎", "△", "△","×"]

def login(driver, district_num, vaccination_num, birthdate):
    driver.get("https://www.vaccine.mrso.jp/sdftokyo/VisitNumbers/visitnoAuth/")
    year, month, day = birthdate.strip().split("-")
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    shikuchouson = driver.find_element_by_xpath("//input[@name='data[VisitnoAuth][name]']")
    shikuchouson.send_keys(district_num) # must be string
    sesshukenn = driver.find_element_by_xpath("//input[@name='data[VisitnoAuth][visitno]']")
    sesshukenn.send_keys(vaccination_num) # must be string 
    bdate_yr = driver.find_element_by_xpath("//select[@name='data[VisitnoAuth][year]']/option[@value={}]".format(int(year)))
    bdate_yr.click()
    bdate_mth = driver.find_element_by_xpath("//select[@name='data[VisitnoAuth][month]']/option[text()='{}']".format(month))
    bdate_mth.click()
    bdate_day = driver.find_element_by_xpath("//select[@name='data[VisitnoAuth][day]']/option[text()='{}']".format(day))
    bdate_day.click()
    tsugi_he_button = driver.find_element_by_xpath("//button[@type='submit']")
    tsugi_he_button.click()
    tsugi_he_button = driver.find_element_by_xpath("//button[@type='submit']")
    tsugi_he_button.click()
    shosai_yoyaku = driver.find_element_by_xpath("//a[@role='button']")
    shosai_yoyaku.click()
    sleep(3)


def search_and_notify3(days_lst, driver, region_code, vaccine_code, birthdate, unopen_days):
    for l in days_lst:
        day = l.find_element_by_xpath("./preceding-sibling::span[@class='day']")
        if l.text.strip() != "×" and day.text not in unopen_days:
            print("Reservation opening found for the", day.text, "th", "on", datetime.now())
            l.click()
            #print(driver.page_source)
            click_time_and_submit(driver, region_code, vaccine_code, birthdate, unopen_days)
            break


def click_time_and_submit(driver, region_code, vaccine_code, birthdate, unopen_days):
    #print(driver.page_source)
    time_slots = driver.find_elements_by_partial_link_text('残り')
    time_slots2 = driver.find_elements_by_xpath("//a[@role='button']") # backup and also sends page back if reservation is full
    if time_slots: 
        time_slots[len(time_slots)//2].click()
        #print(driver.page_source)
        # はい、していません is already checked
        # <button type="submit" class="btn btn-lg btn-warning center-block btn-next">予約内容確認</button>
        sbmt_btn1 = driver.find_elements_by_xpath("//button[@type='submit']")
        sbmt_btn2 = driver.find_elements_by_partial_link_text('予約内容確認')
        if sbmt_btn1: 
            sbmt_btn1[0].click()
            final_submit(driver, region_code, vaccine_code, birthdate, unopen_days)
        elif sbmt_btn2:
            sbmt_btn2[0].click()
            final_submit(driver, region_code, vaccine_code, birthdate, unopen_days)
    elif time_slots2:
        #print(driver.page_source)
        time_slots2[len(time_slots2)//2].click()
        # はい、していません is already checked
        # <button type="submit" class="btn btn-lg btn-warning center-block btn-next">予約内容確認</button>
        sbmt_btn1 = driver.find_elements_by_xpath("//button[@type='submit']")
        sbmt_btn2 = driver.find_elements_by_partial_link_text('予約内容確認')
        if sbmt_btn1:
            sbmt_btn1[0].click()
            final_submit(driver, region_code, vaccine_code, birthdate, unopen_days)
        elif sbmt_btn2:
            sbmt_btn2[0].click()
            final_submit(driver, region_code, vaccine_code, birthdate, unopen_days)
    

    #else:
        #back_btn = driver.find_element_by_partial_link_text('日付を')
        #back_btn.click()
        
def final_submit(driver, region_code, vaccine_code, birthdate, unopen_days):
    print(driver.page_source)
    option1 = driver.find_elements_by_xpath("//button[@type='submit']")
    if option1:
        option1[0].click()
        sleep(5)
        login(driver, region_code, vaccine_code, birthdate)
    else:
        print(driver.page_source)
        i = 0
        while i < 5:
            os.system('say "大至急よやくするボタンを押してください"') 
            i += 1
        login(driver, region_code, vaccine_code, birthdate)
        
        

def find_days_of_week3(driver):
    days_lst = []
    """
    driver.find_element_by_link_text('2021年06月').click()
    sleep(1)
    for symbol in possible_marus:
        days_lst += driver.find_elements_by_partial_link_text('{}'.format(symbol))
    """
    for symbol in possible_marus:
        days_lst += driver.find_elements_by_partial_link_text('{}'.format(symbol))
    #for d in days_lst:
    #    print(d.text)
    #print(len(days_lst))
    return days_lst


def reserve_spot(driver, region_code, vaccine_code, birthdate, unopen_days):
    login(driver, region_code, vaccine_code, birthdate)
    while True:
        #driver.refresh()
        days = find_days_of_week3(driver)
        search_and_notify3(days, driver, region_code, vaccine_code, birthdate, unopen_days) # unavailable days in list form)
        driver.refresh()
        sleep(0.5)



if __name__ == "__main__":
    region_code = input("市区町村コードを記入ください: ")
    vaccine_code = input("接種券コードを記入ください: ")
    birthdate = input("生年月日を'年-月-日'の形式でハイフンで区切りながら半角数字で記入ください: ")
    unopen_days0 = input("今月空いていない日を、日にちだけ、空白で分けながら半角数字で列挙してください.\n \
    例）今月の７日と１５日、１９日がだめな場合、　'7 15 19'と記入:\n")
    unopen_days = set(unopen_days.split())
    driver = webdriver.Chrome(ChromeDriverManager().install())
    reserve_spot(driver, region_code, vaccine_code, birthdate, unopen_days)
# update search_days to include Xs, calculate which days are unavailable from datetime (as +i from today) and use enumerate to filter. 



"""
def find_days_of_week(driver):

    days_lst = find_days_single_month(driver)
    #if len(days_lst) < 7:
    sleep(1)
    driver.find_element_by_link_text('2021年07月').click()
    sleep(3)
    days_lst += find_days_single_month(driver)
    sleep(1)
    driver.find_element_by_link_text('2021年06月').click()
    
    for l in days_lst:
        print(l.text)

    return days_lst

def find_days_single_month(driver):
    links_lst = driver.find_elements_by_xpath("//a")
    days_lst = []

    for l in links_lst:
        if len(l.text.strip()) == 1:
            #print(l.text.strip())
            days_lst.append(l)
    return days_lst

def search_and_notify(days_lst):
    for l in days_lst:
        if l.text.strip() and l.text.strip() != "×":
            print(l.text.strip())
            print("Reservation opening found!!!")
            print(datetime.now())
            i = 0
            while i < 15:
                os.system('say "予約に空きがみつかりました"') 
                i += 1
                sleep(2)

def find_days_of_week2(driver):
    i = 0
    today = datetime.today().weekday()
    days_lst = []
    day_0 = driver.find_element_by_xpath("//td[@class='today']/a")
    days_lst.append(day_0)
    for day in week_day[((today + 2) % 7):]:
        days_lst.append(driver.find_element_by_xpath("//td[@class='{}']/a".format(day)))
    for d in days_lst:
        print(d.text)
    return days_lst
"""