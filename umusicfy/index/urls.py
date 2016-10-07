
from django.conf.urls import url

# Import Class Based Views
from .views import IndexView

urlpatterns = (
    url(r'^$', IndexView.as_view(), name='index_view'),
)
