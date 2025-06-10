from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Replace these with your actual credentials
USERNAME = "Shreya_26"
PASSWORD = "honeychilly26"


def login_and_scrape():
    options = Options()
    options.add_argument("--start-maximized")

    print("🚀 Launching browser...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("🔐 Opening login page...")
        driver.get("https://discourse.onlinedegree.iitm.ac.in/login")

        print("📝 Filling in credentials...")
        time.sleep(3)  # Wait for page to load

        driver.find_element(By.ID, "login-account-name").send_keys(USERNAME)
        driver.find_element(By.ID, "login-account-password").send_keys(PASSWORD)

        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()

        print("⏳ Waiting for login to complete...")
        time.sleep(5)  # Adjust this depending on internet speed

        print("📄 Navigating to posts page...")
        driver.get("https://discourse.onlinedegree.iitm.ac.in/latest")

        time.sleep(5)
        posts = driver.find_elements(By.CLASS_NAME, "title")

        print(f"✅ Found {len(posts)} posts:")
        for i, post in enumerate(posts, start=1):
            print(f"{i}. {post.text}")

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    login_and_scrape()
