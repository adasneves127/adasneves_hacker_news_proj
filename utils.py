"""Contains utilities for finding data within comments"""

import spacy
import re
from bs4 import BeautifulSoup
import string


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
            location += entity.text + "\n"

    if "remote" in comment_text.lower():
        location += "Remote\n"

    if any(["parttime" in comment_text.lower().replace(x, "")
            for x in string.punctuation + string.whitespace]):
        location += "Part Time\n"

    return location.lstrip("<p>").rstrip(",")


def get_comment_salary(comment_text: str, return_dict: dict):
    for char in string.whitespace:
        comment_text = comment_text.replace(char, "")
    pay = re.search(r"\$?([0-9\.]+k?)-\$?([0-9]+k)?", comment_text)
    if pay is not None:
        return_dict["salary_low"] = int(pay.group(1).replace('k', '')) * 1E3

        return_dict["salary_high"] = int(pay.group(2).replace('k', '')) * 1E3


def get_comment_dict(comment: dict):
    return_dict = {}
    raw = comment.get("text")
    if raw is None:  # or "[dead]" in raw or "[flagged] in raw"
        return None
    comment_text = BeautifulSoup(raw, features="html.parser").text
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
