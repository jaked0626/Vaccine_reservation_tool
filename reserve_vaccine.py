# ワクチン予約自動処理ツール

from time import sleep
from selenium import webdriver
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from calendar import monthrange

class VacReserve(object):
    def __init__(self, driver, region_code, vaccine_code, birthdate, unopen_days):
        self.driver = driver
        self.starting_url = "https://www.vaccine.mrso.jp/sdftokyo/VisitNumbers/visitnoAuth/"
        self.region_code = region_code
        self.vaccine_code = vaccine_code
        self.birthdate = birthdate
        self.unopen_days = set(unopen_days.split())
        self.possible_marus = ["○", "◯", "〇", "⭕️", "⚪︎", "△", "△","×"]
        self.month_length_dic = {}
    
    def login(self):
        self.driver.get(self.starting_url)
        year, month, day = self.birthdate.strip().split("-")
        shikuchouson = self.driver.find_element_by_xpath("//input[@name='data[VisitnoAuth][name]']")
        shikuchouson.send_keys(self.region_code) # must be string
        sesshukenn = self.driver.find_element_by_xpath("//input[@name='data[VisitnoAuth][visitno]']")
        sesshukenn.send_keys(self.vaccine_code) # must be string 
        bdate_yr = self.driver.find_element_by_xpath("//select[@name='data[VisitnoAuth][year]']/option[@value={}]".format(int(year)))
        bdate_yr.click()
        bdate_mth = self.driver.find_element_by_xpath("//select[@name='data[VisitnoAuth][month]']/option[text()='{}']".format(self.prepend_zero(month)))
        bdate_mth.click()
        bdate_day = self.driver.find_element_by_xpath("//select[@name='data[VisitnoAuth][day]']/option[text()='{}']".format(self.prepend_zero(day)))
        bdate_day.click()
        tsugi_he_button = self.driver.find_element_by_xpath("//button[@type='submit']")
        tsugi_he_button.click()
        tsugi_he_button = self.driver.find_element_by_xpath("//button[@type='submit']")
        tsugi_he_button.click()
        shosai_yoyaku = self.driver.find_element_by_xpath("//a[@role='button']")
        shosai_yoyaku.click()
        sleep(3)

    def find_openings(self):
        openings_lst = []
        for symbol in self.possible_marus:
            openings_lst += self.driver.find_elements_by_partial_link_text('{}'.format(symbol))
        #for d in days_lst:
        #    print(d.text)
        #print(len(days_lst))
        return openings_lst

    def inspect_openings(self, openings_lst):
        for l in openings_lst:
            day = l.find_element_by_xpath("./preceding-sibling::span[@class='day']")
            if l.text.strip() != "×" and day.text not in self.unopen_days:
                print("Reservation opening found for the", day.text, "th", "on", datetime.now())
                l.click()
                #print(driver.page_source)
                self.click_time_and_submit()
                break


    def click_time_and_submit(self):
        #print(driver.page_source)
        time_slots = self.driver.find_elements_by_partial_link_text('残り')
        time_slots2 = self.driver.find_elements_by_xpath("//a[@role='button']") # backup and also sends page back if reservation is full
        if time_slots: 
            time_slots[len(time_slots)//2].click()
            #print(driver.page_source)
            # はい、していません is already checked
            # <button type="submit" class="btn btn-lg btn-warning center-block btn-next">予約内容確認</button>
            sbmt_btn = self.driver.find_elements_by_xpath("//button[@type='submit']")
            if sbmt_btn: 
                sbmt_btn[0].click()
                self.final_submit_page()
        elif time_slots2:
            time_slots2[len(time_slots2)//2].click()
            sbmt_btn = self.driver.find_elements_by_xpath("//button[@type='submit']")
            if sbmt_btn: 
                sbmt_btn[0].click()
                self.final_submit_page()
            
    def final_submit_page(self):
        print(self.driver.page_source)
        option1 = self.driver.find_elements_by_xpath("//button[@type='submit']")
        if option1:
            option1[0].click()
            sleep(5)
            self.login()

    def reserve_main(self):
        self.login()
        dt = datetime.today()
        month_len = monthrange(dt.year, dt.month)[1]
        if (month_len - dt.day) < 7:
            i = 0
            while True:
                openings = self.find_openings()
                self.inspect_openings(openings)
                if i % 2 == 0:
                    self.driver.find_element_by_link_text("{}年{}月".format(
                        dt.year, self.prepend_zero(dt.month))).click()
                else:
                    self.driver.refresh()
                    self.driver.find_element_by_link_text("{}年{}月".format(
                        dt.year, self.prepend_zero(dt.month + 1))).click()
                i += 1
                sleep(0.5)
        else:
            while True:
                openings = self.find_openings()
                self.inspect_openings(openings)
                self.driver.refresh()
                sleep(0.5)
    
    def prepend_zero(self, num):
        n = str(num)
        if len(n) == 1:
            n = "0" + n

        return n


def main():
    region_code = input("市区町村コードを記入ください \nWrite your regional code: \n")
    vaccine_code = input("\n接種券コードを記入ください \nWrite your vaccine code: \n")
    birthdate = input("\n生年月日を'年-月-日'の形式でハイフンで区切りながら半角数字で記入ください \
                      \nWrite your date of birth in the 'year-month-day' format: \n")
    unopen_days = input("\n今月空いていない日を、日にちだけ、空白で分けながら半角数字で列挙してください.\
                         \n例）今月の７日と１５日、１９日がだめな場合、　'7 15 19'と記入\
                        \nList the days of the month you are unavailable in digits and separate each by a space.\
                        \ne.g.) if you are unavailable on the 7th, 15th, and 19th, write '7 15 19': \n")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    vac = VacReserve(driver, region_code, vaccine_code, birthdate, unopen_days)
    vac.reserve_main()

# For people who want to speed up the process
"""
def main():
    region_code = "reg_code"
    vaccine_code = "vac_code"
    birthdate = "year-month-day"
    unopen_days = "day day day"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    vac = VacReserve(driver, region_code, vaccine_code, birthdate, unopen_days)
    vac.reserve_main()
"""

if __name__ == "__main__":
    main()