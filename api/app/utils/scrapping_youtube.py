import uyts
import flask
import flask_cors


class ScrappingYoutube:
    @staticmethod
    def search_song(phrase: str) -> str:
        query = 'Search query: %s' % '+'.join(phrase.split())
        search = uyts.Search(query)

        return 'https://www.youtube.com/watch?v=%s' % search.results[0].id
