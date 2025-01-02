# Twitter Scraper

A Python Flask application to scrape the trending topics on Twitter using Selenium and store the results in MongoDB.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.10](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/try/download/community)
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) (ensure it matches your installed Chrome version)

## Setup Instructions

### 1. Create and Activate Virtual Environment

You can create a virtual environment to isolate project dependencies.

```bash
# Create virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```
2. Install Dependencies
Once the virtual environment is active, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

3. Set Up MongoDB
Make sure you have MongoDB running locally. You can start it by running:

```bash
# For Windows
mongod

# For macOS/Linux (if MongoDB is installed via Homebrew)
brew services start mongodb-community@5.0
```

4. Running the Application
Once everything is set up, you can run the Flask application:

```bash

# Run the Flask app
python scrapper.py
```
Visit ```http://localhost:5000``` in your browser to start the scraper.

5. Using the Application
```
Visit / and click the "Run Script" button to scrape the latest Twitter trends.
The results will be displayed, and the data will be saved to your MongoDB database.
```
## Authors

- [@Shrey](https://www.github.com/shrey0303)

