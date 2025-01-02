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

# Initialize Flask app
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