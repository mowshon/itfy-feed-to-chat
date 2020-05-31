import pytest
import time
import json
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def add_tp_pass(log, password, message):
    def wait_for_window(timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = driver.window_handles
        wh_then = vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options)
    vars = {}
    driver.get("https://dialogflow.cloud.google.com/")
    driver.set_window_size(1456, 876)
    vars["window_handles"] = driver.window_handles
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".md-btn-login-image-wrapper").click()
    vars["win3607"] = wait_for_window(2000)
    vars["root"] = driver.current_window_handle
    driver.switch_to.window(vars["win3607"])
    driver.find_element(By.ID, "identifierId").send_keys(f"{log}")
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys(f"{password}")
    driver.find_element(By.ID, "passwordNext").click()
    driver.close()
    time.sleep(3)
    driver.switch_to.window(vars["root"])
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".md-btn-login-image-wrapper").click()
    time.sleep(8)
    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[2]/ul/li[2]/intents-list-item/div/div/span/span[2]/span').click()
    time.sleep(8)
    driver.find_element(By.XPATH,
                        "/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[1]/intent-user-says-editor/div[2]/div[1]/user-says-editor/div/div/div[1]/div").click()
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[1]/intent-user-says-editor/div[2]/div[1]/user-says-editor/div/div/div[1]/div")
    element.click()
    time.sleep(1)
    mousedown = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[1]/intent-user-says-editor/div[2]/div[2]/user-says-editor[2]/div/div/button/i")
    mousedown.click()
    time.sleep(1)
    element.click()
    element.send_keys(f"{message}")
    driver.find_element(By.XPATH, '//*[@id="multi-button"]').click()
    time.sleep(5)
    driver.quit()


def add_tp_help(log, password, message):
    def wait_for_window(timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = driver.window_handles
        wh_then = vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options)
    vars = {}
    driver.get("https://dialogflow.cloud.google.com/")
    driver.set_window_size(1456, 876)
    vars["window_handles"] = driver.window_handles
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".md-btn-login-image-wrapper").click()
    vars["win3607"] = wait_for_window(2000)
    vars["root"] = driver.current_window_handle
    driver.switch_to.window(vars["win3607"])
    driver.find_element(By.ID, "identifierId").send_keys(f"{log}")
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys(f"{password}")
    driver.find_element(By.ID, "passwordNext").click()
    driver.close()
    time.sleep(3)
    driver.switch_to.window(vars["root"])
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".md-btn-login-image-wrapper").click()
    time.sleep(8)
    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[2]/ul/li[1]/intents-list-item/div/div/span').click()
    time.sleep(8)
    driver.find_element(By.XPATH,
                        "/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[1]/intent-user-says-editor/div[2]/div[1]/user-says-editor/div/div/div[1]/div").click()
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[1]/intent-user-says-editor/div[2]/div[1]/user-says-editor/div/div/div[1]/div")
    element.click()
    time.sleep(1)
    mousedown = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div/div/section/div/div[3]/div/div/div[1]/intent-user-says-editor/div[2]/div[2]/user-says-editor[2]/div/div/button/i")
    mousedown.click()
    time.sleep(1)
    element.click()
    element.send_keys(f"{message}")
    driver.find_element(By.XPATH, '//*[@id="multi-button"]').click()
    time.sleep(5)
    driver.quit()