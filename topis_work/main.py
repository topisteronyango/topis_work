# @author: YOUR AMAZING NAME here
# PLEASE BE CAREFUL ABOUT THE DOCSTRINGS AND COMMENTS. Don't uncomment them so you don't have errors.
# Once you understand the steps and program, you can remove all comments.

# Import required libraries and modules needed for our program
import requests
import bs4
import sys
import time

"""
The get_valid_page() function helps get the valid page number for the webpage we are trying to access 
in case a user input page numbers as an argument.
NOTE: This is not important, you can just focus on the first webpage alone and remove this function

"""


def get_valid_page(n):
    pages = 2
    if n == 0 or n > pages:
        print("Sorry, this web page only have 2 pages. You can only check books on page 1 and 2")
        sys.exit()


page = 1
get_valid_page(page)

# The url variable holds the URL we are trying to access to get data
url = f"https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg={page}"

# This is a fancy way of letting anyone running your program know that the data is coming ...
print("Fetching data from webpage\n")
time.sleep(2)

""" I have wrapped the entire program in a try and exception. This helps us catch any errors in running our program 
   OR In the event of a network problem (e.g. DNS failure, refused connection, etc).
"""
try:

    """
    I am headers because some servers only allow specific user-agent strings.
    The server might specifically block requests, or they might utilize a whitelist, or some other reason.
    Passing header into the .get() will help solve this problem.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                      'Safari/537.36',
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"
    }
    # Use request.get() to get web page url. Make sure your url is https
    response = requests.get(url, headers=headers, params={"wait": 2})

    # Make a soup object from the BeautifulSoup library
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    """
    Book component is where all books information can be found. E.g, name of book, price, etc.
    Use .select() method in beautiful soup to select the HTML tag and class 
    """
    book_component = soup.select(".zg-item-immersion")

    # EDGE CASE
    """
    Due to problems with requesting from URL, beautiful soup might return an empty list object.
    We want to inform the person running our program to know they should try again
    """
    if not len(book_component):
        print("Oops! The webpage has refused to serve the data. Please can you run the program again")

    # Make an empty list to add all the popular books we have selected from webpage using BeautifulSoup
    popular_books = []
    # loop through my book component
    for book in book_component:
        # if the book is a 5 star rated, get the book. Note: this is my logic for getting the popular books.
        # Be free to explore your own logic if you disagree with this
        if "a-star-5" in str(book):
            for book_names in book.select(".p13n-sc-truncate"):
                popular_books.append(book_names.getText().strip())

    """
    Now that we have all the popular books on that webpage, let's get their prices.
    """
    # Make an empty list to hold the values / prices we get
    popular_books_prices = []
    for book in book_component:
        # We want to make sure we are looking through the book component and getting the prices of popular books
        if "a-star-5" in str(book):
            for prices in book.find(name="span", class_="p13n-sc-price"):
                popular_books_prices.append(float(prices.replace("$", "")))

    """
    Now that we have the prices, we want to sort the prices and get the top 10 prices
    """
    # make an empty lst to hold the sorted prices we get
    sorted_top_ten_prices = []
    # Now loop through the initial prices list and get the top 10
    for price in popular_books_prices:
        sorted_top_ten_prices.append(price)
    # The steps below helps get the top 10 prices of books from lowest to highest
    # Note: if you have a max_range, do change the value of max_range. E.g, if you want to get top 20, max_range = 20
    max_range = 10
    sorted_top_ten_prices.sort()
    sorted_top_ten_prices = sorted_top_ten_prices[-max_range:]

    """
    Now that we have the top 10 prices(most expensive books). We want to get the names of these books from the webpage
    """
    # Make an empty list to hold the value
    ten_most_expensive = []
    """
    Note: Unsorted here is not that important, you can forget about it and just return the ten_most_expensive
    Unsorted prices list holds the top 10 prices with sorting. We are doing this so we can compare it with what 
    ten_most_expensive returns and make a dictionary that holds books and their prices
    """
    unsorted_prices = []
    # Loop through the book component
    for book in book_component:
        # if we find a 5 star book
        if "a-star-5" in str(book):
            # loop through the sorted top ten price list as well
            for val in sorted_top_ten_prices:
                # if the val from the price list is in the string book component
                if f"${val}" in str(book):
                    # append all the books in the ten most expensive books list
                    ten_most_expensive.append((book.find(name="div", class_="p13n-sc-truncate").text.strip()))
                    """
                    Again this part below is not important, you can decide to just return the books as they are instead 
                    of putting them in a list of dictionary like I did below
                    """
                    for prices in book.find(name="span", class_="p13n-sc-price"):
                        unsorted_prices.append(prices)

    # USING dictionary Comprehension
    """
    I have used a dictionary comprehension syntax to save the names of books and their prices in a final result variable 
    that returns our top 10 most expensive popular books with the most reviews as a list of dictionary
    """
    final_result = [{ten_most_expensive[i]: unsorted_prices[i] for i in range(len(ten_most_expensive))}]

    # This is what we are returning as final result
    print(final_result)

except requests.exceptions.RequestException as e:
    print("Something went wrong. Please check the URL\n", e)

# ------------------------------- END OF PROGRAM ----------------------------------------
