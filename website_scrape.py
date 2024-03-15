"""
    Objective: Scrape books data from http://books.toscrape.com and store it in Database.
    
    Note: first remove the books_data.db file to avoid the data redundancy, then run this program.           
"""
from bs4 import BeautifulSoup
import requests
import sqlite3

# Function to create SQLite database and store books data
def store_users_data(name, price, availability, ratings, image):
    try:
        # database connection
        conn = sqlite3.connect('books_data.db')
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS books
                    (name TEXT, price TEXT, availability TEXT, ratings TEXT, image TEXT)''')

        # Insert data into table
        c.execute('INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?, ?)', (
            name,
            price,
            availability,
            ratings,
            image
        ))
        
    except:
        print('Failed to Store users in database')
    finally:
        # Commit changes and close connection
        conn.commit()
        conn.close()


if __name__ == '__main__':
    # page-1 url
    url = "https://books.toscrape.com/catalogue/page-1.html"

    # fetching data from url and store in database
    while url:
        print("================================================")
        # show the loading status
        print(f"{url.split('/')[-1].rstrip('.html')} data loading...")

        # response of the url
        response = requests.get(url)
        # document converted to Unicode, and HTML entities converted to Unicode characters
        soup = BeautifulSoup(response.text, 'html.parser')

        # Process the current page
        books = soup.findAll('article', class_='product_pod')
        
        # storing the book in databse
        for book in books:
            # book's image url
            image = f"https://books.toscrape.com{book.find('img', class_='thumbnail').attrs['src'].lstrip('..').strip()}"
            # book's rating
            ratings = book.find('p', class_='star-rating')['class'][1].strip()
            # book's title
            title = book.find('h3').find('a').get('title').strip()
            # book's price
            price = book.find(
                'p', class_='price_color').get_text().strip().replace("Â", "")
            # book's availability
            availability = book.find('p', class_='availability').get_text().strip()
            
            # store data in database
            store_users_data(title,price,availability,ratings,image)
            
        # show the loading status   
        print(f"{url.split('/')[-1].rstrip('.html')} data loaded successfully...")
        # Find the element for the next page
        next_page = soup.find('li', class_='next')

        if next_page:
            # Extract the link of the next page
            next_page_link = next_page.find('a').get('href')
            # next page link
            url = f"https://books.toscrape.com/catalogue/{next_page_link}"
            
        
        else:
            url = None  # No more pages

