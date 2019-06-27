import pytest

from proxier.parsers import TradeMarkifyHTMLParser


@pytest.fixture
def simple_html_markup():
    return '<html>' \
           '<head><title>В этом слове девять букв</title></head>' \
           '<body>' \
           '<span>Cловцо из шести букофф +40</span>' \
           '<a href="https://habr.com/test/url/">шиесть</a>' \
           '</body>' \
           '</html>'


@pytest.fixture
def parser(simple_html_markup):
    return TradeMarkifyHTMLParser(simple_html_markup)


def test_parser(parser, simple_html_markup):
    assert parser

    new_markup = parser.trademarkify()

    assert new_markup != simple_html_markup

    expected_markup = '<html>' \
                      '<head><title>В этом слове девять™ букв</title></head>' \
                      '<body>' \
                      '<span>Cловцо™ из шести букофф™ +40</span>' \
                      '<a href="http://127.0.0.1:6969/test/url/">шиесть™</a>' \
                      '</body>' \
                      '</html>'

    assert str(new_markup) == str(expected_markup)
