import urllib.request
import json
from .models import Quote


def configure_request(app):
    global base_url
    base_url = app.config['QUOTES_API_BASE_URL']


def get_quotes():
    get_quotes_url = base_url

    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes = url.read()
        get_quotes_response = json.loads(get_quotes)

        quotes_results = None

        if get_quotes_response:
            quotes_list = get_quotes_response
            quotes_results = process_results(quotes_list)

        return quotes_results


def process_results(quotes_list):
    quotes_results = []
    for quote in quotes_list:
        id = quote.get('id')
        author = quote.get('author')
        quote = quote.get('quote')
        permalink = quote.get('permalink')

        if quote:
            quote_object = Quote(id, author, quote, permalink)

      return quotes_results
