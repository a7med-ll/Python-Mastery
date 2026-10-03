from l5_021_vector_search import (
    dot_product,
    magnitude,
    cosine_similarity,
    nearest_neighbors,
    vector_store,
)


def test_dot_product():
    assert dot_product([1, 2], [3, 4]) == 11


def test_cosine_identical_vectors():
    result = cosine_similarity([1, 2, 3], [1, 2, 3])
    assert round(result, 5) == 1.0


def test_zero_vector():
    result = cosine_similarity([0, 0, 0], [1, 2, 3])
    assert result == 0.0


def test_nearest_neighbors():
    query = [0.85, 0.2, 0.3]

    results = nearest_neighbors(query, vector_store, top_k=2)

    assert len(results) == 2
    assert results[0][2] >= results[1][2]