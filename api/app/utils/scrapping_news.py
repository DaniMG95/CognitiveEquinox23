from newscatcher import Newscatcher

class ScrappingNews:
    @staticmethod
    def search_news(number: int = None) -> str:
        nc = Newscatcher(website='nytimes.com')
        results = nc.get_news()
        articles = results['articles']
        url = articles[number]['link'] if number % len(articles) else articles[0]['url']

        return url
