from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import ctime

def option():
    options = Options()
    options.set_capability('pageLoadStrategy', 'normal')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    return options

def enter_search_page(wait):
    try:

        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[type="submit"]')))
        driver.find_element(By.CSS_SELECTOR, 
            'button[type="submit"]').click()

        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//span[@class="pri pri-search"]')))
        driver.find_element(By.XPATH, 
            '//span[@class="pri pri-search"]').click()
        driver.find_element(By.XPATH, 
            '//div[@class="flic-in"]/div').click()

        wait.until(EC.element_to_be_clickable(
            (By.ID, 'searchQuery')))           
        driver.find_element(By.ID, 
            'searchQuery').send_keys('Evergrande')
        driver.find_element(By.XPATH, 
            '//div[@class="toolbar-right"]/a').click()

    except Exception as e:
        print(e); driver.close()


def wait_for_element_location_to_be_stable(element):
    initial_location = element.location
    previous_location = initial_location
    start_time = time.time()
    while time.time() - start_time < 1:
        current_location = element.location
        if current_location != previous_location:
            previous_location = current_location
            start_time = time.time()
        time.sleep(0.4)

def scroll_articles(wait, scroll_bar, actionChains): 
    actionChains.move_to_element(scroll_bar).perform()
    scroll_bar.click()
    last_article = driver.find_elements(By.TAG_NAME, 'article')[-1]
    wait_for_element_location_to_be_stable(last_article)

if __name__ == "__main__":
    print(ctime())
    executable_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    url_login = "http://ezproxy.lb.polyu.edu.hk/login?url=https://www.pressreader.com/"

    driver = webdriver.Chrome(options=option(), executable_path=executable_path)
    driver.get(url_login)

    wait = WebDriverWait(driver, 30)
    enter_search_page(wait)

    actionChains = ActionChains(driver)
    scroll_bar = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='scroller']")))
    while scroll_bar:
        scroll_articles(wait, scroll_bar, actionChains)
    print(ctime())


print('Done ...')
