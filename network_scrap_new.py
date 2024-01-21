from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd
import time

def variable():
    """
    This function will define the variables and store all the variable globally
    """
    global username
    global password
    global driver_path
    global delay
    global hs_path
    global hs_list
    global hs_df
    global hs_df_copy
    global country
    global exim
    global start_date
    global end_date

    username= input('Enter Username to login : ')
    password= input('Enter  Password to login : ')
    driver_path = input('Enter path of your chromdriver : ')
    delay = 200
    hs_path = input('Enter path of the sheet to look for search items without extension : ')
    hs_df = pd.read_excel(rf'{hs_path}.xlsx')
    hs_df_copy = hs_df.copy()
    hs_df_copy.insert(1,'RECORDS',None)
    hs_df_copy.insert(2,'FILTER',None)
    hs_df_copy.insert(3,'SEARCH',None)
    hs_list = hs_df[list(hs_df.columns)[0]].tolist()
    country = input('Enter country name : ')
    exim = input('Enter Import or Export : ')
    start_date= input('Enter start date in "Xyz 1, 1234" format: ')
    end_date = input('Enter end date in "Xyz 1, 1234" format: ')



def driver_func():
    """
    * This function will call the variable function initially
    * Add the options to open the inspection panel with driver
    * Finally, will run the driver
    """

    variable()

    global driver
    global options

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options, executable_path=driver_path)

def item_select(driver,num):
    global cat_list

    """
    * This function will find element of dropdown list of Category
    * Then will store all of the category item in a list
    * Then will take Category to look for input from the above mentioned list
    * Then will set the Category as input
    * Finally, it will sleep for some duration
    """

    try:
        time.sleep(4) 

        selectElement_present = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#demo-select-small")))
        selectElement = driver.find_element(By.CSS_SELECTOR,'#demo-select-small')
        selectElement.send_keys(Keys.ENTER)
    except:
        return (print('Item Select Error'))
    
    list_item = driver.find_elements(By.TAG_NAME,"li")

    cat_list = []
    for item in list_item:

        if item.get_attribute("innerHTML").split('<')[0] != "":
            if num == 0:
                print(item.get_attribute("innerHTML").split('<')[0])
            cat_list.append(item.get_attribute("innerHTML").split('<')[0])

def category_input():

    global category
    global category_dup

    category = input('Please enter category : ').upper()
    category_dup = category

def item_select_click(number):

    item_select(driver=driver,num=number)

    if number == 0:
        category_input()
    index = cat_list.index(category_dup)
    cat_path = driver.find_element(By.XPATH,rf'//*[@id="menu-"]/div[3]/ul/li[{index+1}]')
    driver.execute_script('arguments[0].click();', cat_path)
    time.sleep(4)

def date(driver):
    start = driver.find_element(By.XPATH, '//*[@id="selectComponent-forExplore"]/div/div[2]/div[1]/div/div/div/div/div[1]/input')
    start.send_keys(Keys.CONTROL + "a")
    start.send_keys(Keys.DELETE)
    start.send_keys(start_date)
    start.send_keys(Keys.ENTER)

    end = driver.find_element(By.XPATH, '//*[@id="selectComponent-forExplore"]/div/div[2]/div[1]/div/div/div/div/div[3]/input')
    end.send_keys(Keys.CONTROL + "a")
    end.send_keys(Keys.DELETE)
    end.send_keys(end_date)
    end.send_keys(Keys.ENTER)


def param(driver):
    """
    * This function will find the dropdown list of selection for Import or Export
    * Will take the value of exim from variable function and select it from dropdown list
    * Then, will find the dropdown list of selection for Country
    * Will take the value of country from variable function and select it from dropdown list.
    * Finally, it will find the trade button and click that button
    """

    try:
        time.sleep(4)
        exim_dropdown_present = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#selectComponent-forExplore > div > div.select-container-div > div.explore-select-container > div > div:nth-child(2) > div > select")))
        exim_dropdown = Select(driver.find_element(By.CSS_SELECTOR,"#selectComponent-forExplore > div > div.select-container-div > div.explore-select-container > div > div:nth-child(2) > div > select"))
        exim_dropdown.select_by_value(f'{exim.upper()}')

        country_dropdown = Select(driver.find_element(By.CSS_SELECTOR,"#selectComponent-forExplore > div > div.select-container-div > div.explore-select-container > div > div:nth-child(3) > div > select"))
        country_dropdown.select_by_value(f'{country.upper()}')

        set_trade_btn = driver.find_element(By.CSS_SELECTOR, "#selectComponent-forExplore > div > div.select-container-div > div.explore-select-container > div > div.setTrade-btn-container > button")
        driver.execute_script('arguments[0].click();', set_trade_btn)
    
    except:
        return (print('Param Error'))

