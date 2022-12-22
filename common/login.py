from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from os.path import join


class Login:

    def login(self):
        root = join(__file__, "../..")
        driver_path = join(root, "../chromedriver.exe")

        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        chrome_service = fs.Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=chrome_service, options=options)

        return driver



