"""
De-Duplicate
- Find duplicates based on set properties, and merge chosen properties
"""
from notion_client import Client
from datetime import datetime
import sys
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
De-Dupe Options
"""
properties_to_match_on = ['Title', 'Author']
case_sensitive = False
prefer_oldest = True
date_property = 'created_time'  # other option: 'last_edited_time'
merge_cover = True
properties_to_merge = ['Rec', 'Status', 'Book Id', 'Year', 'Date Added', 'Publisher', 'Link']
max_number_to_merge = 1000

print('Getting data from Notion...')
all_results = get_all_in_collection(client, database_id)
item_table = []


"""
Returns item_a with missing properties from item_b
- Also updates local properties
"""
def merge_update_item(item_a, item_b):
    update_dict = { 'properties': {} }
    submit_update = False
    for property in properties_to_merge:
        prop_a_val = get_property_value(item_a['properties'][property])
        prop_b_val = get_property_value(item_b['properties'][property])
        # print('Comparing:', prop_a_val, prop_b_val)
        if prop_b_val and not prop_a_val:
            update_dict['properties'][property] = item_b['properties'][property]
            submit_update = True
    if merge_cover:
        prop_a_cover = item_a['cover']
        prop_b_cover = item_b['cover']
        if prop_b_cover and not prop_a_cover:
            if prop_b_cover['type'] == 'external':
                update_dict['cover'] = prop_b_cover
                submit_update = True
            else:
                # API only supports updating 'external'
                print('Warning: Uploaded cover image can not be handled')
    update_dict['page_id'] = item_a['id']
    if submit_update:
        # Update the page item!
        updated_page = client.pages.update(
            **update_dict
        )
        # Update local values, in case there are more copies
        for idx, item in enumerate(item_table):
            if item['id'] == updated_page['id']:
                item_table[idx] = updated_page
                break
    else:
        print('No properties to update.')


"""
Archives page with given id
- Also updates local properties
"""
def delete_item(id: str):
    print("Archiving duplicate...")
    # Delete AKA Archive, since Notion doesn't have a delete endpoint
    client.pages.update(
        **{
            "page_id": id,
            "archived": True
        }
    )
    # Remove local values
    for idx, item in enumerate(item_table):
        if item['id'] == id:
            item_table.pop(idx)
            break

# Useful for determining key values for properties in a Collection
# print('\nAvailable properties in Collection:\n')
# for key in all_results[0]['properties'].keys():
#     print(key)

merge_count = 0

for result in all_results:
    properties = result['properties']
    match_str = ''
    simple_dict = {}

    # Dates are top level Notion metadata
    date_value = result[date_property][0:18]
    simple_dict['COMPARE_DATE'] = datetime.strptime(date_value, '%Y-%m-%dT%H:%M:%S')
    simple_dict['id'] = result['id']

    for property in properties_to_match_on:
        if property in properties:
            value = get_property_value(properties[property])
            if value:
                if case_sensitive:
                    match_str += value
                else:
                    match_str += value.lower()
            else:
                match_str += '##EMPTY##VALUE##'
    simple_dict['MATCH_ON'] = match_str
    simple_dict['RESULT'] = result
    already_deleted = False
    # Check for duplicates so far
    for other in item_table:
        if simple_dict['MATCH_ON'] == other['MATCH_ON']:
            print('\nFound duplicate!')
            print(simple_dict['MATCH_ON'])
            a = simple_dict['RESULT']
            b = other['RESULT']
            if (simple_dict['COMPARE_DATE'] > other['COMPARE_DATE']) == prefer_oldest:
                a, b = b, a
                already_deleted = True
            # Make update request (also updates local values)
            merge_update_item(result, other['RESULT'])
            # Make archive request (also updates local values)
            delete_item(b['id'])
            merge_count += 1
            if merge_count >= max_number_to_merge:
                sys.exit(0)
    # Build table
    if not already_deleted:
        item_table.append(simple_dict)

print(f'\nDe-dupe complete, {merge_count} merged')
