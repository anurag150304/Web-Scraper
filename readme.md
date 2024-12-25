# Web Scraping App

This is a web scraping application built with Python, Flask, Selenium, and MongoDB. The app scrapes product data from Myntra and stores it in a MongoDB database. The scraped data can be viewed through a web interface.

## Features

- Scrapes product data from Myntra
- Stores scraped data in MongoDB
- Displays scraped data in a web interface
- Uses Flask for the web server
- Uses Selenium for web scraping

## Requirements

- Python 3.x
- MongoDB
- Google Chrome
- ChromeDriver

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/web-scraping-app.git
    cd web-scraping-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add your MongoDB URI:
    ```env
    MONGO_URI=your_mongodb_uri
    ```

## Usage

1. Run the Flask app:
    ```sh
    python main.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Use the web interface to start scraping and view the scraped data.

## Routes

- `/` - Home page
- `/scrape` - Triggers the scraping process
- `/scraped-data` - Displays the scraped data

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Selenium](https://www.selenium.dev/)
- [MongoDB](https://www.mongodb.com/)
- [Bootstrap](https://getbootstrap.com/)