from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""
def generate_match_score(applicant_cv: str, job_description: str) -> float:
This function takes the applicant's CV and the job description as input
It then generates a match score between the CV and the job description
This is done on the cosine simialrity between the CV and the job description
"""


def generate_match_score(applicant_cv: str, job_description: str) -> float:
    cv = CountVectorizer()
    matrix = cv.fit_transform([applicant_cv, job_description])
    similarity_matrix = cosine_similarity(matrix)
    return round(similarity_matrix[0][1] * 100, 2)
