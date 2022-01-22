## Python Notion Scripts

Handy scripts to automate or integrate with Notion

## goodreads.py

Add book covers from GoodReads to Notion.

### 1. First, import your GoodReads shelves into Notion

After exporting your My Books from [GoodReads](https://www.goodreads.com/) (in the lefthand sidebar), upload the .csv file to a collection in Notion using the "Merge with CSV" option. Make sure after importing that books have a "Book ID" value, if they don't you may need to add a "Book ID" property to the collection before merging/importing.

### 2. Create a Notion integration

* You will need an Integration Secret from Notion to use their API, [create one here](https://www.notion.so/my-integrations).
* Then add/share the Collection you are using for your books with the integration you created.
* Add the Integration Secret to the script.

### 3. Find your Database ID

Find the database ID by viewing the Notion collection in your browser, and copying it from the URL:
`https://www.notion.so/my_workspace/COPY_THIS_DATABASE_ID?v=another_string`

Then add the database id to the script.

### 4. Run the script!

Make sure you have the dependencies installed:
`pip install notion_client bs4`

Then run using:
`python ./goodreads.py`

To begin scraping cover image URLs from GoodReads.


## de-dupe.py

### 1. Add Notion integration secret and Database ID

See `goodreads.py` steps for details.

### 2. Choose settings

Various variables are available to configure the de-dupe/merge process, such as `properties_to_match_on` and `prefer_oldest` - read through them carefully before beginning the script. Consider setting `max_number_to_merge` to handle one or two at a time and check the results first.

### 3. Install dependencies, and run script!

Make sure you have the dependencies installed:
`pip install notion_client`

Then run using:
`python ./de-dupe.py`
