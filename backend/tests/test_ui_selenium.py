

# backend/tests/test_ui_selenium.py

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")


@pytest.fixture
def driver():

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    yield driver
    driver.quit()


@pytest.mark.ui
@pytest.mark.integration
def test_homepage_title_and_form_elements(driver):
    driver.get(BASE_URL)

    # מחכים שכותרת העמוד תופיע
    h1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Currency Converter" in h1.text

    # input של amount
    amount_input = driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
    assert amount_input is not None

    # שני ה-selects (From, To)
    selects = driver.find_elements(By.TAG_NAME, "select")
    assert len(selects) == 2

    # כפתור Convert
    button = driver.find_element(By.TAG_NAME, "button")
    assert "Convert" in button.text or "Converting" in button.text
    time.sleep(3)


# @pytest.mark.ui
# @pytest.mark.integration
# def test_convert_flow(driver):
#     """בודק זרימת המרה מלאה דרך ה-UI."""
#     driver.get(BASE_URL)

#     # קלט amount
#     amount_input = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="number"]'))
#     )
#     amount_input.clear()
#     amount_input.send_keys("100")

#     # בוחרים From ו-To
#     selects = driver.find_elements(By.TAG_NAME, "select")
#     assert len(selects) == 2

#     from_select = Select(selects[0])
#     to_select = Select(selects[1])

#     from_select.select_by_value("USD")
#     to_select.select_by_value("EUR")

#     # לוחצים על כפתור Convert
#     button = driver.find_element(By.TAG_NAME, "button")
#     button.click()

#     # מחכים שיתקבל תוצאה (strong בתוך ה-result box)
#     result_strong = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "strong"))
#     )
    
#     time.sleep(10)
#     text = result_strong.text  # למשל: "91.23 EUR"
#     # בודקים שיש שם EUR ושזה לא ריק
#     assert "EUR" in text
#     assert len(text.strip()) > 0




# pytest -m "ui"
# pytest tests/test_ui_selenium.py -m ui
