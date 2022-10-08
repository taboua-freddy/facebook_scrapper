class Post:

    def __init__(self) -> None:
        self._id = ""
        self._topic = ""
        self._text = ""
        self._images = []
        self._comments = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def text(self) -> str:
        return self._text

    @property
    def images(self) -> list:
        return self._images

    @property
    def comments(self) -> list:
        return self._comments

    def set_topic(self, topic):
        self._topic = topic

    def set_text(self, text):
        self._text = text

    def set_images(self, images: list):
        self._images = images

    def set_comments(self, comments: list):
        self._comments = comments

    def to_JSON(self) -> dict:
        """Transform object to JSON

        Returns:
            dict:
        """
        return {
            "topic": self.topic,
            "text": self.text,
            "images": self.images,
            "comments": self.comments
        }

    def to_object(self, post: dict):
        """Convert dict in post object

        Args:
            post (dict | None): provided data

        Returns:
            Post: post
        """
        if post is None:
            return self
        if post.get("_id") is not None:
            self._id = post["_id"]
        if post.get("topic") is not None:
            self.set_topic(post["topic"])
        if post.get("text") is not None:
            self.set_text(post["text"])
        if post.get("images") is not None:
            self.set_images(post["images"])
        if post.get("comments") is not None:
            self.set_comments(post["comments"])

        return self
