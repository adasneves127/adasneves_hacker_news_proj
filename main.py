import web_utils
from urllib import parse
from datetime import datetime
import db_conn


def get_comment_dict(comment: dict):
    return_dict = {}
    company_name = comment["text"].split(";")
    print(company_name)
    return_dict["id"] = comment["id"]
    return_dict["parent_id"] = comment["parent_id"]
    comment_text = comment["text"]
    split_text = comment_text.split("|")
    # We always know that the company name is the first element
    return_dict["company"] = split_text[0]
    
    # We need to look at the next element to see if it's a location or position
    
    
    return return_dict
    
    
def get_article_by_id(article_id: int):
    article = web_utils.get_data(
        f"http://hn.algolia.com/api/v1/items/{article_id}"
    )
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


def project_2_main():
    # Get the 12 articles from the past year
    past_year = get_pages_past_year()
    # Filter out the articles that don't start with "Ask HN: Who is hiring? ("
    past_hire = filter_title(past_year)
    # Create a database connection
    db = db_conn.db_conn("output.db")
    # Create a table for the articles
    db.create_table("articles", db_conn.article_dict)
    db.create_table("comments", db_conn.comment_dict)
    for article in past_hire:
        db.insert("articles", article)
        print(article.get("title"))
        article_id = article.get("objectID")
        article_data = get_article_by_id(article_id)
        for comment in article_data.get("children"):
            comment_data = get_comment_dict(comment)
            db.insert("comments", comment_data)
            
    db.close()


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
