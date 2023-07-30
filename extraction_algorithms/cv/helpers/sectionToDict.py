#  It extracts experience from the extracted section

def extract_experience(tuple_list):
    experience = ''
    for item in tuple_list:
        if 'experience' in item[0].lower():
            experience += item[1]
    return experience


def extract_education(tuple_list):
    education = ''
    for item in tuple_list:
        if 'education' in item[0].lower():
            education += item[1]
    return education


def extract_skills(tuple_list):
    skills = ''
    for item in tuple_list:
        if 'skills' in item[0].lower():
            skills += item[1]
    return skills


def extract_projects(tuple_list):
    projects = ''
    for item in tuple_list:
        if 'projects' in item[0].lower():
            projects += item[1]
    return projects


def extract_achievements(tuple_list):
    achievements = ''
    for item in tuple_list:
        if 'achievements' in item[0].lower():
            achievements += item[1]
    return achievements


def extract_certifications(tuple_list):
    certifications = ''
    for item in tuple_list:
        if 'certifications' in item[0].lower():
            certifications += item[1]
    return certifications


def extract_award(tuple_list):
    awards = ''
    for item in tuple_list:
        if 'award' in item[0].lower():
            awards += item[1]
    return awards


def extract_about(tuple_list):
    about = ''
    for item in tuple_list:
        if 'about' in item[0].lower():
            about += item[1]
    return about


def extract_research(tuple_list):
    research = ''
    for item in tuple_list:
        if 'research' in item[0].lower():
            research += item[1]
    return research


def extract_thesis(tuple_list):
    thesis = ''
    for item in tuple_list:
        if 'thesis' in item[0].lower():
            thesis += item[1]
    return thesis


def extract_publications(tuple_list):
    publications = ''
    for item in tuple_list:
        if 'publications' in item[0].lower():
            publications += item[1]
    return publications


def extract_course(tuple_list):
    course = ''
    for item in tuple_list:
        if 'course' in item[0].lower():
            course += item[1]
    return course


def extract_summary(tuple_list):
    summary = ''
    for item in tuple_list:
        if 'summary' in item[0].lower():
            summary += item[1]
    return summary


def extract(tuple_list):
    info_dict = {
        'experience': extract_experience(tuple_list),
        'education': extract_education(tuple_list),
        'skills': extract_skills(tuple_list),
        'projects': extract_projects(tuple_list),
        'achievements': extract_achievements(tuple_list),
        'certifications': extract_certifications(tuple_list),
        'award': extract_award(tuple_list),
        'about': extract_about(tuple_list),
        'research': extract_research(tuple_list),
        'publications': extract_publications(tuple_list),
        'course': extract_course(tuple_list),
        'thesis': extract_thesis(tuple_list),
        'summary': extract_summary(tuple_list)
    }
    return info_dict
