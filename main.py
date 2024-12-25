from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from flask import Flask, render_template_string, redirect, url_for
from webdriver_manager.chrome import ChromeDriverManager
import os

# Load environment variables
load_dotenv()

# MongoDB Atlas Setup
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["myntra_scraping"]
collection = db["tshirts"]

# Selenium Driver Setup
def init_driver():
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())  # Dynamically install ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    return driver

driver = init_driver()

# Flask App Setup
app = Flask(__name__)

# URL to scrape
MYNTRA_URL = "https://www.myntra.com/tshirts?rawQuery=tshirts"

# Scraping Function
def scrape_myntra():
    """Scraping product's data from Myntra and storing it in MongoDB."""
    try:
        print("Loading page...")
        driver.get(MYNTRA_URL)
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-base"))
        )
        print("Page loaded successfully!")

        elements = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
        scraped_data = []

        for index, element in enumerate(elements):
            try:
                title = element.find_element(By.CSS_SELECTOR, "a div.product-productMetaInfo h3").text
                description = element.find_element(By.CSS_SELECTOR, "h4.product-product").text
                link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                if title and link:
                    scraped_data.append({"title": title, "description": description, "link": link})
            except Exception as e:
                print(f"Error scraping element {index}: {e}")

        if scraped_data:
            try:
                collection.delete_many({})
                collection.insert_many(scraped_data)
                print("Data stored in MongoDB successfully!")
            except Exception as e:
                print(f"Error storing data in MongoDB: {e}")
        else:
            print("No data found to store.")
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

# Flask Routes
@app.route("/scrape")
def scrape():
    """Triggers the scraping process"""
    try:
        scrape_myntra()
    except Exception as e:
        print(f"Scraping failed: {e}")
    return redirect(url_for("display_data"))

@app.route("/scraped-data")
def display_data():
    """Displays scraped data in a web page"""
    data = collection.find()
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scraped Items</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; font-family: Arial, sans-serif; }
            .container { margin-top: 30px; }
            .card { margin-bottom: 20px; border: 1px solid #dee2e6; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            .card h5 { color: #495057; font-size: 18px; font-weight: bold; }
            .card p { font-size: 14px; color: #6c757d; margin: 5px 0 10px; }
            .card a { text-decoration: none; color: #007bff; }
            .card a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center mb-4">Scraped Items</h1>
            <div class="row">
                {% for item in data %}
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ item.title }}</h5>
                                <p class="card-text">{{ item.description }}</p>
                                <a href="{{ item.link }}" target="_blank" class="card-link">View Product</a>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return render_template_string(html_template, data=data)

@app.route("/")
def home():
    """Home page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scraper App</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container text-center mt-5">
            <h1>Welcome to ScraperApp</h1>
            <p>Your one-stop solution to scrape and organize product information.</p>
            <a href="/scrape" class="btn btn-primary">Start Scraping</a>
            <a href="/scraped-data" class="btn btn-secondary">View Scraped Data</a>
        </div>
    </body>
    </html>
    """

# Entry Point
if __name__ == "__main__":
    app.run(debug=True)