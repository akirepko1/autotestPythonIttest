import html
import traceback
import validators
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from helpers.settings import LONG_WAIT
from helpers.utils import try_to_retry, beautify_url



class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(self.driver)


    def open_page(self, url, url_path):
        pure_url = beautify_url(base_url=url, path=url_path)
        if validators.url(pure_url):
            print(f'\n\nПереходим на адрес {pure_url}')
            self.driver.get(f'{pure_url}')
            for i in range(0, 5):
                if (self.driver.title == "502 Bad Gateway"):
                    self.refresh_page()
            print(f'Зашли на страницу - {self.driver.title}')
        else:
            print(f'Введен невалидный url - {pure_url}')
            raise

    def refresh_page(self):
        self.driver.refresh()

    def wait_for_visibility_element(self, locator, time=LONG_WAIT):
        try:
            WebDriverWait(self.driver, time).until(EC.visibility_of_element_located((locator.by, locator.path)))
            print(f'Локатор {locator.path} появился')
        except WebDriverException:
            print('=============================================')
            print(f'Прошел таймаут {time} сек, но локатор {locator.path} не появился')
            print('=============================================')
            raise

    def wait_for_invisibility_element(self, locator, time=LONG_WAIT):
        try:
            WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located((locator.by, locator.path)))
            print(f'Локатор {locator.path} скрылся')
        except WebDriverException:
            print('=============================================')
            print(f'Прошел таймаут {time} сек, но локатор {locator.path} не скрылся')
            print('=============================================')
            raise

    def wait_for_presence_element(self, locator, time=LONG_WAIT):
        try:
            WebDriverWait(self.driver, time).until(EC.presence_of_element_located((locator.by, locator.path)))
            print(f'Локатор {locator.path} появился')
        except WebDriverException:
            print('=============================================')
            print(f'Прошел таймаут {time} сек, локатор {locator.path} не в DOMе')
            print('=============================================')
            raise

    def move_to_elem(self, locator):
        try:
            elem = self.driver.find_element(locator.by, locator.path)
            self.actions.move_to_element(elem).perform()
        except WebDriverException:
            print("Элемент не найден на странице")

    @try_to_retry()
    def set_text_input(self, locator, value, message=''):
        # WebDriverWait(self.driver, SHORT_WAIT).until(
        #     EC.visibility_of_element_located((locator.by, locator.path)))
        element = self.driver.find_element(locator.by, locator.path)
        # self.actions.move_to_element(element).click()
        self.scroll_to(element)
        element.click()
        element.clear()
        element.send_keys(value)
        assert value in element.get_attribute("value")
        # WebDriverWait(self.driver, SHORT_WAIT).until(
        #     EC.text_to_be_present_in_element_value((locator.by, locator.path), value))
        print(f'{message}: {element.get_attribute("value")}')

    @try_to_retry()
    def set_text_input_without_clear(self, locator, value, message=''):
        element = self.driver.find_element(locator.by, locator.path)
        self.scroll_to(element)
        element.click()
        element.send_keys(value)
        assert value in element.get_attribute("value")
        print(f'{message}: {element.get_attribute("value")}')

    @try_to_retry()
    def datepicker(self, locator, value, message=''):
        element = self.driver.find_element(locator.by, locator.path)
        self.scroll_to(element)
        element.click()
        element.clear()
        element.send_keys(value)
        element.send_keys(Keys.ESCAPE)
        assert value in element.get_attribute("value")
        print(f'{message}: {element.get_attribute("value")}')

    @try_to_retry()
    def datepicker_js(self, locator, script_locator, date, message=''):
        element = self.driver.find_element(locator.by, locator.path)
        assert element.is_displayed()
        self.driver.execute_script(
            f"$('{script_locator}').val('{date}').trigger('change');"
        )
        print(f'{message}: {element.get_attribute("value")}')

    @try_to_retry()
    def select(self, locator, option, message=''):
        element = Select(self.driver.find_element(locator.by, locator.path))
        element.select_by_visible_text(option)
        print(f'{message}: {option}')

    @try_to_retry()
    def first_select(self, locator, message=''):
        element = Select(self.driver.find_element(locator.by, locator.path))
        option = element.options[1]
        text = option.text
        element.select_by_visible_text(text)
        print(f'{message}: {text}')

    @try_to_retry()
    def radio_button(self, locator, message=''):
        element = self.driver.find_element(locator.by, locator.path)
        assert element.is_displayed()
        text = element.text
        element.click()
        assert element.is_enabled()
        print(f'{message}: {text}')

    @try_to_retry()
    def radio_button_new(self, locator, message='Установлен радио-баттон'):
        """
        Для корректной работы:
        1. локатор надо указывать ТОЛЬКО через XPATH
        2. XPATH должен указывать на input с name/id

        Пример:
        def reimbursement_method_repairs():
            return Locator(By.XPATH, '//input[@name="reimbursement-method-direct"]')
        """
        element = self.driver.find_element(
            locator.by,
            f'{locator.path}/following-sibling::div[@class="radio__indicatior"]')
        assert element.is_displayed()
        text = self.driver.find_element(locator.by, f'{locator.path}/parent::div/following-sibling::span')
        element.click()
        print(f'{message}: {text.text}')

    @try_to_retry()
    def set_checkbox(self, locator, message='Установлен чекбокс'):
        element = self.driver.find_element(locator.by, locator.path)
        self.scroll_to(element)
        # text = self.driver.find_element(
        #     locator.by,
        #     f'{locator.path}/parent::div/following-sibling::span')
        element.click()
        print(f'{message}')

    @try_to_retry()
    def checkbox(self, locator, message='Установлен чекбокс'):
        """
        Для корректной работы:
        1. локатор надо указывать ТОЛЬКО через XPATH
        2. XPATH должен указывать на input с name/id

        Пример:
        def is_insurer():
            return Locator(By.XPATH, '//input[@name="vzr-insurer-set-as-holder-0"]')
        """
        element = self.driver.find_element(
            locator.by,
            f'{locator.path}/following-sibling::div[@class="checkbox__indicatior"]'
        )
        self.scroll_to(element)
        text = self.driver.find_element(
            locator.by,
            f'{locator.path}/parent::div/following-sibling::span')
        element.click()
        print(f'{message}: {text.text}')

    @try_to_retry()
    def checkbox_re(self, locator, message='Установлен чекбокс'):
        """
        Для корректной работы:
        1. локатор надо указывать ТОЛЬКО через XPATH
        2. XPATH должен указывать на input с name/id

        Пример:
        def is_insurer():
            return Locator(By.XPATH, '//input[@name="vzr-insurer-set-as-holder-0"]')
        """
        text = self.driver.find_element(
            locator.by,
            f'{locator.path}/following-sibling::label/span[contains(@class, "checkbox__text")]')
        if not self.driver.find_element(locator.by, locator.path).is_selected():
            element = self.driver.find_element(
                locator.by,
                f'{locator.path}/following-sibling::label/*[local-name() = "svg"]')
            self.scroll_to(element)
            element.click()
            checkbox_status = self.driver.find_element(locator.by, locator.path)
            assert checkbox_status.is_selected(), f'Чекбокс с локатором {locator.path} не выбрался'
            print(f'{message}: {text.text}')
        else:
            print(f'Чекбокс: "{text.text}" уже установлен')

    @try_to_retry()
    def radiobutton_re(self, locator, value, message='Выбран вариант'):
        """
        Для корректной работы:
        1. локатор надо указывать ТОЛЬКО через XPATH
        2. XPATH должен указывать на input с name/id

        Пример:
        def is_insurer():
            return Locator(By.XPATH, '//input[@name="vzr-insurer-set-as-holder-0"]')
        """
        element = self.driver.find_element(
            locator.by,
            f'{locator.path}/following-sibling::label/span[contains(., "{value}")]')
        element.click()
        radiobutton_status = self.driver.find_element(
            locator.by,
            f'{locator.path}[following-sibling::label/span[contains(., "{value}")]]')
        assert radiobutton_status.is_selected(), f'Радио-баттон с локатором {locator.path} не выбрался'
        print(f'{message}: {element.text}')

    @try_to_retry()
    def button_click(self, locator, message='Нажали кнопку/ссылку'):
        element = self.driver.find_element(locator.by, locator.path)
        text = element.text
        self.scroll_to(element)
        element.click()
        print(f'{message}: {text}')

    @try_to_retry()
    def dadata(self, locator, value, message):
        """
                Для корректной работы:
                1. локатор надо указывать ТОЛЬКО через XPATH
                2. XPATH должен указывать на input с name/id

                Пример:
                def street():
                    return Locator(By.XPATH, '//input[@name="street"]')
        """
        suggest_value = self.glocator.dadata_value(locator.path, value)
        element = self.driver.find_element(locator.by, locator.path)
        self.scroll_to(element)
        # assert element.is_displayed()
        element.click()
        element.clear()
        element.send_keys(value)
        self.wait_for_visibility_element(self.glocator.dadata_suggests(locator.path), time=5)
        suggest = self.driver.find_element(suggest_value.by, suggest_value.path)
        # assert suggest.is_displayed()
        suggest.click()
        self.wait_for_invisibility_element(self.glocator.dadata_suggests(locator.path), time=5)
        element = self.driver.find_element(locator.by, locator.path)
        assert value in element.get_attribute("value")
        print(f'{message}: {value}')

    @try_to_retry()
    def button_click_js(self, locator, message='Нажали кнопку/ссылку'):
        element = self.driver.find_element(locator.by, locator.path)
        # assert element.is_displayed()
        assert element.is_enabled()
        text = element.text
        self.driver.execute_script(f'$("{locator.path}").click()')
        print(f'{message}: {text}')

    @try_to_retry()
    def attach_file(self, locator, value, message='Приложили файл'):
        element = self.driver.find_element(locator.by, locator.path)
        element.send_keys(value)
        print(f'{message}: {element.get_attribute("value")}')

    @try_to_retry()
    def attach_file_js(self, locator, value='6689190', message='Приложили файл с id='):
        element = self.driver.find_element(locator.by, locator.path)
        self.driver.execute_script(f"arguments[0].setAttribute('value', {value})", element)
        print(f'{message}{value}')

    def scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView("
            "{ block: 'center' });",
            element)
        return element

    @try_to_retry()
    def js_click(self, locator, message='Нажали кнопку/ссылку'):
        element = self.driver.find_element(locator.by, locator.path)
        self.driver.execute_script(
            "arguments[0].click();",
            element)
        print(f'{message}: {element.text}')
        return element

    @try_to_retry()
    def get_text(self, locator, message='Получили текст'):
        element = self.driver.find_element(locator.by, locator.path)
        text = element.text
        print(f'{message}: {text}')
        return text

    def close_modal_window(self):
        modal_elem = self.glocator.modal_window()
        close_button = self.glocator.mw_close_button()
        try:
            self.wait_for_visibility_element(modal_elem)
            self.button_link(close_button, message="Закрыли модальное окно")
            print("\nЗакрыли появившееся модальное окно")
        except NoSuchElementException:
            print("\nМодальное окно не появилось")
            pass


class ConsoleLog(BasePage):

    def get_console_log(self, locator):
        element = self.driver.find_elements(locator.by, locator.path)
        if len(element) > 0:
            for i in element:
                try:
                    raise Exception(html.unescape(i.get_attribute('innerHTML')))
                except Exception:
                    traceback.print_exc()




