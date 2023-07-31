import pandas as pd
import uuid


def export_csv(data):
    # Flatten candidate info and extract the first element from education_info
    flattened_data = []

    for candidate in data:
        candidate_info = candidate.get('candidate_info', {})
        education_info = candidate.get('education_info', [{}])[0]
        row = {
            'name': str(candidate_info.get('name', '')),
            'score': str(candidate.get('score', '')),
            'rank': str(candidate.get('rank', '')),
            'phone': str(candidate_info.get('phone', '')),
            'experience': str(candidate.get('experience', '')),
            'cgpa': str(education_info.get('cgpa', '')),
            'email': str(candidate_info.get('email', '')),
            'institution': str(education_info.get('institution', '')),
            'department': str(education_info.get('department', '')),
        }
        flattened_data.append(row)

    # Create a csv file from the flattened data
    df = pd.DataFrame(flattened_data)

    # Generate unique filename
    filename = 'documents/dump/' + str(uuid.uuid4()) + '.csv'
    df.to_csv(filename, index=False)
