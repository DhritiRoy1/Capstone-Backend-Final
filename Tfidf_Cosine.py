import FlaskApp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
print(FlaskApp.goals,FlaskApp.data)
def calculate_scores_for_titles(goals_array, titles_array):
    """
    Calculates the Cosine Similarity score for a list of page titles 
    against a combined user goal.
    
    Args:
        goals_array (list): List of user's goals (e.g., ["study python", "apply for jobs"]).
        titles_array (list): List of page titles to score (e.g., ["Python Tutorial 1", "Funny Cat Video"]).
        
    Returns:
        list: An array of similarity scores (floats) corresponding to the input titles.
    """
    if not goals_array or not titles_array:
        if not goals_array:
            return "goals_array"
        else:
            return "titles_array"

    # 1. Create the 'super-goal' document
    user_goal_document = " ".join(goals_array)
    
    # 2. Define the Corpus
    # The corpus must contain the goal document PLUS all the titles to be compared.
    # [Goal, Title1, Title2, Title3, ...]
    corpus = [user_goal_document] + titles_array
    print(corpus)
    
    # 3. Vectorize the Corpus
    # The vectorizer fits on ALL text, determining word importance across the entire set.
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    print(tfidf_matrix)

    
    # 4. Calculate Cosine Similarity
    # We compare the Goal vector (index 0) against ALL other vectors (index 1 onwards).
    # Since the matrix includes the goal itself, we take the entire first row.
    cosine_score_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    print(cosine_score_matrix)
    
    # 5. Extract and Return Scores
    # The result is the first row of the matrix. We discard index [0][0] (Goal vs. Goal) 
    # and return the rest, which are the scores for Title1, Title2, etc.
    
    # [0] selects the first row of the matrix (the row showing scores against the Goal)
    # [1:] selects all scores starting from the second element (Title 1's score).
    similarity_scores = cosine_score_matrix[0][0:].tolist() 
    
    return similarity_scores
print(calculate_scores_for_titles(FlaskApp.goals,FlaskApp.data))