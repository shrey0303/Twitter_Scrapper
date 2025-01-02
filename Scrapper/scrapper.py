from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pymongo
import uuid
import requests
from flask import Flask, jsonify, render_template_string
import json
from selenium.webdriver.chrome.options import Options
import time

<<<<<<< HEAD
# Initialize Flask app
=======
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

    twitter_username = process.env.username
    twitter_password = process.env.password

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

>>>>>>> origin/master
app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_trends"]
collection = db["trending_topics"]

# ProxyMesh configuration
PROXYMESH_USERNAME = "jonty_007"
PROXYMESH_PASSWORD = "X.85PzyETBtiTf%40"
PROXYMESH_ENDPOINTS = [
    "us-wa.proxymesh.com:31280",
    "us-ny.proxymesh.com:31280",
    "us-fl.proxymesh.com:31280"
]

def get_proxy():
    """Get a random proxy from ProxyMesh"""
    proxy = PROXYMESH_ENDPOINTS[int(time.time()) % len(PROXYMESH_ENDPOINTS)]
    return {
        'http': f'http://{PROXYMESH_USERNAME}:{PROXYMESH_PASSWORD}@{proxy}',
        'https': f'http://{PROXYMESH_USERNAME}:{PROXYMESH_PASSWORD}@{proxy}'
    }

def scrape_twitter_trends():
    """Scrape trending topics from Twitter"""
    # Set up Chrome options
    chrome_options = Options()
    proxy = get_proxy()
    chrome_options.add_argument(f'--proxy-server={proxy["http"]}')
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Login to Twitter
        driver.get("https://x.com/i/flow/login")
        
        # Wait for email input and enter credentials
        email_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email_input.send_keys("jontyjim07@gmail.com")
        
        # Click Next
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
        
        # Wait for password input and enter password
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys("#Bond007")
        
        # Click Login
        login_button = driver.find_element(By.XPATH, "//span[text()='Log in']")
        login_button.click()
        
        # Wait for trending section to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='What's happening']"))
        )
        
        # Get trending topics
        trending_topics = driver.find_elements(By.XPATH, "//div[@data-testid='trend']")[:5]
        trends = [topic.text.split('\n')[0] for topic in trending_topics]
        
        # Create document for MongoDB
        document = {
            "_id": str(uuid.uuid4()),
            "nameoftrend1": trends[0],
            "nameoftrend2": trends[1],
            "nameoftrend3": trends[2],
            "nameoftrend4": trends[3],
            "nameoftrend5": trends[4],
            "timestamp": datetime.now(),
            "ip_address": requests.get('https://api.ipify.org').text
        }
        
        # Insert into MongoDB
        collection.insert_one(document)
        return document
        
    finally:
        driver.quit()

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Trends Scraper</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .button { 
            padding: 10px 20px;
            background-color: #1DA1F2;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .results {
            margin-top: 20px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    {% if not results %}
    <a href="/scrape" class="button">Click here to run the script</a>
    {% else %}
    <div class="results">
        <h3>These are the most happening topics as on {{ results.timestamp }}:</h3>
        <p>Name of trend1 - {{ results.nameoftrend1 }}</p>
        <p>Name of trend2 - {{ results.nameoftrend2 }}</p>
        <p>Name of trend3 - {{ results.nameoftrend3 }}</p>
        <p>Name of trend4 - {{ results.nameoftrend4 }}</p>
        <p>Name of trend5 - {{ results.nameoftrend5 }}</p>
        <p>The IP address used for this query was {{ results.ip_address }}</p>
        <h4>Here's a JSON extract of this record from MongoDB:</h4>
        <pre>{{ results_json }}</pre>
        <br>
        <a href="/" class="button">Click here to run the query again</a>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scrape')
def scrape():
    results = scrape_twitter_trends()
    results_json = json.dumps(results, default=str, indent=2)
    return render_template_string(HTML_TEMPLATE, results=results, results_json=results_json)

if __name__ == '__main__':
    app.run(debug=True)