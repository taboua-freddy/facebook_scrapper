import json
import os
from bs4 import BeautifulSoup
from time import sleep

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv, find_dotenv
from .mongo_db import PostDB
from .post import Post

from .utils import image_as_base64

load_dotenv(find_dotenv())

class FacebookScraper:
    """This class scrapes post on Facebook
    """
    def __init__(self, EMAIL: str, PASSWORD: str) -> None:
        self._login_page = "https://m.facebook.com/"
        self._search_url = "https://m.facebook.com/search/posts/?q={}&source=filter&isTrending=0&tsid=0.14935919284721044"
        self._post_url = "https://m.facebook.com/story.php?story_fbid={}&id={}&eav=AfaaD4rwbd3CHZ2A2HbT-m9DmyFPqb_szlYYjo5IkSJyhLL4VX7eUp_K7s0_jyzG1rw&paipv=0"
        chrome_driver_path = os.environ.get("CHROME_DRIVER_PATH")

        chrome_option = Options()
        chrome_option.add_argument('--disable-notifications')
        #chrome_option.add_argument("--no-startup-window")

        self._driver = webdriver.Chrome(
            chrome_driver_path, options=chrome_option)

        #get login page
        self._driver.get(self._login_page)

        #get input form
        username = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        password = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

        # enter username and password
        username.clear()
        username.send_keys(EMAIL)
        password.clear()
        password.send_keys(PASSWORD)

        #clic on login button
        button = WebDriverWait(self._driver, 2).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[value='Log in']"))).click()

    @property
    def get_driver(self) -> webdriver:
        return self._driver

    def scrap_post(self, word: str) -> list:
        """Scrap posts according to a key word

        Args:
            word (str): _description_

        Returns:
            json: posts data
        """        
        sleep(5)
        data = []
        # post url
        url = self._search_url.format(word)

        #post page
        self._driver.get(url)
        sleep(5)

        #self._driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #scrapping posts url
        soup = BeautifulSoup(self._driver.page_source, "html.parser")

        posts = soup.find_all("a", {"class": "_5msj _26yo"})
        urls = []
        print("Strating scrapping---->>>>>>>>>>>")
        for n,post in enumerate(posts,1):
            print(f"Post number {n}/{len(posts)} is scrapping. Please wait......... ")
            url = post["href"]
            if not url.startswith("https://"):
                url = self._login_page[:-1]+url
            urls.append(url)

        for url in urls:
            sleep(5)
            self._driver.get(url)
            
            #for each url save text, comments and images
            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            text = soup.find("div", {"class": "_5rgt _5nk5"}).string
            text = self._driver.find_element(
                By.XPATH, "//div[contains(@class, '_5rgt _5nk5')]").text

            images_tags = soup.find(
                "div", {"class": "_5rgu _7dc9 _27x0"}).find_all("a")

            url_images = []
            for tag in images_tags:
                url = tag["href"]
                if not url.startswith("https://"):
                    url = self._login_page[:-1]+url
                url_images.append(image_as_base64(url))

            comments = {}
            comments_tags = soup.find_all("div", {"class": "_2a_i"})
            for tag in comments_tags:
                author = tag.find("div", {"class": "_2b05"})
                comment = author.find_next("div")
                comments[author.string] = comment.string

            data.append({
                "text": text,
                "images": url_images,
                "comments": list(comments.values()),
                "topic": word
            })

        return data


if __name__ == "__main__":
    EMAIL = os.environ.get("EMAIL")
    PASSWORD = os.environ.get("PASSWORD")
    topic = "iphone"
    fs = FacebookScraper(EMAIL, PASSWORD)
    db = PostDB()
    data = fs.scrap_post(topic)

    for i, d in enumerate(data):
        data[i] = (Post()).to_object(d).to_JSON()
    
    print("Saving is starting.......")
    if db.topic_exist(topic):
        print("Would you like to replace by the new one ?")
        response = True
        if response:
            db.delete_by_topic(topic)
            db.add_posts(data)
            print("New posts added")
        else:
            print("Noting has been changed ")
    else:
        db.add_posts(data)
        print("New posts added")

    #fs.get_driver.quit()

    