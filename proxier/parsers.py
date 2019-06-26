import re

from bs4 import BeautifulSoup, NavigableString
from bs4.element import PreformattedString


class TradeMarkifyHTMLParser:
    list_of_bad_names = ['style', 'script']  # мы же не хотим все сломать

    def __init__(self, html_doc):
        self._soup = BeautifulSoup(html_doc, 'html.parser')

    def _six_symbol_words_replacer(self, string_for_replace):
        new_string = re.sub(
            r'(\b\w{6}\b)',
            r'\1' + '\u2122',
            str(string_for_replace)
        )
        return new_string

    def trademarkify(self):
        for tag in self._soup.find_all():
            if tag.name in self.list_of_bad_names:
                continue

            if tag.name == 'a':
                try:  # потому что hasattr иногда ложно-положительный
                    tag['href'] = tag['href'].replace("https://habr.com",
                                                      "http://127.0.0.1:6969")
                except KeyError:
                    continue

            if tag.contents:
                new_contents = []

                for el in tag.contents:
                    # нужны только строки, не комменты, и не всякое разное
                    if isinstance(el, NavigableString) \
                            and not isinstance(el, PreformattedString):
                        new_string = self._six_symbol_words_replacer(el)
                        new_contents.append(NavigableString(new_string))
                    else:
                        new_contents.append(el)

                tag.contents = new_contents

        return str(self._soup)
