from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view

from proxier.parsers import TradeMarkifyHTMLParser


@csrf_exempt
def trademarkify_habr_page(request, path):
    remote_url = 'http://habr.ru/' + path
    response = proxy_view(request, remote_url)

    parser = TradeMarkifyHTMLParser(response.content)
    response.content = parser.trademarkify()

    return response
