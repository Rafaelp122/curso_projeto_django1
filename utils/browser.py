# from pathlib import Path

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service

# ROOT_PATH = Path(__file__).parent.parent
# CHROMEDRIVER_NAME = ''
# CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


# def make_chrome_browser(*options):
#     chrome_options = webdriver.ChromeOptions()
#     chrome_service = Service(exutable_path=CHROMEDRIVER_PATH)
#     browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
#     return browser


# if __name__ == '__main__':
#     browser = make_chrome_browser()
#     browser.get('http://www.udemy.com.br/')
#     browser.quit()

import os

from selenium import webdriver


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument(option)

    browser = webdriver.Chrome(options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://www.udemy.com.br/')
    browser.quit()
