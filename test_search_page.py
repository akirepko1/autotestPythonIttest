import pytest


from .pages.search_page import SearchPage

url = "https://www.google.ru/"
url_path=""
def test_search_ittest(driver):
    page = SearchPage(driver)
    page.open_page(url, url_path)
    page.search()
    page.search_check()

def test_negative_search_ittest(driver):
    page = SearchPage(driver)
    page.open_page(url, url_path)
    page.search()
    page.search_check()
