import web_utils
from urllib import parse
from datetime import datetime
import db_conn
import utils
from typing import List
import threading


threads: List[List[threading.Thread | str]] = []


def get_article_by_id(id: int):
    article = web_utils.get_data(f"http://hn.algolia.com/api/v1/items/{id}")
    return article


def get_all_pages():
    page_num = 0
    articles = []

    page_data = web_utils.get_data(
        f"""http://hn.algolia.com/api/v1/search?query={
            parse.quote('Ask HN: Who is Hiring?')
            }"""
    )

    page_count = page_data.get("nbPages")

    while page_num < page_count:
        page_data = web_utils.get_data(
            f"""http://hn.algolia.com/api/v1/search?query={
                parse.quote('Ask HN: Who is Hiring?')
                }&page={page_num}"""
        )
        articles.extend(page_data.get("hits"))
        page_num += 1

    return articles


def get_pages_past_year():
    all_articles = get_all_pages()
    date_now = datetime.fromtimestamp(1693540800)

    articles_within_year = []
    for article in all_articles:
        article_date = datetime.fromtimestamp(article.get("created_at_i"))
        if article_date.year == date_now.year:
            articles_within_year.append(article)
        elif (
            article_date.year == date_now.year - 1
            and article_date.month > date_now.month
        ):
            articles_within_year.append(article)
    return articles_within_year


def filter_title(articles: list):
    valid_articles = []
    for article in articles:
        if str(article.get("title", "")).startswith("Ask HN: Who is hiring? ("):
            valid_articles.append(article)
    return valid_articles


def init_db(thread_id: int):
    threads[thread_id][1] = "Creating database"
    db = db_conn.db_conn("output.db")
    # Create a table for the articles
    threads[thread_id][1] = "Creating tables"
    db.create_table("articles", db_conn.article_dict)
    db.create_table("comments", db_conn.comment_dict)

    return db


def save_articles(db: db_conn.db_conn, articles, thread_id: int):
    for art_idx, article in enumerate(articles):
        db.insert("articles", article)
        article_id = article.get("objectID")
        article_data = get_article_by_id(article_id)
        com_list = article_data.get("children")
        for com_idx, comment in enumerate(com_list):
            export_status(art_idx, len(articles), com_idx, len(com_list),
                          thread_id)
            comment_data = utils.get_comment_dict(comment)
            if comment_data is not None:
                db.insert("comments", comment_data)


def project_2_main(thread_id: int):
    threads[thread_id][1] = "Getting articles"
    # Get the 12 articles from the past year
    past_year = get_pages_past_year()
    # Filter out the articles that don't start with "Ask HN: Who is hiring? ("
    threads[thread_id][1] = "Filtering articles"
    past_hire = filter_title(past_year)
    # Create a database connection

    db = init_db(thread_id)

    save_articles(db, past_hire, thread_id)

    db.close()
    threads[thread_id][1] = "Done"


def export_status(art_cnt, art_ttl, com_cnt, com_ttl, TID: int):
    threads[TID][1] = \
        f"Article {art_cnt + 1}/{art_ttl} Comment {com_cnt + 1}/{com_ttl}"


# This is the code for project 1
def project_1_main():
    past_year = get_pages_past_year()
    past_hire = filter_title(past_year)
    with open("output.txt", "w") as f:
        f.write("Title, Comments\n")
        f.writelines(
            [
                f"""{
            ','.join([x['title'], str(x['num_comments'])])
            }\n"""
                for x in past_hire
            ]
        )


def get_from_db(query: str):
    db = db_conn.db_conn("output.db")

    results = db.exec_raw(query)
    db.close()
    return results


if __name__ == "__main__":
    threads.append([threading.Thread(target=project_2_main, args=[0]), ""])
    threads[-1][0].start()
    try:
        while True:
            print(threads[0][1])
            if threads[0][1] == "Done":
                threads[0][0].join()
                break
    except KeyboardInterrupt:
        for thread in threads:
            thread[0].join()
