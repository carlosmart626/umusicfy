from django.contrib.algoliasearch import AlgoliaIndex


class SongIndex(AlgoliaIndex):
    fields = ('title', 'album', 'rating')
    settings = {'attributesToIndex': ['title', 'rating']}
    index_name = 'song_name_index'
