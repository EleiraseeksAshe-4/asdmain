import pandas as pd
import json

# Load the Excel file
file_path = "/Users/johnbridges/Dropbox/NewHope Psychology/JoyConsulting/GateInc/ExpertReports/templates/carseval_data.xlsx"
xls = pd.ExcelFile(file_path)

# Initialize the main structure
data_structure = {
    "parent": {},
    "contributing_items": [],
    "weights_section": [],
    "evaluation_map": {},
    "parent_value_map": {},
    "severity_ranges": [],
    "age_group_lookups": {}
}

# Process each sheet in the Excel file
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)

    if sheet_name.lower() == "parent":
        data_structure["parent"] = {
            "section": {
                "name": "Parent Section",
                "detail": "Details about parent section",
                "questions": [
                    {"number": int(row['number']), "question": row['question']}
                    for _, row in df.iterrows()
                ]
            }
        }
    elif sheet_name.lower() == "contributing items":
        data_structure["contributing_items"] = [
            {"number": int(row['number']), "detail": row['detail'], "related_question_numbers": row['related_question_numbers']}
            for _, row in df.iterrows()
        ]
    elif sheet_name.lower() == "weights section":
        data_structure["weights_section"] = [
            {"number": int(row['number']), "detail": row['detail'], "related_question_weights": row['related_question_weights']}
            for _, row in df.iterrows()
        ]
    elif sheet_name.lower() == "evaluation map":
        data_structure["evaluation_map"] = {row['value']: row['name'] for _, row in df.iterrows()}
    elif sheet_name.lower() == "parent value map":
        data_structure["parent_value_map"] = {row['value']: row['name'] for _, row in df.iterrows()}
    elif sheet_name.lower() == "severity":
        data_structure["severity_ranges"] = df.to_dict(orient='records')
    elif sheet_name.lower() == "age group":
        data_structure["age_group_lookups"] = df.to_dict(orient='records')

# Convert the data structure to JSON and display it
json_data_structure = json.dumps(data_structure, indent=4)
print(json_data_structure)
