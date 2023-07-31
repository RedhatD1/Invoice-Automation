from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def generate_match_score(applicant_cv: str, job_description: str):
    cv = CountVectorizer()
    matrix = cv.fit_transform([applicant_cv, job_description])
    similarity_matrix = cosine_similarity(matrix)
    return round(similarity_matrix[0][1] * 100, 2)
