from django.contrib.algoliasearch import AlgoliaIndex


class SongIndex(AlgoliaIndex):
    fields = ('title', 'album')
    settings = {'attributesToIndex': ['title']}
    index_name = 'song_name_index'
