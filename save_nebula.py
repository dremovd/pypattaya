from selenium import webdriver
import time

def _set_up():
    """A method to set up the browser's driver."""
    import os

    # Set basic variables.
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # Do not wait for full page load

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values':
                 {'disk-cache-size': 4096, 'plugins': 2, 'popups': 2, 'geolocation': 2,
                  'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 1,
                  'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                  'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                  'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                  'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                  'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                  'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)

    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    # Set headless mode for Chrome (not showing the browser window).
    # options.add_argument("headless")

    driver = webdriver.Chrome(options=options, desired_capabilities=caps,
                              executable_path=os.path.join(os.path.dirname(__file__), '/usr/bin/chromedriver'))

    driver.implicitly_wait(10)

    return driver


def _wait_load(driver, selector_to_check):
    """A method to wait until element appears on the page"""
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    timeout = 300

    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, selector_to_check))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        return "Timed out waiting for page to load."
    finally:
        return "Page loaded."

def _scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height


def _tear_down(driver):
    """A method to destroy the driver and close the browser window."""
    driver.quit()


if __name__ == '__main__':
    """A script to download all the PDF papers from Nebula library."""

    driver = _set_up()
    driver.get('https://portal.nebula.org/login')

    # Waits until the manual login.
    _wait_load(driver, 'div .result-ready-dashboard')
    time.sleep(2)

    driver.get('https://portal.nebula.org/reporting/library')
    _wait_load(driver, 'div .papers-component-body')
    time.sleep(2)
    _scroll_down(driver)
    time.sleep(10)

    result = driver.find_elements_by_class_name('button-div')
    # print(len(result))

    for paper in result:
        paper.click()
        time.sleep(1)
        result_share = driver.find_elements_by_class_name('share-text-download')
        result_share[1].click()
        time.sleep(3)
        driver.find_element_by_class_name('fa-arrow-left').click()

    time.sleep(20)

    _tear_down(driver)
