import time
from logininformation import MAIL, USERNAME, PASSWORD
from databaseMONGODB import *
from databaseMYSQL import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    InvalidSelectorException,
    ElementNotInteractableException,
    StaleElementReferenceException
)

# Screenshot kısımları. Program hata vermesi durumunda nerede hata verdiyse o anın ekran görüntüsünü alıp kaydediyor. Hatayı anlama açısından kolaylık sağlıyor.


driver = webdriver.Chrome()
time.sleep(2)
driver.maximize_window()
time.sleep(3)
driver.get("https://twitter.com/i/flow/login")
time.sleep(20)  # Sayfanın yüklenme süresine göre azaltılabilir veya arttırılabilir.


def loginToX():
    loginField = driver.find_element(by=By.TAG_NAME, value="input")
    time.sleep(2)
    loginField.send_keys(MAIL)
    time.sleep(3)

    loginField.send_keys(Keys.TAB)
    time.sleep(2)
    loginField.send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        loginField = driver.find_element(by=By.TAG_NAME, value="input")
        loginField.send_keys(USERNAME)
        time.sleep(2)
        loginField.send_keys(Keys.TAB)
        time.sleep(2)
        loginField.send_keys(Keys.ENTER)
        time.sleep(2)
        passwordField = driver.find_element(by=By.NAME, value="password")
        passwordField.send_keys(PASSWORD)
        time.sleep(2)
        for i in range(3):
            passwordField.send_keys(Keys.TAB)
            time.sleep(1)
        passwordField.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.save_screenshot("screenshotTRY-loginToX.png")
        print("Sorunu asma basarili.")
        time.sleep(5)
    except NoSuchElementException:
        loginField.send_keys(PASSWORD)
        time.sleep(2)

        for i in range(3):
            loginField.send_keys(Keys.TAB)
            time.sleep(1)
        loginField.send_keys(Keys.ENTER)
        driver.save_screenshot("screenshotEXCEPT-loginToX.png")

        time.sleep(5)
        driver.quit()
    else:
        driver.save_screenshot("screenshotELSE-loginToX.png")

        print("HATA YOK - LoginToX")
        time.sleep(5)

    finally:
        driver.save_screenshot("screenshotFINALLY-loginToX.png")

        print("TRY EXCEPT - FINAL-loginToX")
        time.sleep(5)


def getTweets():
    script = "document.body.style.zoom='50%';"
    driver.execute_script(script)
    try:
        time.sleep(2)

        tweetSender = driver.find_elements(
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/div/section/div/div/div/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a",
        )
        tweetContents = driver.find_elements(
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[5]/div/section/div/div/div/div/div/article/div/div/div[2]/div[2]/div[2]/div/span"
        )
        sql = "INSERT INTO <table_name> (username,postcontent) VALUES (%s, %s)"
        counter = 1
        for sender, contents in zip(tweetSender, tweetContents):
            try:
                print(counter, " - Tweet Gönderen Kisi: ", sender.text)
                print(counter, " - Tweet İçeriği: ", contents.text)
                
                ### MongoDB
                tweetDict = {"Tweeti Paylaşan Kişi":sender.text,"Tweet İçeriği":contents.text}
                mongoCollection.insert_one(tweetDict)
                ###
                
                ### MySQL
                val = (sender.text,contents.text)
                mycursor.execute(sql,val)
                mydb.commit()
                ###
                print(mycursor.rowcount,"record inserted.")
                print("\n\n")

                time.sleep(1)
                counter += 1
                
            except StaleElementReferenceException:
                print("CEKILECEK TWEET VERISI BULUNAMADI.")
                
        print("Tweet Çekme işlemi başarılı.")
        time.sleep(5)
        driver.save_screenshot("screenshotTRY-getTweets.png")
        driver.quit()
    except NoSuchElementException:
        print("Tweet Çekilemedi.")
        driver.save_screenshot("screenshotEXCEPT-getTweets.png")
    except InvalidSelectorException:
        print("Invalid Selector Inception.")
    except ElementNotInteractableException:
        print("ElementNotInteractableException")
