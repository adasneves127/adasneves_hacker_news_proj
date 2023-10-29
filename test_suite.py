import pytest
from main import get_pages_past_year, filter_title, get_article_by_id
from db_conn import db_conn, article_dict, comment_dict
from datetime import datetime
from app import app
from threading import Thread
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium import webdriver


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
    results = db.exec_raw("SELECT name FROM sqlite_master WHERE type='table';")
    assert results[0][0] == "articles"  # Check that the table exists

    db.insert("articles", {"objectID": 1, "title": "test"})
    results = db.exec_raw("SELECT * FROM articles;")
    assert results[0][0] == 1  # Check that the object ID matches


def test_age_filter(tmp_path):
    f1 = tmp_path / "test.db"
    db = db_conn(f1)
    db.create_table("articles", article_dict)
    db.create_table("comments", comment_dict)
    db.insert("articles", {
        "objectID": 1,
        "created_at": datetime.fromtimestamp(0),
        "title": "Ask HN: Test"
    })
    db.insert("comments", {
        "id": 2,
        "parent_id": 1,
        "company": "Dasneves Data",
        "location": "Somewhereville, MA",
        "salary_low": "75000",
        "salary_high": "100000",
        "created_at": 1659326400
    })
    db.insert("comments", {
        "id": 3,
        "parent_id": 1,
        "company": "Santore Software",
        "location": "Nowhereville, MA",
        "salary_low": "100000",
        "salary_high": "100001",
        "created_at": 1690862400
    })
    date = 1690362400

    res = db.exec_raw(f"select * from comments where created_at > {date}")
    db.close()
    # Make sure we get one and only one comment
    assert len(res) == 1
    # Make sure we get the correct comment
    assert res[0][0] == 3


def test_gui_placement():
    # Create a thread for our web app. Daemon says don't wait for process end
    web_thread = Thread(target=app.run, daemon=True)
    web_thread.start()  # Start the server
    db = db_conn('output.db')  # Get an article from the database
    CID = 33068430
    query = f"SELECT * FROM comments WHERE ID={CID}"
    # Strip whitespace from end
    results = [str(x).strip() for x in db.exec_raw(query)[0]]
    db.close()
    # Create a Firefox Selenium Instance
    options = FirefoxOptions()
    options.add_argument('--headless')  # No window!
    driver = webdriver.Firefox(options=options)
    # Get the site, compare that everything looks good
    driver.get("localhost:5000/expand/33068430")
    assert driver.find_element(By.ID, 'CID').text == f'View Comment {CID}'
    assert driver.find_element(By.ID, 'CompanyName').text ==\
        f'Company Name: {results[2]}'
    assert driver.find_element(By.ID, 'Salary').text == \
        f"Salary Range: ${results[4]}-${results[5]}"
    assert driver.find_element(By.ID, 'Location').text ==\
        f"Location: {results[3]}"
    assert driver.find_element(By.ID, 'Comment').text ==\
        "Comment:\n" + results[6]
    driver.close()  # Close the firefox instance


def test_salary_range(tmp_path):
    f1 = tmp_path / "test.db"
    db = db_conn(f1)
    db.create_table("articles", article_dict)
    db.create_table("comments", comment_dict)
    db.insert("articles", {
        "objectID": 1,
        "created_at": datetime.fromtimestamp(0),
        "title": "Ask HN: Test"
    })
    db.insert("comments", {
        "id": 2,
        "parent_id": 1,
        "company": "Dasneves Data",
        "location": "Somewhereville, MA",
        "salary_low": "75000",
        "salary_high": "100000",
        "created_at": 1659326400
    })
    db.insert("comments", {
        "id": 3,
        "parent_id": 1,
        "company": "Santore Software",
        "location": "Nowhereville, MA",
        "salary_low": "200000",
        "salary_high": "400000",
        "created_at": 1690862400
    })
    # Get data from database
    query = "SELECT * FROM comments " + \
            "WHERE salary_low > 150000 " + \
            "and salary_high < 400000"
    results = db.exec_raw(query)
    assert len(results) == 1
    assert results[0][0] == 2


def test_filters():
    # web_thread = Thread(target=app.run, daemon=True)
    # web_thread.start()  # Start the server
    options = FirefoxOptions()
    options.add_argument('--headless')  # No window!
    driver = webdriver.Firefox(options=options)
    driver.get("localhost:5000/view")
    table_unfiltered = driver.find_element(By.ID, "data_table")
    # Get the rows in the table
    rows_unfiltered = len(table_unfiltered.find_elements(By.TAG_NAME, "tr"))

    # Apply a Filter
    driver.get("localhost:5000/view?keywords=python")
    table_filtered = driver.find_element(By.ID, "data_table")
    rows_filtered = len(table_filtered.find_elements(By.TAG_NAME, "tr"))
    assert rows_filtered <= rows_unfiltered

    # Apply a second filter
    driver.get("localhost:5000/view?keywords=python,java")
    table_double_filtered = driver.find_element(By.ID, "data_table")
    rows_double_filtered = len(
        table_double_filtered.find_elements(
            By.TAG_NAME, "tr")
        )
    assert rows_double_filtered <= rows_filtered


if __name__ == "__main__":
    pytest.main()
