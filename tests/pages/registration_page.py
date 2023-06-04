import time
from selenium.webdriver.common.by import By


class RegistrationPage():

    PATH_TO_REGISTRATION_FORM = "http://localhost/registration"

    def __init__(self, browser):
        self.browser = browser.driver
        
    def open(self):
        self.browser.get(self.PATH_TO_REGISTRATION_FORM)
    
    def send_form(self):
        time.sleep(3)
        self.browser.find_element(By.ID, "name").send_keys("Test")
        self.browser.find_element(By.ID,"surname").send_keys("Tester")
        self.browser.find_element(By.ID,"group").send_keys("bsbo_06_20")
        self.browser.find_element(By.ID,"email").send_keys("testEmail@mail.ru")
        self.browser.find_element(By.ID,"password").send_keys("qazwsx123edc")
        self.browser.find_element(By.ID,"repeat_password").send_keys("qazwsx123edc")
        
        self.browser.find_element(By.XPATH , '//*[@id="app"]/div/main/div/div/form/input').click()
        time.sleep(3)

    def find_task_list_if_exists(self):
        return self.browser.find_element(By.ID,"task-list").is_displayed()

    def check_curent_url(self):
        return self.browser.current_url
    
    def find_logout_button_if_exists(self):
        return self.browser.find_element(By.XPATH,'//*[@id="navbarSupportedContent"]/ul/li[5]/a').text
    
 
