# Flipkart Review Scraper

## Description

Flipkart Review Scraper is a Python-based web scraper designed to extract product reviews from Flipkart's website. The scraper allows users to specify the product they are interested in, after which it automatically retrieves reviews for each product displayed on the front page. The scraped data includes the product name, reviewer's name, a short review excerpt, and the main review text. The extracted data is then stored in MongoDB.

## How it Works

1. Enter the name of the product you want to fetch reviews for.
2. The scraper will visit the Flipkart website and collect all products displayed on the front page.
3. Reviews for each product will be scraped, including the product name, reviewer's name, short review excerpt, and main review text.
4. The scraped data is then stored in a MongoDB database.

## How to Setup

Follow these steps to set up the Flipkart Review Scraper:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create an account on the MongoDB website (if you haven't already).
4. Obtain the connection link for your MongoDB instance and replace it in the script.
5. Uncomment the for loop (`for i in range(1, max_pages + 1):`) in the code if you want to fetch reviews from multiple pages (note: this may increase processing time).
6. Run the script, and you're done!

## Limitations

1. The scraper currently fetches products only from the first page of search results (typically 10 products).
2. If you choose to fetch reviews from all pages, the front end may not function properly until the scraping process is complete. However, the data will still be stored in MongoDB.

## Deployment

The project is ready to be deployed on the cloud. It has already been deployed on AWS.

Feel free to contribute to the project and improve its functionality!

