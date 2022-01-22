"""
GoodReads Cover Images
- Script to fetch book covers from GoodReads, after importing .csv
- Based on AmunRa1322's script https://github.com/AmunRa1322/Notion-Scripts
"""
import sys
from notion_client import Client
from bs4 import BeautifulSoup
from urllib.request import urlopen
from utils import get_all_in_collection, get_property_value

"""
Access Settings
"""
# TODO:
# Create an Integration Token here:
# https://www.notion.so/my-integrations
# And invite the Integration app to the collection you want it to access
client = Client(auth=">>ADD SECRET HERE<<")
# TODO:
# Find the database id by viewing the collection in your browser, and copying it from the URL:
# https://www.notion.so/my_workspace/COPY_THIS_DATABASE_ID?v=another_string
database_id = ">>ADD DATABASE ID HERE<<"

"""
Cover fetch options
"""
goodreads_url = "https://www.goodreads.com/book/show/"


book_table = []
all_results = get_all_in_collection(client, database_id)

for result in all_results:
    properties = result['properties']
    if "Book Id" in properties:
        book_id = get_property_value(properties["Book Id"])
        if book_id:
            title = get_property_value(properties["Title"])
            case = { 'id': result['id'], 'Book_Id': book_id, 'Image': result["cover"],
                    'title': title }
            book_table.append(case)

if len(book_table) == 0:
    print('No items with property "Book Id" found. Did you import a csv from GoodReads?')
    sys.exit(0)

print('Splitting the data into chunks of 10 elements...\n')

def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]

book_table = list(split(book_table, 10))

print(str(len(book_table)) + ' chunks created.')

for idy, valA in enumerate(book_table):
    print('----')
    print('chunk ' + str(idy) + ' in progress')
    for idx, val in enumerate(valA):
        if not val['Image']:
            url = goodreads_url + str(val['Book_Id'])
            try:
                url_open = urlopen(url)
                soup = BeautifulSoup(url_open, 'html.parser')
                tag = soup.find("img", {"id": "coverImage"})
                img = tag['src']
                print(f'Updating image for: {val["title"]}')
                client.pages.update(
                    **{
                        "page_id": val['id'],
                        "cover": {
                            'type': 'external',
                            'external': {
                                'url': tag['src']
                            }
                        }
                    }
                )
            except:
                print(f'Image update failed for: {val["title"]}')
        else:
            print(str(idx + 1) + f' / 10 - Skipping "{val["title"]}", already has a cover image')
    print('chunk ' + str(idy) + ' finished')
