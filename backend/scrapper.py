import time
import random
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import requests

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trends']

def get_proxy():
    # Replace 'USERNAME' and 'PASSWORD' with your actual ProxyMesh account credentials.
    proxy_url = "https://jonty_007:X.85PzyETBtiTf%40@proxy.proxymesh.com:31280"
    
    try:
        response = requests.get(proxy_url)
        response.raise_for_status()  # Raises an error for unsuccessful status codes
        print(f"Proxy fetched successfully: {response.text.strip()}")  # Debugging line
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching proxy: {e}")
        return None  # Return None if there's an error
    
def init_driver(proxy):
    if proxy:
        print(f"Using proxy: {proxy}")  # Debugging line
    else:
        print("No proxy provided")  # Debugging line
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument("--no-proxy-server")
    
    service = Service("C:/Users/SHREY/chromedriver-win64/chromedriver.exe")  # Path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Scrape Twitter home page for trending topics
def scrape_trending():
    proxy = get_proxy()  # Fetch new proxy IP
   
    driver = init_driver(proxy)

    twitter_username = "parker_jon43869"
    twitter_password = "#Bond007"

    driver.get("https://x.com/i/flow/login")

    # Wait for the "text" field to appear
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_field.send_keys(twitter_username)
        username_field.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error locating the username field: {e}")
        driver.quit()
        return None

    time.sleep(2)
    
    try:
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(twitter_password)
        password_field.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error locating the password field: {e}")
        driver.quit()
        return None

    # Wait until the trending page is loaded
    time.sleep(5)
    driver.get("https://x.com/explore/tabs/trending")
    time.sleep(3)

    # Get the names of the top 5 trending topics
    trends = []
    trend_elements = driver.find_elements(By.XPATH, '//div[@data-testid="trend"]//span')
    
    if trend_elements:
        for trend in trend_elements[:5]:
            trends.append(trend.text)
    else:
        print("No trends found.")
    
    if len(trends) < 5:
        print("Warning: Less than 5 trends found.")
        trends += ["No trend"] * (5 - len(trends))

    # Generate a unique ID and store data in MongoDB
    unique_id = str(uuid.uuid4())
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    data = {
        "_id": unique_id,
        "trend1": trends[0],
        "trend2": trends[1],
        "trend3": trends[2],
        "trend4": trends[3],
        "trend5": trends[4],
        "timestamp": timestamp,
        "ip": proxy if proxy else "No proxy"
    }

    # Save the record to MongoDB
    collection.insert_one(data)

    driver.quit()

    return data
# Flask API to trigger the scraper and fetch the results
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/run-scraper', methods=['GET'])
def run_scraper():
    result = scrape_trending()
    return jsonify({
        'trends': [result['trend1'], result['trend2'], result['trend3'], result['trend4'], result['trend5']],
        'ip': result['ip'],
        'timestamp': result['timestamp'],
        'data': result,
        'message': 'Scraper run successfully!'
    })

if __name__ == "__main__":
    app.run(debug=True)
