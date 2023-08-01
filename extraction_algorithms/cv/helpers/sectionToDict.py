#  It extracts experience from the extracted section
from typing import Dict


def extract_attribute(tuple_list: list, attribute: str) -> str:
    attribute_text = ''
    for item in tuple_list:
        if attribute in item[0].lower():
            attribute_text += item[1]
    return attribute_text


def extract(tuple_list: list) -> Dict:
    info_dict = {
        'experience': extract_attribute(tuple_list, 'experience'),
        'education': extract_attribute(tuple_list, 'education'),
        'skills': extract_attribute(tuple_list, 'skills'),
        'projects': extract_attribute(tuple_list, 'projects'),
        'achievements': extract_attribute(tuple_list, 'achievements'),
        'certifications': extract_attribute(tuple_list, 'certifications'),
        'award': extract_attribute(tuple_list, 'award'),
        'about': extract_attribute(tuple_list, 'about'),
        'research': extract_attribute(tuple_list, 'research'),
        'publications': extract_attribute(tuple_list, 'publications'),
        'course': extract_attribute(tuple_list, 'course'),
        'thesis': extract_attribute(tuple_list, 'thesis'),
        'summary': extract_attribute(tuple_list, 'summary')
    }
    return info_dict
