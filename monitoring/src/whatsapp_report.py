from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utilities.src.utils import *


class WhatsappBot:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://web.whatsapp.com/")
        self.driver.maximize_window()
        time.sleep(40)

    def send_msg(self, group_title, msg):
        try:
            group = self.driver.find_element_by_xpath('//span[@title="%s"]' % group_title)
            group.click()
            time.sleep(1)
            message_inputs = self.driver.find_elements_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]')
            for message_input in message_inputs:
                if int(message_input.get_attribute('data-tab')) == 1:
                    message_input.click()
                    message_input.send_keys(msg)
                    ActionChains(self.driver).key_down(Keys.ENTER).perform()
        except Exception as ex:
            print(ex)

    def upload_file(self, group_title, file_path):
        try:
            group = self.driver.find_element_by_xpath('//span[@title="%s"]' % group_title)
            group.click()
            time.sleep(1)
            self.driver.find_element_by_xpath("//span[@data-icon='clip']").click()
            self.driver.find_element_by_xpath("//input[@type='file']").send_keys(file_path)
            time.sleep(1)
            self.driver.find_element_by_xpath("//span[@data-icon='send']").click()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    wbot = WhatsappBot()
    wbot.upload_file('Saeed', root_path('Config/prrt.xlsx'))