import requests


class ScrappingNews:
    @staticmethod
    def search_song(phrase: str, number: int = None) -> str:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept-Language': 'en'
        }

        response = requests.get('https://saurav.tech/NewsAPI/everything/cnn.json', headers=headers)
        response_json = response.json()
        articles = response_json['articles']
        total_results = response_json['totalResults']

        url = response_json['articles'][number]['url'] if number % total_results else response_json['articles'][0][
            'url']
        return url