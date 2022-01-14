
from notion_client import Client
from bs4 import BeautifulSoup
from urllib.request import urlopen

book_table = []
goodreads_url = "https://www.goodreads.com/book/show/"
# TODO:
# Create an Integration Token here:
# https://www.notion.so/my-integrations
# And invite the Integration app to the collection you want it to access
client = Client(auth="ADD_INTEGRATION_SECRET")
print('Getting data from Notion...')
list_users_response = client.users.list()
print("Accessing user: " + list_users_response["results"][0]["name"])

page = client.databases.query(
    **{
        # TODO:
        # Find the database id by viewing the collection in your browser, and copying it from the URL:
        # https://www.notion.so/my_workspace/COPY_THIS_DATABASE_ID?v=another_string
        "database_id": "ADD_DATABASE_ID",
    }
)

'''
Example property format:
'Publisher': {'id': 'BW%7C%3D',
                'type': 'rich_text',
                 'rich_text': [{'type': 'text',
                              'text': {'content': 'Self-Realization Fellowship Publishers', 'link': None}
'''
def get_property_value(property):
    if property:
        type = property["type"]
        sub_type = property[type][0]["type"]
        return property[type][0][sub_type]["content"]
    else:
        return None

for result in page['results']:
    properties = result['properties']
    if "Book Id" in properties:
        book_id = get_property_value(properties["Book Id"])
        title = get_property_value(properties["Title"])
        # cover = get_property_value(properties["Cover"])
        print(f'Found book {book_id}')
        case = { 'id': result['id'], 'Book_Id': book_id, 'Image': result["cover"],
                 'title': title }
        book_table.append(case)

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
            url_open = urlopen(url)
            soup = BeautifulSoup(url_open, 'html.parser')
            tag = soup.find("img", {"id": "coverImage"})
            try:
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
