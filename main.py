import time
import re
import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from copy import copy

def __getstory__(text):
    textstory = []
    for y in text:
        if y.text == 'Welcome to r/AmITheAsshole. Please view our voting guide here, and remember to use only one ' \
                     'judgement in your comment.':
            break
        else:
            textstory.append(y.text)
    return textstory


def __getcomments__(text):
    textcomments = []
    Comments = False
    for y in text:
        if y.text == 'Welcome to r/AmITheAsshole. Please view our voting guide here, and remember to use only one judgement in your comment.':
            Comments = True
        else:
            if Comments:
                textcomments.append(y.text)
    return textcomments


def __play_audio__(text):
    driver.get("https://freetts.com/")
    driver.find_element(By.XPATH, "//select[@name='Voice']/option[text()='en-US-Standard-C']").click()
    driver.find_element(By.ID, 'TextMessage').send_keys(text)
    driver.find_element(By.XPATH, "//button[text()='Convert to Mp3']").click()
    time.sleep(8)
    driver.find_element(By.XPATH, "//button[text()='Download Mp3']").click()
    return 0


def __download_audio_offline__(text, reader):
    final_text = "This article was written by user " + text.author + ". Today's article is " + text.title + ". " + text.text

    reader.setProperty("rate", 150)
    reader.setProperty("volume", 1)
    print(text.title + "title should be here")
    location = "C:\\Users\\Josh\\Desktop\\" + re.sub('[^A-Za-z0-9]+', '', text.title)+ ".mp3"
    print(location)
    reader.save_to_file(final_text, location)
    reader.runAndWait()

    return 0


def __find_story__(browser, website):
    browser.get(website)

    storylisting = browser.find_elements(By.XPATH, "//a[@href]")
    namelist = []
    # denylist = {'Sign Up', 'Assk the Mods', 'Ask the Mods', "Frequently Assed Q's", "Resources", 'Hot', 'New', 'Top'}
    z = 0
    # approval = len(denylist)
    for x in storylisting:

        if x.text == '':
            storylisting.pop(z)

        else:
            if z > 12:
                namelist.append(x.text)
        z = z + 1

    return namelist


def __compile_story__(story):
    class storys:
        def __init__(self, title, author, text):
            self.title = title
            self.author = author
            self.text = text

    compiled = []
    user = storys('none', 'none', 'none')
    for x in story:

        if x[0: 4] == 'AITA' or x[0: 4] == 'WIBT':
            user.title = x
            continue

        if x[0: 2] == "u/":
            user.author = x[2: -1]
            continue
        if x[- 8: -1] == 'Comment':

            if user.author == 'none' and user.title == 'none':

                user.title = 'none'
                user.text = ''
                user.author = 'none'
                continue

            else:
                compiled.append(copy(user))
                user.text = user.text + (' ' + x)
                continue
        user.text = user.text + (' ' + x)
    return compiled


if __name__ == '__main__':
    reddit = []
    story = []
    comments = []
    speech = pyttsx3.init()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    storylist = []
    articlename = []

    url = "https://www.reddit.com/r/AmItheAsshole/new/"
    storylist = __find_story__(driver, url)

    reddit = __compile_story__(storylist)

    for x in reddit:


        __download_audio_offline__(x, speech)
print("Done")
driver.quit()
