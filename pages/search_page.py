from .base_page import BasePage
from locators.search_locators import SearchPageLocators


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locator = SearchPageLocators()

    def search(self):
        self.wait_for_invisibility_element(self.locator.search_string())
        self.set_text_input(self.locator.search_string(), value="IT Test",
                            message="Ввели в поиск IT Test")
