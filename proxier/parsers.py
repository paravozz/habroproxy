import re

from bs4 import BeautifulSoup, NavigableString
from bs4.element import PreformattedString


class TradeMarkifyHTMLParser:
    _list_of_bad_names = ['style', 'script']  # мы же не хотим все сломать
    _list_of_link_attrs = ['src', 'href', 'xlink:href']

    def __init__(self, html_doc):
        self._soup = BeautifulSoup(html_doc, 'html5lib')

    def _six_symbol_words_replacer(self, string_for_replace):
        new_string = re.sub(
            r'(\b\w{6}\b)',
            r'\1' + '\u2122',
            str(string_for_replace)
        )
        return new_string

    def _transform_tag_content(self, content):
        new_content = []

        for el in content:
            # нужны только строки, не комменты, и не всякое разное
            is_nav_string = isinstance(el, NavigableString) \
                            and not isinstance(el, PreformattedString)

            if is_nav_string:
                new_string = self._six_symbol_words_replacer(el)
                new_string = NavigableString(new_string)
            else:
                new_string = el

            new_content.append(new_string)

        return new_content

    def trademarkify(self):
        for tag in self._soup.find_all():
            if tag.name in self._list_of_bad_names:
                continue

            for attr in self._list_of_link_attrs:  # заменяем ссылки
                try:  # потому что hasattr иногда ложно-положительный
                    tag[attr] = tag[attr].replace("https://habr.com",
                                                  "http://127.0.0.1:6969")
                except KeyError:
                    pass

            if tag.contents:
                tag.contents = self._transform_tag_content(tag.contents)

        return self._soup.prettify(formatter=None)
