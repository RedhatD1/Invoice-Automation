from extraction_algorithms.cv.helpers import pdfToInfo


def getJSON(pdfFileName, jobDescription, algorithm='default'):
    pdfFilePath = f"documents/cv/{pdfFileName}"
    return pdfToInfo.extractInfo(pdfFilePath, jobDescription)


# Example Usage
pdfFileName = 'abidbhai.pdf'
jobDescription = """
Job Title: PHP Web Developer & Team Leader

Job Description:

We are seeking an experienced and skilled PHP Web Developer & Team Leader to join our dynamic team. As a core member of our development team, you will be responsible for the end-to-end development of web applications, ensuring seamless integration of front-end and back-end components. Your role will involve leading and mentoring a team of developers, overseeing project progress, and collaborating with stakeholders throughout the development lifecycle.

Key Responsibilities:

Proficient in core PHP, HTML, JavaScript, jQuery, AJAX, and CSS Bootstrap.
Strong knowledge of relational database systems, particularly MySQL.
Experience in server maintenance and cPanel configuration.
Lead and manage a team of developers, coordinating tasks, evaluations, and schedules.
Perform requirements analysis, planning, and design of web applications.
Develop and maintain technical documentation and process documentation.
Provide technical training and support to the development team.
Troubleshoot and resolve issues during the development process and in production support.
Familiarity with version control systems like GIT for collaborative development.
Experience in integrating APIs for YouTube, Facebook, Google, SMS, and payment gateways.
Knowledge of HTML-5, Silverlight, Sass, Bootstrap, and AngularJS is a plus.

Qualifications:

Bachelor's degree in Computer Science, Engineering, or related field.
Proven experience in PHP development, preferably in a team lead or management role.
Strong programming knowledge in PHP, JavaScript, HTML/CSS, and web application development.
Solid understanding of front-end and back-end integration using AJAX and other technologies.
Ability to create and manage technical documents and project-related documentation.
Excellent troubleshooting and problem-solving skills.
Prior experience with API integration and third-party services.
Familiarity with web development best practices and coding standards.
"""

output = getJSON(pdfFileName, jobDescription)
# add an optional argument 'algorithm' to specify which algorithm to use
# currently no other algorithm is implemented
for key, value in output.items():
    print(f'{key}: {value}')