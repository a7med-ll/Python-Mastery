import math

def dot_product(vector_a, vector_b):
    """Applying dot product between two vectors to use cosine similarity"""

    return sum(a * b for a, b in zip(vector_a, vector_b))           # -->  returns dot product between two vectors

def magnitude(vector):
    """finding the magnitude of a vector"""

    return math.sqrt(sum(a ** 2 for a in vector))  # --> vector magnitude formula

def cosine_similarity(vector_a, vector_b):
    """Applying cosine similarity between two vectors."""

    if len(vector_a) != len(vector_b):   # --> checking vector dimensions
        raise ValueError("vector_a and vector_b must have the same dimension")

    magnitude_a = magnitude(vector_a)  # --> magnitude of vec a
    magnitude_b = magnitude(vector_b)  # --> magnitude of vector b

    # Zero divisible check
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    # else we return the cosine similarity
    return dot_product(vector_a, vector_b) / (magnitude_a * magnitude_b)

#------------------------------------------------------------------------------------
# Vector store to apply k nearst neighbour and cosine similarity
#------------------------------------------------------------------------------------

vector_store = [
    {
        "id": "doc_1",
        "text": "Python is a programming language",
        "vector": [0.9, 0.1, 0.2]               # --> vector
    },
    {
        "id": "doc_2",
        "text": "Machine learning uses data",
        "vector": [0.8, 0.3, 0.4]               # --> vector
    },
    {
        "id": "doc_3",
        "text": "Football is a popular sport",
        "vector": [0.1, 0.9, 0.2]              # --> vector
    },
    {
        "id": "doc_4",
        "text": "Basketball players score points",
        "vector": [0.2, 0.8, 0.3]             # --> vector
    }
]

#------------------------------------------------------------------------------------
# K nearest neighbours
#------------------------------------------------------------------------------------

def nearest_neighbors(query_vector, vector_store, top_k=2):
    scores = []

    for item in vector_store:
        score = cosine_similarity(query_vector, item["vector"])
        scores.append((item["id"], item["text"], score))

    scores.sort(key=lambda x: x[2], reverse=True)

    return scores[:top_k]

#------------------------------------------------------------------------------------
# QUERY IT
#------------------------------------------------------------------------------------

query_vector = [0.85, 0.2, 0.3]

results = nearest_neighbors(query_vector, vector_store, top_k=2)

for doc_id, text, score in results:
    print(doc_id, text, score)
