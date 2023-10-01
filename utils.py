"""Contains utilities for finding data within comments"""

import spacy
import re
from bs4 import BeautifulSoup


nlp = spacy.load("en_core_web_sm")


def get_comment_location(comment_text: str):
    # Look at the next element to see if it's a location or
    #                                  position using spacy

    # Only look at the first 100 characters.
    doc = nlp(comment_text[:100])
    location = ""

    # Iterate through the items found by Spacy and see if they are location
    for entity in doc.ents:
        if entity.label_ == "GPE":
            location += entity.text + ","

    if "remote" in comment_text.lower():
        location += "Remote,"

    if "part time" in comment_text.lower():
        location += "Part-Time,"

    return location.lstrip("<p>").rstrip(",")


def get_comment_salary(comment_text: str, return_dict: dict):
    salary = re.search(r"\$([0-9]+k)-?\$([0-9]+k)?", comment_text)
    if salary is not None:
        return_dict["salary_low"] = salary.group(1)
        return_dict["salary_high"] = salary.group(2)


def get_comment_dict(comment: dict):
    return_dict = {}
    comment_text = BeautifulSoup(comment.get("text")).text
    if comment_text is None:
        return None
    split_text = comment_text.split("|")

    return_dict["company"] = split_text[0]
    if len(return_dict["company"]) > 20:
        return_dict["company"] = return_dict["company"].split(" ")[0]
    return_dict["id"] = comment["id"]
    return_dict["parent_id"] = comment["parent_id"]
    return_dict["location"] = get_comment_location(comment_text)
    get_comment_salary(comment_text, return_dict)

    return_dict["raw_comment"] = comment_text

    return return_dict
