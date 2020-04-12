from rest_framework.filters import SearchFilter


class SongSearch(SearchFilter):

    def get_search_fields(self, view, request):
        field = request.query_params.get('search_for')
        if field == 'genre':
            field = 'genre'
        elif field == 'album':
            field = 'album__name'
        elif field == 'artist':
            field = 'album__artist__name'
        else:
            field = 'title'
        return [field]
