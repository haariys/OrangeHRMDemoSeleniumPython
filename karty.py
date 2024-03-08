from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# initialize web driver with options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # auto download webdriver
driver.maximize_window()
driver.implicitly_wait(5) # I have used implicit and explicit wait but added time.sleep for better visibility for assessment
wait = WebDriverWait(driver, 5)

def logout():    
    driver.find_element(By.CSS_SELECTOR, '.oxd-userdropdown-tab').click()
    driver.find_element(By.CSS_SELECTOR, '.oxd-dropdown-menu > li:nth-child(4) > a:nth-child(1)').click()

"""
******* Main Scenario : User Login *******
"""
# get url
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
time.sleep(5)
# enter username and password
driver.find_element(By.NAME, 'username').send_keys('Admin')
driver.find_element(By.NAME, 'password').send_keys('admin123')
# click login button
driver.find_element(By.CSS_SELECTOR, 'button.oxd-button').click()
# assert page url
get_url = driver.current_url
assert 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index' == get_url,"URL not same"
logout()

"""
******* Alternate Scenario : User Login (Invalid Credentials) *******
"""
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
time.sleep(5)
# enter username and password
driver.find_element(By.NAME, 'username').send_keys('admin1')
driver.find_element(By.NAME, 'password').send_keys('admin1')
# click login button
driver.find_element(By.CSS_SELECTOR, 'button.oxd-button').click()
time.sleep(5)
# assert Invalid Credentials text on page
try:  
    driver.find_element(By.CSS_SELECTOR, '.oxd-alert-content-text')
except Exception as e:
    print ("Element not found")


"""
******* Alternate Scenario : User Login (Both Credentials Blank) *******
"""
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
time.sleep(5)
# do not enter username and password
# click login button
driver.find_element(By.CSS_SELECTOR, 'button.oxd-button').click()
# assert Required text on both fields
elements=driver.find_elements(By.XPATH, '//*[text()="Required"]')
assert len(elements)==2, "The elements not found"
time.sleep(2)

# """
# ******* Alternate Scenario : User Login (Only Password Blank) *******
# """
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
time.sleep(5)
driver.find_element(By.NAME, 'username').send_keys('Admin')
# do not enter password
# click login button
driver.find_element(By.CSS_SELECTOR, 'button.oxd-button').click()
# assert Required text on both fields
elements=driver.find_elements(By.XPATH, '//*[text()="Required"]')
assert len(elements)==1, "The elements not found"
time.sleep(2)

# """
# ******* Main Scenario : Password Reset *******
# """
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
time.sleep(5)
# do not enter username and password
# click login button
driver.find_element(By.CSS_SELECTOR, '.orangehrm-login-forgot-header').click()
time.sleep(5)
get_url = driver.current_url
assert "https://opensource-demo.orangehrmlive.com/web/index.php/auth/requestPasswordResetCode" in get_url,"Page not found"
driver.find_element(By.NAME, 'username').send_keys('Admin')
driver.find_element(By.CSS_SELECTOR, 'button.oxd-button:nth-child(2)').click()
time.sleep(5)
assert driver.find_elements(By.XPATH, '//*[text()="Reset Password link sent successfully"]') , "Error: Email not sent"
time.sleep(2)

"""
******* Alternate Scenario : Password Reset (Blank username) *******
"""
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
time.sleep(5)
# do not enter username and password
# click login button
driver.find_element(By.CSS_SELECTOR, '.orangehrm-login-forgot-header').click()
time.sleep(5)
get_url = driver.current_url
# assert url
assert "https://opensource-demo.orangehrmlive.com/web/index.php/auth/requestPasswordResetCode" in get_url,"Page not found"
# click reset button
driver.find_element(By.CSS_SELECTOR, 'button.oxd-button:nth-child(2)').click()
# assert text 
assert driver.find_element(By.XPATH, '//*[text()="Required"]')
time.sleep(2)

"""
******* Alternate Scenario : Password Reset (Invalid email) *******
"""
driver.get("https://www.facebook.com")
time.sleep(5)
# click on Forgotten Password link
driver.find_element(By.XPATH, '//*[text()="Forgotten password?"]').click()
time.sleep(5)
# enter wrong email and search
driver.find_element(By.ID, 'identify_email').send_keys('1111111111111111111111111111@g.com')
driver.find_element(By.ID, 'did_submit').click()
# assert text
assert wait.until(EC.visibility_of_element_located((By.XPATH, '//*[text()="No search results"]'))), "Element not found"
