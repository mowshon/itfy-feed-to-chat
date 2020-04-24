from selenium import webdriver
from PIL import Image
import os

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

def take_screenshot(link):
    driver.get(link)
    element = driver.find_elements_by_class_name("message-cell--main")[0]
    location = element.location
    size = element.size
    driver.save_screenshot("screenshot.png")

    # crop image
    x = location['x']
    y = location['y']
    width = location['x']+size['width']
    height = location['y']+size['height']
    im = Image.open('screenshot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save('attachement.png')
    os.remove("screenshot.png")
    driver.quit()
    return True
