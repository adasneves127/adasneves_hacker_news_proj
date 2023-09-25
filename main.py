import web_utils
from urllib import parse
from datetime import datetime
import db_conn
import utils


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
    date_now = datetime.now()

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
        if str(article["title"]).startswith("Ask HN: Who is hiring? ("):
            valid_articles.append(article)
    return valid_articles


def init_db():
    print("Creating database")
    db = db_conn.db_conn("output.db")
    # Create a table for the articles
    print("Creating tables")
    db.create_table("articles", db_conn.article_dict)
    db.create_table("comments", db_conn.comment_dict)


def save_articles(db: db_conn.db_conn, articles):
    for art_idx, article in enumerate(articles):
        db.insert("articles", article)
        article_id = article.get("objectID")
        article_data = get_article_by_id(article_id)
        com_list = article_data.get("children")
        for com_idx, comment in enumerate(com_list):
            print_bottom_status(art_idx, len(articles), com_idx, len(com_list))
            comment_data = utils.get_comment_dict(comment)
            if comment_data is not None:
                db.insert("comments", comment_data)


def project_2_main():
    print("Getting articles")
    # Get the 12 articles from the past year
    past_year = get_pages_past_year()
    # Filter out the articles that don't start with "Ask HN: Who is hiring? ("
    print("Filtering articles")
    past_hire = filter_title(past_year)
    # Create a database connection

    db = init_db()

    save_articles(db, past_hire)

    db.close()


def print_bottom_status(art_count, art_total, com_count, com_total):
    print(
        f"Articles: {art_count + 1}/{art_total} "
        + f"Comments: {com_count + 1}/{com_total}        ",
        end="\r",
    )


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


if __name__ == "__main__":
    project_2_main()
