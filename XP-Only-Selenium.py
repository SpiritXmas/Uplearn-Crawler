from math import ceil
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'disable-popup-blocking', 'enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)


driver.get("https://web.uplearn.co.uk/login")

input("Press enter once logged in...")

xp_wanted = ceil(int(input("Desired xp gain: "))/16)

delay = 0.2


#main class

def ProtectedCall(function):
    try:
        function()
    except: pass

    return True

class Search:
    def Button(text, click=False):
        btn, timeout = False, 0

        while not btn:
            try:
                if not click:
                    btn = driver.find_elements(By.XPATH, '//button[normalize-space()="' + text + '"]')
                else:
                    btn = driver.find_element(By.XPATH, '//button[normalize-space()="' + text + '"]')
            except:
                sleep(0.1)
                timeout += 1

            if timeout >= 100:
                raise Exception("Timeout within function 'Button' with arguments text:'" + text + "' and click:'" + str(click) + "'")
        
        if not click:
            return btn
        
        btn.click()

        return True
    
    def CheckBox(option, click=False, option2=""):
        chckbx, timeout = False, 0

        search_string = ""
        if option2 == "":
            search_string = "//input[@value='" + option + "']"
        else:
            search_string = "//input[@value='" + option + "'][@name='" + option2 + "']"

        while not chckbx:
            try:
                if not click:
                    chckbx = driver.find_elements(By.XPATH, search_string)
                else:
                    chckbx = driver.find_element(By.XPATH, search_string) 
            except:
                sleep(0.1)
                timeout += 1

            if timeout >= 100:
                raise Exception("Timeout within function 'CheckBox' with arguments option:'" + option + "' and click:'" + str(click) + "' and option2:'" + option2 + "'")

        if not click:
            return chckbx
        
        chckbx.click()

        return True

    def DropDown(name, value):
        drpdown, timeout = False, 0

        while not drpdown:
            try:
                drpdown = driver.find_element(By.XPATH, "//select[@name='" + name + "']")
            except:
                sleep(0.1)
                timeout += 1

            if timeout >= 100:
                raise Exception("Timeout within function 'DropDown' with arguments name:'" + name + "' and value:'" + value + "'")
        
        select = Select(drpdown)

        select.select_by_value(value)

    def IntermediateNextPage():
        Search.Button("I know it", True)
        Search.Button("Submit", True)

        sleep(0.1)

        Search.Button("Continue ->", True)

    def NextPage():
        timeout = 0
        while not ProtectedCall(Search.IntermediateNextPage):
            timeout += 1
            sleep(0.1)

            if timeout >= 100:
                return Exception("Timeout within function 'NextPage' with null arguments.")


for iteration in range(xp_wanted):
    driver.get("https://app.uplearn.co.uk/learn/maths-1/symbols-and-meaning/subsection-quiz")

    # initialise

    Search.Button("Begin?", True)

    sleep(delay)

    # sifting through questions

    Search.CheckBox("option2", True)
    Search.CheckBox("option4", True)
    Search.NextPage()

    Search.CheckBox("option2", True)
    Search.NextPage()

    Search.CheckBox("option3", True, "optionsRadios[0][]")
    Search.CheckBox("option1", True, "optionsRadios[1][]")
    Search.NextPage()

    Search.CheckBox("option1", True)
    Search.CheckBox("option2", True)
    Search.CheckBox("option3", True)
    Search.CheckBox("option4", True)
    Search.NextPage()

    Search.CheckBox("option2", True)
    Search.CheckBox("option4", True)
    Search.NextPage()

    Search.CheckBox("option1", True)
    Search.CheckBox("option2", True)
    Search.CheckBox("option3", True)
    Search.CheckBox("option5", True)
    Search.CheckBox("option7", True)
    Search.CheckBox("option8", True)
    Search.NextPage()

    Search.DropDown("optionsDropdown[0][]", "≡")
    Search.DropDown("optionsDropdown[1][]", "≡")
    Search.DropDown("optionsDropdown[2][]", "=")
    Search.DropDown("optionsDropdown[3][]", "≡")
    Search.CheckBox("option1", True)
    Search.CheckBox("option3", True)
    Search.NextPage()

    Search.CheckBox("option1", True)
    Search.NextPage()

    sleep(1)

driver.quit()

print("Finished xp gain.")