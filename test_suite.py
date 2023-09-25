import pytest
from main import get_pages_past_year, filter_title, get_article_by_id
from db_conn import db_conn, article_dict, comment_dict

def test_article_comment_length():
    # Get an article
    past_year = get_pages_past_year()
    past_hire = filter_title(past_year)
    article = past_hire[0]
    article_id = article.get("objectID")
    article_data = get_article_by_id(article_id)
    com_list = article_data.get("children")
    assert len(com_list) >= 100


def test_database_functionality():
    # Create a database connection in memory
    db = db_conn(":memory:")
    # Create a table for the articles
    db.create_table("articles", article_dict)
    # check that the table exists
    results = db.query_raw("SELECT name FROM sqlite_master WHERE type='table';")
    assert results[0][0] == "articles"  # Check that the table exists
        
    db.insert("articles", {"objectID": 1, "title": "test"})
    results = db.query_raw("SELECT * FROM articles;")
    assert results[0][0] == 1  # Check that the object ID matches


if __name__ == "__main__":
    pytest.main()
