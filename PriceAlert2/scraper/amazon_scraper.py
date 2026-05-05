from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def get_product_details(driver, url):
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)
        price_container = wait.until(
            EC.presence_of_element_located((By.ID, "corePriceDisplay_desktop_feature_div"))
        )

        whole = price_container.find_element(By.CLASS_NAME, "a-price-whole").text
        try:
            fraction = price_container.find_element(By.CLASS_NAME, "a-price-fraction").text
        except: 
            fraction= ""
        price = float((whole + fraction).replace(",", ""))
        title_element = wait.until(
        EC.presence_of_element_located((By.ID, "productTitle"))
        )
        title = title_element.text.strip()
        return price, title

    except Exception as e:
        print("Error:", e)
        return None