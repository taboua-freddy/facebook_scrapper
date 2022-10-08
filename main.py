import argparse
from time import sleep

from packages.mongo_db import PostDB
from packages.post import Post
from packages.facebook_scaper import FacebookScraper

def run():
    """facebook-scraper entry point when used as a script"""
    parser = argparse.ArgumentParser(
        prog='facebook-scraper',
        description="Scrape Facebook post according a topic",
    )
    parser.add_argument('--email', type=str, help="provide your email or phone number")
    parser.add_argument('--password', type=str, help="provide your password's account")
    parser.add_argument('-t', type=str, help="provide the topic to search")
    parser.add_argument('--erase_exist', default="True", type=bool, help="erase topic in db if exists")

    args = parser.parse_args()
    
    EMAIL = args.email
    PASSWORD = args.password
    topic = args.t

    fs = FacebookScraper(EMAIL, PASSWORD)
    db = PostDB()
    data = fs.scrap_post(topic)

    for i, d in enumerate(data):
        data[i] = (Post()).to_object(d).to_JSON()

    print("Saving is starting.......")
    if db.topic_exist(topic):
        if args.erase_exist:
            print(f"Topic {topic} is already there it will be detected")
            db.delete_by_topic(topic)
            db.add_posts(data)
            print("New posts replaced")
        else:
            print(f"Topic {topic} is already there Noting has been changed ")
    else:
        db.add_posts(data)
        print("New posts added")

    fs.get_driver.quit()


if __name__ == '__main__':
    run()
