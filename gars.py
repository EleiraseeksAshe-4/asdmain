import json


def fetch_gars_data(context):
    active_path = context['active_path']
    gars_json_path = f"{active_path}/word/gars3.json"
    with open(gars_json_path, 'r') as file:
        gars = json.load(file)

    ratingscales = context['rs']
    ratingscales['gars'] = gars

    return gars
