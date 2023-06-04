from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class BaseHandler():

    def __init__(self, *args, **kwargs):
        self.headless = kwargs['headless']

        self.driver = None
        self.cookies = None

        self.path_to_chrome_driver = '/Users/kirill/Downloads/chromedriver'
        self.path_to_ff_driver = '/Users/kirill/Downloads/geckodriver'

    def init_driver(self):
        """
        метод для иницилизации фаер фокса
        """
        options = Options()

        capabilities = webdriver.DesiredCapabilities.FIREFOX
        capabilities['marionette'] = True

        if self.headless:
            options.headless = True

        self.driver = webdriver.Firefox(capabilities=capabilities,
                                        options=options,
                                        executable_path=self.path_to_ff_driver,
                                        )

    def init_chrome_driver(self):
        """
        метод для иницилизации хром драйвера
        """
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--incognito")

        if self.headless:
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(self.path_to_chrome_driver, options=chrome_options)

    def close_driver(self):
        self.driver.close()
        self.driver.quit()
