import pandas as pd
import uuid


def export_csv(data):
    # Flatten candidate info and extract the first element from education_info
    flattened_data = []

    for candidate in data:
        candidate_info = candidate['candidate_info']
        education_info = candidate['education_info'][0]
        row = {
            'name': str(candidate_info['name']),
            'score': str(candidate['score']),
            'rank': str(candidate['rank']),
            'phone': str(candidate_info['phone']),
            'experience': str(candidate['experience']),
            'cgpa': str(education_info['cgpa']),
            'email': str(candidate_info['email']),
            'institution': str(education_info['institution']),
            'department': str(education_info['department']),
        }
        flattened_data.append(row)

    # Create a csv file from the flattened data
    df = pd.DataFrame(flattened_data)

    # Generate unique filename
    filename = 'documents/dump/' + str(uuid.uuid4()) + '.csv'
    df.to_csv(filename, index=False)
