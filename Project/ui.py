import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
import webbrowser

def search_compareraja(product_name):
    search_query = product_name.replace(' ', '-')
    url = f"https://www.compareraja.in/search?c=all&q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')


    if soup:
        product_name_element = soup.find("a", class_="link")
        product_price_element = soup.find("b")

        if product_name_element and product_price_element:
            product_name = product_name_element.text.strip()
            product_price = product_price_element.text.strip()
            numeric_price = extract_numeric_price(product_price)
            if numeric_price:
                compareraja_result['text'] = f"Product Name: {product_name}\nProduct Price: {numeric_price}"
                return numeric_price
            else:
                compareraja_result['text'] = "Product not found."
        else:
            compareraja_result['text'] = "Product not found."
    else:
        compareraja_result['text'] = "Product not found."
    return None


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
            flipkart_result['text'] = f"Product Name: {product_name}\nProduct Price: {numeric_price}"
            return numeric_price
        else:
            flipkart_result['text'] = "Product not found."
    else:
        flipkart_result['text'] = "Product not found."
    return None


def search_gadgetsnow(product_name):
    search_query = product_name.replace(' ', '+')
    url = f"https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={search_query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    if soup:
        product_name_element = soup.find("span", class_="product-name")
        product_price_element = soup.find("span", class_="offerprice")

        if product_name_element and product_price_element:
            product_name = product_name_element.text.strip()
            product_price = product_price_element.text.strip()
            numeric_price = extract_numeric_price(product_price)
            if numeric_price:
                gadgetsnow_result['text'] = f"Product Name: {product_name}\nProduct Price: {numeric_price}"
                return numeric_price
            else:
                gadgetsnow_result['text'] = "Product not found."
        else:
            gadgetsnow_result['text'] = "Product not found."
    else:
        gadgetsnow_result['text'] = "Product not found."
    return None


def extract_numeric_price(price):
    # Convert price data to numerical format
    if price:
        numeric_price = re.sub(r"[^\d]", "", price)
        try:
            numeric_price = int(numeric_price)
            return numeric_price
        except ValueError:
            return None
    return None



#data analysis part
def compare_prices():
    product_name = search_entry.get()
    flipkart_price = search_flipkart(product_name)
    gadgetsnow_price = search_gadgetsnow(product_name)
    compareraja_price = search_compareraja(product_name)

    if flipkart_price and gadgetsnow_price and compareraja_price:
        min_price = min(flipkart_price, gadgetsnow_price, compareraja_price)
        if min_price == flipkart_price:
            cheapest_price['text'] = "Flipkart"
        elif min_price == gadgetsnow_price:
            cheapest_price['text'] = "GadgetsNow"
        else:
            cheapest_price['text'] = "compareRaja"
    else:
        cheapest_price['text'] = "Product not found."



def open_product_link():
    product_name = search_entry.get()
    flipkart_price = search_flipkart(product_name)
    gadgetsnow_price = search_gadgetsnow(product_name)
    compareraja_price = search_compareraja(product_name)

    if flipkart_price and gadgetsnow_price and compareraja_price:
        if flipkart_price < gadgetsnow_price and flipkart_price < compareraja_price:
            product_link = get_flipkart_product_link(product_name)
        elif gadgetsnow_price < flipkart_price and gadgetsnow_price < compareraja_price:
            product_link = get_gadgetsnow_product_link(product_name)
        else:
            product_link = get_compareraja_product_link(product_name)

        if product_link:
            webbrowser.open(product_link)
    else:
        cheapest_price['text'] = "Product not found."



def get_flipkart_product_link(product_name):
    search_query = product_name.replace(' ', '%20')
    url = f"https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    return url


def get_gadgetsnow_product_link(product_name):
    search_query = product_name.replace(' ', '+')
    url = f"https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={search_query}"
    return url


def get_compareraja_product_link(product_name):
    search_query = product_name.replace(' ', '-')
    url = f"https://www.compareraja.in/search?c=all&q={search_query}"
    return url


# Create Tkinter window
window = tk.Tk()
window.title("Price Comparison")
window.geometry("800x600")

# Create search section
search_frame = tk.Frame(window)
search_frame.pack(pady=20)

search_label = tk.Label(search_frame, text="Enter Product Name:")
search_label.grid(row=0, column=0)

search_entry = tk.Entry(search_frame, width=40)
search_entry.grid(row=0, column=1)

search_button = tk.Button(search_frame, text="Search", command=compare_prices)
search_button.grid(row=0, column=2)

# Create Flipkart section
flipkart_frame = tk.Frame(window)
flipkart_frame.pack(pady=20)

flipkart_label = tk.Label(flipkart_frame, text="Flipkart", font=("Helvetica", 16, "bold"))
flipkart_label.pack()

flipkart_result = tk.Label(flipkart_frame, text="", font=("Helvetica", 12))
flipkart_result.pack()

# Create GadgetsNow section
gadgetsnow_frame = tk.Frame(window)
gadgetsnow_frame.pack(pady=20)

gadgetsnow_label = tk.Label(gadgetsnow_frame, text="GadgetsNow", font=("Helvetica", 16, "bold"))
gadgetsnow_label.pack()

gadgetsnow_result = tk.Label(gadgetsnow_frame, text="", font=("Helvetica", 12))
gadgetsnow_result.pack()

# Create compareraja section
compareraja_frame = tk.Frame(window)
compareraja_frame.pack(pady=20)

compareraja_label = tk.Label(compareraja_frame, text="compareRaja", font=("Helvetica", 16, "bold"))
compareraja_label.pack()

compareraja_result = tk.Label(compareraja_frame, text="", font=("Helvetica", 12))
compareraja_result.pack()

# Create cheapest price section
cheapest_frame = tk.Frame(window)
cheapest_frame.pack(pady=20)

cheapest_label = tk.Label(cheapest_frame, text="Cheapest Price", font=("Helvetica", 16, "bold"))
cheapest_label.pack()

cheapest_price = tk.Label(cheapest_frame, text="", font=("Helvetica", 12))
cheapest_price.pack()

# Create Get Product section
get_product_frame = tk.Frame(window)
get_product_frame.pack(pady=20)

get_product_button = tk.Button(get_product_frame, text="Get Product", command=open_product_link)
get_product_button.pack()

# Start the Tkinter event loop
window.mainloop()
