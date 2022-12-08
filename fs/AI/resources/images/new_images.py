from sre_parse import CATEGORIES
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import numpy as np

# # open Chrome browser
# driver = webdriver.Chrome("C:/Product/Family-Savior/src/chromedriver/chromedriver.exe")

# driver.get('https://www.google.com/')

# function 
def get_images(no_of_img, name, driver):
    # open search bar and write 
    box = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    box.send_keys(name)
    box.send_keys(Keys.ENTER)

    # go to images 
    driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()

    # for scrolling down
    #Will keep scrolling down the webpage until it cannot scroll no more
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height

    
    for i in range(no_of_img):
        # escape from replacing same index images  
        img_nam = np.random.randint(1,50000)
        # skip first 10 items
        driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div['+str(i+10)+']/a[1]/div[1]/img').screenshot('C:/Product/Family-Savior/src/data/Images/('+str(img_nam)+').png')
    driver.close()    

# --------------- Getting images ------------------ #

CATEGORIES =['Refrigerator','Bed', 'Iron','Washing Machine','Tabel','showcase',
'sofa','lamp','Wardrobe','smart phone','Laptop','Tablet','Jumar','Computer','TV','UPS','Wifi','Dining Tabel','Basin','Vacuum Cleaner','Oven','Sewing machine','Dog','Cate','Parrot','fishes','pets']

for c in  CATEGORIES:
    # open Chrome browser
    driver = webdriver.Chrome("C:/Product/Family-Savior/src/chromedriver/chromedriver.exe")
    driver.get('https://www.google.com/')
    get_images(5, c, driver)


