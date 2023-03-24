import random
from newscatcher import Newscatcher


class ScrappingNews:
    @staticmethod
    def search_news() -> str:
        nc = Newscatcher(website='nytimes.com')
        results = nc.get_news()
        articles = results['articles']
        url = random.choice(articles)['link']

        return url
