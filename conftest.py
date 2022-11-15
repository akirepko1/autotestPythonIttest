import pathlib
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from datetime import datetime

from helpers.settings import SCREEN_ERROR_PATH
from pages.base_page import ConsoleLog

pytest.fixture
def driver(request, browser):
    if browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.headless = True
        wd = webdriver.Firefox(GeckoDriverManager().install(), options=options)
    elif browser == 'ie':
        wd = webdriver.Ie(IEDriverManager(os_type='Win32', version='3.1.0').install())
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument('window-size=1920x6500')
        options.add_argument('disable-search-geolocation-disclosure')
        options.add_argument('--disable-notifications')
        # options.add_argument('--enable-logging=stderr --log-level=0')
        wd = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # wd.implicitly_wait(IMPLICITLY_WAIT)
    # wd.set_page_load_timeout(PAGE_TIMEOUT)
    wd.maximize_window()

    print(f'\n\nЗапускаем тест {request.node.name}\n')

    yield wd

    try:
        if request.node.rep_call.failed and request.node.rep_setup.passed:
            current_time = datetime.now()
            dir_name = f'{SCREEN_ERROR_PATH}{current_time.strftime("%Y-%m-%d")}/{current_time.strftime("%H")}'
            pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
            now = current_time.strftime('_%d-%m-%Y_%H-%M-%S')
            img = f"{dir_name}/{request.node.name}{now}.png"
            print(f"##teamcity[publishArtifacts '{img}']")
            print(f"##teamcity[testMetadata type='image' value='{img}']")
            print(img)
            height = wd.execute_script("return document.body.scrollHeight")
            wd.set_window_size(1920, height + 100)
            wd.save_screenshot(img)
            ConsoleLog(driver=wd).print_log()

        if request.node.rep_call.passed:
            print(f'\nТест {request.node.name} прошел успешно!\n\n')
    except:
        pass
    finally:
        print('Завершаем тест, закрываем браузер')
        wd.quit()
