import requests
from bs4 import BeautifulSoup
import re

def search_flipkart(product_name):
    search_query = product_name.replace(' ', '%20')
    url = f"https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_name_element = soup.find("div", class_="_4rR01T")
    product_price_element = soup.find("div", class_="_30jeq3 _1_WHN1")

    if product_name_element and product_price_element:
        product_name = product_name_element.text.strip()
        product_price = product_price_element.text.strip()
        numeric_price = extract_numeric_price(product_price)
        if numeric_price:
            result = f"Product Name: {product_name}\nProduct Price: {numeric_price}"
        else:
            result = "Product not found."
    else:
        result = "Product not found."

    return result

def extract_numeric_price(price):
    # Convert price data to numerical format
    if price:
        numeric_price = re.sub(r"[^\d.]", "", price)
        try:
            numeric_price = float(numeric_price)
            return numeric_price
        except ValueError:
            return None
    return None
