import selenium
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ObtainWebDriver(driverpath,downloadpath) -> object:
    # Initialize the Service object with the path to the ChromeDriver
    service = Service(driver_path)

    # # Initialize the WebDriver
    #driverobj = webdriver.Chrome(service=service)

    # Set download directory
    chrome_options = Options()
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    driverobj = webdriver.Chrome(service=service, options=chrome_options)

    return driverobj    

def OpenWebsite(driverobj : webdriver.Chrome, webaddress : str):        #Opens Website and Prints the name
        # Open a webpage
        driverobj.get(webaddress)

        # Print the title of the webpage
        print(driverobj.title)

    # Function to close the WebDriver

def close_driver(driver: webdriver.Chrome) -> None:
    driver.quit()

# Function to locate element by XPath and print its value
def print_element_value_by_xpath(driver: webdriver.Chrome, xpath: str) -> None:
    try:
        element = driver.find_element(By.XPATH, xpath)
        print(f"Element value: {element.text}")
    except Exception as e:
        print(f"Error: {e}")

#Function to click on an XPath
def ClickXPath(xpaths) :
    element = driver.find_element(By.XPATH, xpaths)
    element.click()

#Function to check if an Element Exists in the XPATH
def element_exists_by_xpath(driver: webdriver.Chrome, xpath: str) -> bool:
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except NoSuchElementException:
        return False    

#Function to wait Till Available for Download
def wait_TillAvail(driver: webdriver.Chrome, xpath: str, timeout: int = 10) -> None:
    try:
        # Wait until the element is present and clickable
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(f"Clicked on element with XPath: {xpath}")
    except Exception as e:
        print(f"Error: {e}")

#Function to wait Till Download Complete
# def wait_TillComplete(download_path: str, expected_num_files: int, timeout: int = 10) -> bool:
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         # Check if the number of files in the download directory is equal to or greater than expected_num_files
#         if len(os.listdir(download_path)) >= expected_num_files:
#             print(len(os.listdir(download_path)))
#             return True  # Return True if all files are downloaded
#         time.sleep(1)  # Wait for 1 second before checking again
#     return False  # Return False if timeout occurs

#Function to download    
def Download(driver: webdriver.Chrome, downloadpath):
    i = 1;
    xpath = f'//*[@id="spa-root"]/div/div[176]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div[5]/table/tbody/tr[{i}]/td[1]/img'
    wait_TillAvail(driver,xpath,3)
    while element_exists_by_xpath(driver,xpath):
        ClickXPath(xpath)
        time.sleep(2)
        print(xpath)
        i+=1
        xpath = f'//*[@id="spa-root"]/div/div[176]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div[5]/table/tbody/tr[{i}]/td[1]/img'
    # expected_num = i-1   
    # print(f'{expected_num=}') 
    # if expected_num>0:
    #     complete = wait_TillComplete(downloadpath,expected_num,5)
    #     while complete:
    #         complete = wait_TillComplete(downloadpath,expected_num,5)
    #         pass


# Function to change the selected option of a dropdown by XPath
def change_Airline(driver: webdriver.Chrome, option_text: str) -> None:
    try:
        xpath = '//*[@id="selectAirline"]'
        wait_TillAvail(driver,xpath,3)
        ClickXPath(xpath)


        if "AIX Connect"==option_text :
            xpath = '//*[@id="menu-selectAirline"]/div[3]/ul/li[1]'
            ClickXPath(xpath)
        elif "Air India Express" == option_text:
            xpath = '//*[@id="menu-selectAirline"]/div[3]/ul/li[2]'
            ClickXPath(xpath)           
        print(f"Selected option: {option_text}")
    except Exception as e:
        print(f"Error: {e}")


# Function to change the value of an element by XPath
def change_PNR_Value(driver: webdriver.Chrome, new_pnr: str) -> None:
    try:
        xpath = '//*[@id="pnr"]'
        wait_TillAvail(driver,xpath,3)
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        element.clear()  # Clear existing text
        element.send_keys(new_pnr)  # Send new value
        print(f"Element value changed to: {new_pnr}")
    except Exception as e:
        print(f"Error: {e}")

def change_ORG_Value(driver: webdriver.Chrome, new_org: str) -> None:
    try:
        xpath = '//*[@id="Origin"]'
        wait_TillAvail(driver,xpath,3)
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        element.clear()  # Clear existing text
        element.send_keys(new_org)  # Send new value
        xpath = '//*[@id="spa-root"]/div/div[176]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[3]/div[2]'
        ClickXPath(xpath)
        print(f"Element value changed to: {new_org}")
    except Exception as e:
        print(f"Error: {e}")

#Function to Update all Records for one airline, PNR, org
def UpdateRecord(driver, airline, pnr, org) -> None:
    change_Airline(driver, airline)
    change_PNR_Value(driver, pnr)
    change_ORG_Value(driver, org)


# Main script
if __name__ == "__main__":
    driver_path = r'C:\Users\sarve\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Path to the ChromeDriver
    download_path = r'C:\Users\sarve\Downloads\Selenium Invoice Downloads'                            # Path to my Downloads
    driver = ObtainWebDriver(driver_path,download_path)
    webaddress1 = "https://www.google.com"
    webaddress2 = "https://www.airindiaexpress.com/gst-tax-invoice"
    Datalist = [['AIX Connect','KY7Q4E','SXR'],['Air India Express','ABCDEF','MAA']]
    
    try:
        OpenWebsite(driver,webaddress1)
        

        for row in Datalist:
            OpenWebsite(driver,webaddress2)
            airline, NewPNR, NewORG = row
            print(airline, NewPNR, NewORG)
            # airline = 'AIX Connect'
            # NewPNR = 'KY7Q4E'
            # NewORG = 'SXR'
            UpdateRecord(driver,airline,NewPNR,NewORG)
            xpathSearch = '//*[@id="spa-root"]/div/div[176]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[4]/span'
            ClickXPath(xpathSearch)
            Download(driver,download_path)

    finally:
        #Wait for input before closing
        input("Press Enter to close the browser...")
        # Close the browser
        close_driver(driver)







