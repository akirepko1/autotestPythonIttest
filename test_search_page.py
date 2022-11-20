import pytest


from .pages.search_page import SearchPage


def test_search_ittest(driver):
    link = "https://www.google.ru/"
    page = SearchPage(driver, link)
    page.open_page()
    page.search()
    page.search_check()

