import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import pandas as pd

# Setup Faker for generating random user data
fake = Faker()

# Generate random email and password components for testing
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Function to set up Chrome with Selenium
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Anti-detection
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to create Gmail account
def create_gmail_account(driver):
    driver.get("https://accounts.google.com/signup")
    
    # Use WebDriverWait to ensure elements load before interacting
    wait = WebDriverWait(driver, 15)

    # Generate random user details
    first_name = fake.first_name()
    last_name = fake.last_name()

    # Step 1: Fill out name and click 'Next'
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='First name']"))).send_keys(first_name)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='lastName']"))).send_keys(last_name)
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()
    time.sleep(2)  # Wait for the next page to load

    # Step 2: Fill out birthday and gender
    # Randomly generate date of birth
    day = random.randint(1, 28)
    month = random.choice(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    year = random.randint(1980, 2003)
    gender = random.choice(['Male', 'Female'])

    # Enter the day
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Day']"))).send_keys(day)
    
    # Select the month
    # month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id="month"]")))
    month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='month']/option[1]")))
    month_dropdown.click()
    driver.find_element(By.XPATH, f"//option[text()='{month}']").click()
    
    # Enter the year
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Year']"))).send_keys(year)
    
    # Select gender
    # gender_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id="gender"]")))
    gender_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gender']")))
    
    gender_dropdown.click()
    driver.find_element(By.XPATH, f"//option[text()='{gender}']").click()
    
    # Click 'Next' to proceed
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()
    time.sleep(5)  # Wait for the next page to load

    # Step 3: Enter Username and Password
    # Generate username and password
    username = f"{first_name.lower()}{random.randint(1, 1000)}.{last_name.lower()}"
    password = generate_random_string(12) + "!"

    # Enter the username
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Username']"))).send_keys(username)
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()
    time.sleep(2)  # Wait for the next page to load

    # Enter the password and confirm password
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Password']"))).send_keys(password)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Confirm']"))).send_keys(password)
    
    # Click 'Next' to finish this section
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()
    time.sleep(5)  # Wait for the next page to load
    # Skip phone number
    try:
        # Click "Skip" if phone number prompt appears
        skip_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button/span[contains(text(), 'Skip')]")))
        skip_button.click()
    except:
        print("Phone number step may be required.")
        return None  # If skipping is not possible, end process

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{username}@gmail.com",
        "password": password,
        "day": day,
        "month": month,
        "year": year,
        "gender": gender
    }

# Save credentials to a CSV file
def save_credentials_to_csv(data, filename="gmail_credentials.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Credentials saved to {filename}")

# Main execution
def main():
    driver = setup_driver()
    credentials_list = []

    try:
        # Step 1: Create Gmail account and gather details
        credentials = create_gmail_account(driver)
        credentials_list.append(credentials)

        # Step 2: Save credentials to CSV file
        save_credentials_to_csv(credentials_list)

    except Exception as e:
        print(f"Error encountered: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
