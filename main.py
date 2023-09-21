import web_utils
from urllib import parse
from datetime import datetime


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
        elif article_date.year == date_now.year - 1 \
                and article_date.month > date_now.month:
            articles_within_year.append(article)
    return articles_within_year


def filter_title(articles: list):
    valid_articles = []
    for article in articles:
        if str(article['title']).startswith("Ask HN: Who is hiring? ("):
            valid_articles.append(article)
    return valid_articles


def main():
    past_year = get_pages_past_year()
    past_hire = filter_title(past_year)
    with open("output.txt", 'w') as f:
        f.write("Title, Comments\n")
        f.writelines([f"""{
            ','.join([x['title'], str(x['num_comments'])])
            }\n""" for x in past_hire])


if __name__ == "__main__":
    main()
