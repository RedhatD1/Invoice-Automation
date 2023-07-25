#  It extracts experience from the extracted section

def extractExperience(tuple_list):
    experience = ''
    for item in tuple_list:
        if 'experience' in item[0].lower():
            experience += item[1]
    return experience

def extractEducation(tuple_list):
    education = ''
    for item in tuple_list:
        if 'education' in item[0].lower():
            education += item[1]
    return education

def extractSkills(tuple_list):
    skills = ''
    for item in tuple_list:
        if 'skills' in item[0].lower():
            skills += item[1]
    return skills

def extractProjects(tuple_list):
    projects = ''
    for item in tuple_list:
        if 'projects' in item[0].lower():
            projects += item[1]
    return projects

def extractAchievements(tuple_list):
    achievements = ''
    for item in tuple_list:
        if 'achievements' in item[0].lower():
            achievements += item[1]
    return achievements

def extractCertifications(tuple_list):
    certifications = ''
    for item in tuple_list:
        if 'certifications' in item[0].lower():
            certifications += item[1]
    return certifications

def extractAward(tuple_list):
    awards = ''
    for item in tuple_list:
        if 'award' in item[0].lower():
            awards += item[1]
    return awards

def extractAbout(tuple_list):
    about = ''
    for item in tuple_list:
        if 'about' in item[0].lower():
            about += item[1]
    return about


def extract(tuple_list):
    dict = {
        'experience': extractExperience(tuple_list),
        'education': extractEducation(tuple_list),
        'skills': extractSkills(tuple_list),
        'projects': extractProjects(tuple_list),
        'achievements': extractAchievements(tuple_list),
        'certifications': extractCertifications(tuple_list),
        'award': extractAward(tuple_list),
        'about': extractAbout(tuple_list),
    }
    return dict