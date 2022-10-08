import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

from .post import Post

load_dotenv(find_dotenv())

MONGO_PWD = os.environ.get("MONGO_PWD")

class PostDB:
    """This class provides data access to post collection in MongoDB
    """
    def __init__(self) -> None:

        try:
            self._client = MongoClient(
                f"mongodb+srv://freddy:{MONGO_PWD}@cluster0.hrmoxr3.mongodb.net/?retryWrites=true&w=majority")
        except:
            print("Something went wrong during the connection to the database!")
            self._client = None

        self._db = self._client.smart

        self._collection = self._db.post

    # @property
    # def _db(self)-> MongoClient.Database:
    # self._db

    @property
    def client_not_exist(self) -> bool:
        return self._client is None

    def add_post(self, post: Post):
        if self.client_not_exist:
            return None
            
        return self._collection.insert_one(post).inserted_id

    def add_posts(self, posts: list):
        if self.client_not_exist or len(posts) == 0:
            return None

        self._collection.insert_many(posts)

    def find_one_by_topic(self, topic: str) -> Post:
        if self.client_not_exist:
            return None

        post = self._collection.find_one({"topic": topic})
        return Post().to_object(post)

    def delete_by_topic(self, topic: str):
        if self.client_not_exist:
            return None

        self._collection.delete_many({"topic": topic})

    def topic_exist(self, topic: str):
        if self.client_not_exist:
            return None

        post = self.find_one_by_topic(topic)
        return post.id is not ""

    def get_posts_by_topic(self, topic: str) -> list:
        if self.client_not_exist:
            return None

        tmp_posts = self._collection.find({"topic": topic})
        posts = []
        for post in tmp_posts:
            posts.append(Post().to_object(post))

        return posts


if __name__ == "__main__":
    client = MongoClient(
        f"mongodb+srv://freddy:32323@cluster0.hrmoxr3.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    print(client.is_mongos)
