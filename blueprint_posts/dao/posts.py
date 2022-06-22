class Post:
    """
    Абстракция постов для использования в DAO
    """

    def __init__(self, poster_name="",
                 poster_avatar="",
                 pic="",
                 content="",
                 views_count=0,
                 likes_count=0,
                 pk=0
                 ):
        self.poster_name = poster_name
        self.poster_avatar = poster_avatar
        self.pic = pic
        self.content = content
        self.views_count = views_count
        self.likes_count = likes_count
        self.pk = pk

    def __repr__(self):
        return f"Post(" \
               f"{self.poster_name}, " \
               f"{self.poster_avatar}, " \
               f"{self.pic}, " \
               f"{self.content}, " \
               f"{self.views_count} ," \
               f"{self.likes_count}, " \
               f"{self.pk}" \
               f")"

    def as_dict(self):
        dict_dat = {
            "poster_name": self.poster_name ,
            "poster_avatar": self.poster_avatar,
            "pic": self.pic,
            "content": self.content,
            "views_count": self.poster_name,
            "likes_count": self.likes_count,
            "pk": self.pk,
        }

        return dict_dat
