from django.conf.urls import url

from proxier.views import trademarkify_habr_page

urlpatterns = [
    url('(?P<path>.*)', trademarkify_habr_page),
]
