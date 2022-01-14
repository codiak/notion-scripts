## Python Notion Scripts

Handy scripts to automate or integrate with Notion

## goodreads.py

Add book covers from GoodReads to Notion.

### 1. First, get your books in Notion

After exporting your My Books from [GoodReads](https://www.goodreads.com/) (in the lefthand sidebar), upload the .csv file to a collection in Notion using the "Merge with CSV" option. Make sure after importing that books have a "Book ID" value, if they don't you may need to add a "Book ID" property to the collection before merging/imoprting.

### 2. Create a Notion integration*

* You will need an Integration Secret from Notion to use their API, [create one here](https://www.notion.so/my-integrations).
* Then add/share the Collection you are using for your books with the integration you created.
* Add the Integration Secret to the script.

### 3. Find your Database ID

Find the database id by viewing the Notion collection in your browser, and copying it from the URL:
`https://www.notion.so/my_workspace/COPY_THIS_DATABASE_ID?v=another_string`

Then add the database id to the script.

### 4. Run the script!

Make sure you have the dependencies installed:
`pip install notion_client bs4`

Then run using:
`python ./goodreads.py`

To begin the scraping image URLs from GoodReads.