def main():
    """
    * This function will call the driver_func() and get the mentioned page
    * Then will give the input in username and password from variables function
    * Will sleep for mentioned duration to let the page load properly
    * The will the get the mentioned page
    * Then, will call the param and item_select function
    * Will find the input list for the item from excel file to entered
    * Will wait for the mentioned duration to let the the dropdown list open
    * Then, will select the first option from the dropdown list
    * After that, will hit the search button
    * Will wait for some time to completely load the page
    * Execute the script to get the network log in json format
    * Then it will store the json data in a list and finally will fetch all the required data from that list
    * Will append the fetched data in dataframe
    * Will refresh the driver page and enter next item from the excel file
    * At last, will save the dataframe in excel file with name {original_file}_fetch at the same path 
    """


    driver_func()

    driver.get(f"Enter the link of website to login and scrap : ")

    try:
        id_present = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.ID,"email-id-input")))
        driver.find_element("id", "email-id-input").send_keys(username)
        driver.find_element("id", "password-input").send_keys(password)

        login_box = driver.find_element(By.CSS_SELECTOR, "#cta-login-account")
        driver.execute_script('arguments[0].click();', login_box)
    except:
        return (print('Login Error'))
    time.sleep(2)
    driver.get(f"Enter the webpage link to get onto the page : ")
 
    param(driver=driver)

    # putting in the search with term and clicking the search button
    for item in hs_list:
        item_select_click(number=hs_list.index(item))
        date(driver=driver)
        try:
            hs_present = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#react-select-2-input")))
            driver.find_element(By.CSS_SELECTOR, "#react-select-2-input").send_keys(item)

            try:
                time.sleep(4)
                cursor_present = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#react-select-2-listbox > div > div")))
                cursor = driver.find_element(By.CSS_SELECTOR,'#react-select-2-listbox > div > div')
                driver.execute_script('arguments[0].click();', cursor)

                search_btn = driver.find_element(By.CSS_SELECTOR, "#search-container-explore > div > div.search-item.undefined > div > button:nth-child(1)")
                driver.execute_script('arguments[0].click();', search_btn)
                time.sleep(5)
            
            except:
                return (print('Search with term Error'))

        except:
            return (print('search with term Input Error'))
        
        # getting the netwrok data json file

        network_timing_data_script = 'return JSON.stringify(window.performance.getEntriesByType("resource"))'
        network_data = driver.execute_script(network_timing_data_script)
        
        for elem in range(len(json.loads(network_data))):
            if json.loads(network_data)[elem]['name'] == 'Enter the Records URL to fetch network data':
                for num in range(len(hs_df_copy)):
                    if hs_df_copy[(hs_df_copy.columns)[0]][num] == item:
                        hs_df_copy['RECORDS'][num] = json.loads(network_data)[elem]['duration']

            if json.loads(network_data)[elem]['name'] == 'Enter the Filter URL to fetch network data':
                for num in range(len(hs_df_copy)):
                    if hs_df_copy[(hs_df_copy.columns)[0]][num] == item:
                        hs_df_copy['FILTER'][num] = json.loads(network_data)[elem]['duration']    

            if json.loads(network_data)[elem]['name'] == 'Enter the Search URL to fetch network data':
                for num in range(len(hs_df_copy)):
                    if hs_df_copy[(hs_df_copy.columns)[0]][num] == item:
                        hs_df_copy['SEARCH'][num] = json.loads(network_data)[elem]['duration']

        driver.refresh()
        time.sleep(5)
    driver.quit()
    
    hs_df_copy.to_excel(rf'{hs_path}_updated.xlsx',index=False)
if __name__ == "__main__":
    main()