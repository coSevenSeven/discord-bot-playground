from typing import Dict

from utils.ptt import Article


class Storage:
    ptt_articles: Dict[str, Article]

    def __init__(self):
        self.ptt_articles: Dict[str, Article] = {}
        print("storage initiation done")
