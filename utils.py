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
    # If the posting has the word 'remote' in it, add it to the location
    if "remote" in comment_text.lower():
        location += "Remote\n"
    # If the word 'part time' appears in any way, add it to the location
    if any(["parttime" in comment_text.lower().replace(x, "")
            for x in string.punctuation + string.whitespace]):
        location += "Part Time\n"

    # Remove the beginning html tag if needed, and remove trailing commas.
    return location.lstrip("<p>").rstrip(",")


def get_comment_salary(comment_text: str, return_dict: dict):
    # Remove all whitespace from the comment.
    for char in string.whitespace:
        comment_text = comment_text.replace(char, "")
    # Regex that matches a salary range
    regex = r"\$?([0-9]+\.?[0-9]*k?)-(?:\$?([0-9]+\.?[0-9]*k))?"
    # Execute the regex on the comment text.
    # flags=10 means Case Insensitive +multiline.
    pay = re.search(regex, comment_text, flags=10)
    # If we matched
    if pay is not None:
        # Replace the 'k' with nothing
        rep_pay = pay.group(1).replace('k', '')
        try:  # Try to convert to number.
            if float(rep_pay) < 500:  # If is not too high
                # We cast to a float first to catch any decimal points
                return_dict["salary_low"] = int(float(rep_pay) * 1E3)
        except ValueError:  # If we can't convert to a number, do nothing
            pass
        # Check that we got a high end
        if pay.group(2) is not None:
            rep_pay = pay.group(2).replace('k', '')
            try:  # Convert to an integer. 1E3 is sci. notation for 1000
                return_dict["salary_high"] = int(float(rep_pay) * 1E3)
            except ValueError:
                pass


def get_comment_dict(comment: dict):
    # Blank return dict
    return_dict = {}
    # Get the comment text
    raw = comment.get("text")
    # Check that there is text, and it is not dead or flagged
    if raw is None or "[dead]" in raw or "[flagged]" in raw:
        return None
    # Parse the HTML through BeautifulSoup to remove HTML formatting
    comment_text = BeautifulSoup(raw, features="html.parser").text

    # Get the comment and split on pipe symbol
    split_text = comment_text.split("|")
    # The company name is the first entry before the |
    return_dict["company"] = split_text[0]
    # If the company name seems to be too long, just return the first word.
    if len(return_dict["company"]) > 20:
        return_dict["company"] = return_dict["company"].split(" ")[0]
    # Get the ID of the comment and the post it was on
    return_dict["id"] = comment["id"]
    return_dict["parent_id"] = comment["parent_id"]
    # Get the location of the comment
    return_dict["location"] = get_comment_location(comment_text)
    # Find the salary range
    get_comment_salary(comment_text, return_dict)
    # Keep track of the whole text of the comment.
    return_dict["raw_comment"] = comment_text
    return_dict['created_at'] = comment.get('created_at_i')
    return return_dict
