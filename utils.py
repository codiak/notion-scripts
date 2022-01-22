"""
Shared code between scripts
"""

def get_all_in_collection(client, database_id: str):
    all_results = []
    def query_database(all_results, cursor: str = None):
        args = {
            "database_id": database_id,
            "page_size": 100,  # API maximum is 100
        }
        if cursor:
            args['start_cursor'] = cursor
        page = client.databases.query(
            **args
        )
        if page['results']:
            all_results = all_results + page['results']
        else:
            Exception('No results returned!')
        return page
    # Initiate query
    page = query_database(all_results)
    all_results = page['results']

    # Iterate over pages and collect all results
    while page['has_more']:
        page = query_database(all_results, page['next_cursor'])
        all_results = all_results + page['results']

    print(f'\nCollection contains {len(all_results)} items')
    return all_results


'''
Fetches a simple value for a given property, designed for comparison

Example property format:
'Publisher': {'id': 'BW%7C%3D',
                'type': 'rich_text',
                 'rich_text': [{'type': 'text',
                              'text': {'content': 'Self-Realization Fellowship Publishers', 'link': None}
'''
def get_property_value(property):
    try:
        prop_type = property["type"]
        value = property[prop_type]
        # Handle nested values, such as rich_text fields
        if type(value) is list:
            first = value[0]  # it's not clear why these values are arrays
            if first and "type" in first:
                sub_type = value[0]["type"]
                sub_value = value[0][sub_type]
                if type(sub_value) is dict:
                    if "content" in sub_value:
                        return sub_value["content"]
                    elif "name" in sub_value:
                        return sub_value["name"]
                    else:
                        # TODO: May need to handle other property types
                        return sub_value
        else:
            # Handle simple types, such as number
            return value
    except:
        return None
