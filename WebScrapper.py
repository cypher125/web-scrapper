import requests
from bs4 import BeautifulSoup


class ProductScraper:
    def __init__(self, url):
        self.url = url

    def save_html_page(self, filename):
        # Send an HTTP GET request to the URL
        response = requests.get(self.url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Get the HTML content from the response
            html_content = response.text
            
            # Save the HTML content to a file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(html_content)
                print("HTML page saved as page.html.")
        else:
            print("ERROR: Failed to save the HTML content.")

    def scrape_products(self, filename):
        # Read the HTML content from the file
        with open(filename, "r", encoding="utf-8") as file:
            html_content = file.read()
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Find all product divs
            products = soup.find_all("div", class_="product")
            
            # Open a file to save the scraped data
            with open('all_products.txt', 'a', encoding='utf-8') as txt_file:
                for product in products:
                    # Extract product details
                    product_name = product.find("h5").text.strip()
                    original_price = product.find("p", class_="offer-price").text.strip()
                    second_price_index = original_price.find('₦', 1)
                    product_price = original_price[:second_price_index].strip()
                    discount_price = original_price[second_price_index:].strip()
                    product_size = product.find("span").text.strip()
                    
                    # If product size is empty, set it to "No size"
                    if product_size == "":
                        product_size = "No size"
                    
                    # Prepare the table data
                    table_data = f"Product Name: {product_name}\nProduct Price: {product_price}   Discount Price: {discount_price}\nProduct Size: {product_size}\n"
                    
                    # Write the table data to the file
                    txt_file.write(table_data + "\n")

                    print(f"Data for {product_name} appended to all_products.txt")


if __name__ == "__main__":
    # Define the URL and HTML filename
    url = "http://www.asadefud.com"
    html_filename = "page.html"

    # Create an instance of the ProductScraper class
    scraper = ProductScraper(url)
    
    # Save the HTML page
    scraper.save_html_page(html_filename)
    
    # Scrape product details from the HTML file
    scraper.scrape_products(html_filename)
