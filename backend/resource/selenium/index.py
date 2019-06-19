#!/user/bin/env python
# -*-coding:utf-8-*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import xlrd
from app.config import config

class selenium:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def index(self,excel_list):
        username = 'matt.wang'
        password = 'Mawa5749'
        self.driver.get("https://intranet.thirdbridge.com/offspring/login")
        self.driver.find_element_by_id('email_address').send_keys(username)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('login_query').click()

        time.sleep(5)
        element = self.driver.find_element_by_class_name('rollover-container-slide-right')
        action = ActionChains(self.driver)
        time.sleep(5)
        action.move_to_element(element).perform()
        time.sleep(5)

        self.driver.find_element_by_xpath('//ul[@class="no-list rollover-item"]/a[10]').click()
        time.sleep(2)
        for list in excel_list:
            self.driver.find_element_by_xpath(
                '//div[@class="list_right"]/div[@class="window_header"]/span[2]/a[2]').click()
            time.sleep(5)
            HRID = list[7]
            FirstName = list[5]
            SurName = list[6]
            EmailAddress = list[10]
            PhoneNumber = list[12]
            if len(list) == 16:
                MobilePhoneNumber = list[15]
            else:
                MobilePhoneNumber = ''
            OfficePhoneExtension = list[11]
            Password = list[13]
            StartDate = list[8]
            StartOp = list[8]
            team_ID = teamID(list[3])
            title_ID = TitleID(list[2])
            Location = LocationID(list[14])
            Position = RoleID(list[2], team_ID)
            Lan = Language(Location, team_ID)
            # 填写数据

            s1 = Select(self.driver.find_element_by_name('Title'))
            s2 = Select(self.driver.find_element_by_name('Position'))
            s3 = Select(self.driver.find_element_by_name('Status'))
            s4 = Select(self.driver.find_element_by_name('Location'))
            s5 = Select(self.driver.find_element_by_name('TeamID'))
            s6 = Select(self.driver.find_element_by_name('External'))
            s7 = Select(self.driver.find_element_by_name('StaffGroup'))
            s8 = Select(self.driver.find_element_by_name('Profile'))
            s9 = Select(self.driver.find_element_by_name('Languages[]'))

            self.driver.find_element_by_name('HRID').send_keys(HRID)
            if type(title_ID) == int:
                s1.select_by_index(title_ID)
            else:
                s1.select_by_value(title_ID)
            if Position:
                s2.select_by_value(Position)
            else:
                s2.select_by_index('0')

            self.driver.find_element_by_name('FirstName').send_keys(FirstName)
            self.driver.find_element_by_name('Surname').send_keys(SurName)
            self.driver.find_element_by_name('EmailAddress').send_keys(EmailAddress)
            s3.select_by_value('ACTIVE')
            self.driver.find_element_by_name('PhoneNumber').send_keys(PhoneNumber)
            self.driver.find_element_by_name('MobilePhoneNumber').send_keys(MobilePhoneNumber)
            self.driver.find_element_by_name('OfficePhoneExtension').send_keys(OfficePhoneExtension)
            self.driver.find_element_by_name('Password').send_keys(Password)
            s4.select_by_value(Location)
            s5.select_by_value(team_ID)
            s6.select_by_value('0')
            s7.select_by_value('Cognolink')
            s8.select_by_value('STAFF')
            self.driver.find_element_by_name('StartDate').send_keys(StartDate)
            self.driver.find_element_by_name('StartOp').send_keys(StartOp)
            for i in Lan:
                s9.select_by_value(i)
            time.sleep(5)
            self.driver.find_element_by_name('insert').click()





def teamID(date):
    if config.Team[date]:
        return config.Team[date]
    else:
        return False


def TitleID(date):
    if config.Title[date]:
        return config.Title[date]
    else:
        return False


def RoleID(date, teamID):
    if date in config.Role and teamID in config.position:
        return config.Role[date]
    else:
        return False


def LocationID(date):
    if config.Office_location[date]:
        return config.Office_location[date]
    else:
        return False


def Language(location, teamID):
    list = ['en']
    if location == 'SHG':
        if teamID == '40':
            list.append('ja')
        elif teamID == '54' or teamID == '135':
            list.append('ko')
        else:
            pass
    else:
        pass

    return list


if __name__ == '__main__':
    selenium = selenium()
    selenium.index()
