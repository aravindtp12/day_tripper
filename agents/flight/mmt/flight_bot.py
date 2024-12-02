from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime


class MakeMyTripBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.home_url)
        time.sleep(2)
        self.wait = WebDriverWait(self.driver, 10)

    @property
    def home_url(self):
        return "https://www.makemytrip.com/"

    def enter_num_travellers(self, num_travellers):
        pass

    def enter_date_and_destination(self, from_city, to_city, departure_date):
        departure_date_object = datetime.strptime(departure_date, "%Y-%m-%d")
        departure_day_abbr = departure_date_object.strftime("%a")
        year, month, day = departure_date.split('-')
        month_abbr = departure_date_object.strftime("%B")

        try:
            close_button = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[data-cy="closeModal"]'))
            )
            close_button.click()
        except:
            pass  # No pop-up present

        # From City
        from_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "fromCity"))
        )
        from_field.click()
        from_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From']"))
        )
        from_input.send_keys(from_city)
        time.sleep(2)
        from_suggestion = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[@role='option']"))
        )
        from_suggestion.click()

        # To City
        to_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "toCity"))
        )
        to_field.click()
        to_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='To']"))
        )
        to_input.send_keys(to_city)
        time.sleep(2)
        to_suggestion = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[@role='option']"))
        )
        to_suggestion.click()

        time.sleep(2)

        target_month = f"{month_abbr} {year}"

        # Loop until the correct month is visible
        while True:
            # Check if the target month is displayed
            month_display = self.driver.find_element(By.CSS_SELECTOR, "div.DayPicker-Caption div").text
            if month_display == target_month:
                break

            # Click the next month arrow if the target month is not yet displayed
            next_button = self.driver.find_element(By.XPATH, "//span[@aria-label='Next Month']")
            next_button.click()

        month_abbr = departure_date_object.strftime("%b")
        date_xpath = f"//div[@aria-label='{departure_day_abbr} {month_abbr} {day} {year}']"
        date_element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, date_xpath))
        )
        date_element.click()
        time.sleep(2)

    def search_submit(self):
        search_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//p[@data-cy='submit']//a[@class='primaryBtn font24 latoBold widgetSearchBtn ']")))
        search_button.click()

    def search_flights(self, from_city, to_city, departure_date, num_travellers=1):
        try:
            self.enter_date_and_destination(from_city, to_city, departure_date)
            self.enter_num_travellers(num_travellers)
            self.search_submit()
            print("done")
        finally:
            print("done")
            # self.driver.quit()


bot = MakeMyTripBot()
bot.search_flights("mumbai", "delhi", "2025-08-01")

