import pandas as pd
import uuid


"""
def export_csv(data):

This function takes the dictionary variable 'data' as input
This input variable is contains all the detected sections as a dictionary
The function then flattens the dictionary and exports it as a CSV file
All missing data are handled accordingly
"""


def export_csv(data) -> str:
    # Flatten candidate info and extract the first element from education_info
    flattened_data = []

    for candidate in data:
        try:
            candidate_info = candidate.get('candidate_info', {})
        except AttributeError:
            candidate_info = {}
        if len(candidate['education_info']):
            education_info = candidate.get('education_info', [{}])[0]
        else:
            education_info = {}
        row = {
            'rank': str(candidate.get('rank', '')),
            'name': str(candidate_info.get('name', '')),
            'phone': str(candidate_info.get('phone', '')),
            'email': str(candidate_info.get('email', '')),
            'institution': str(education_info.get('institution', '')),
            'department': str(education_info.get('department', '')),
            'cgpa': str(education_info.get('cgpa', '')),
            'experience': str(candidate.get('experience', '')),
            'score': str(candidate.get('score', '')),
        }
        flattened_data.append(row)

    # Create a csv file from the flattened data
    df = pd.DataFrame(flattened_data)

    # Generate unique filename
    filename = 'assets/dump/' + str(uuid.uuid4()) + '.csv'
    df.to_csv(filename, index=False)
    return filename
