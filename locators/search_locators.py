from selenium.webdriver.common.by import By

from locators import Locator


class SearchPageLocators:
    @staticmethod
    def search_string():
       return Locator(By.CLASS_NAME, "gLFyf")

    @staticmethod
    def search_button():
        return Locator(By.CLASS_NAME, "gNO89b")

    @staticmethod
    def search_results():
        return Locator(By.PARTIAL_LINK_TEXT, "IT Test - complex industry IT solutions for business")

    @staticmethod
    def icon_ittest():
        return Locator(By.CLASS_NAME, "partial-logo")


