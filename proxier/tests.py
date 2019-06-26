import pytest

from proxier.parsers import TradeMarkifyHTMLParser


@pytest.fixture
def simple_html_markup():
    return '<html>' \
           '<head><title>В этом слове девять букв</title></head>' \
           '<body><span>Cловцо из шести букофф</span></body>' \
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
                      '<body><span>Cловцо™ из шести букофф™</span></body>' \
                      '</html>'

    assert str(new_markup) == str(expected_markup)
