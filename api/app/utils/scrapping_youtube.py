import uyts


class ScrappingYoutube:
    @staticmethod
    def search_song(phrase: str) -> str:
        query = 'Search query: %s' % '+'.join(phrase.split())
        search = uyts.Search(query)

        return search.results[0].id
