# Hacker News API Project

## Programmed By: Alex Dasneves

### COMP 490 | Senior Design and Development

---

### Installing

To install this project, create and source a new venv using the commands `python3.10 -m venv venv` followed by:

#### BASH/ZSH

`source ./venv/bin/activate`

#### Windows Powershell

`./venv/bin/Activate.ps1`

#### Free-BSD

`source ./venv/bin/activate.csh`

#### FISH Shell

`. venv/bin/activate.fish`

### Installing required packages

To install required packages, use python's PIP command as follows:
`pip3.10 install -r requirements.txt`

---

### Usage

To run the program, use `python3.10 main.py`. The program will begin execution, gathering all the "Who is Hiring" pages from the past 12 months, and putting them in a "output.db" file.

---

### Viewing Data

To view the output, you can use the [DB Browser for SQLite](https://sqlitebrowser.org/) or [Jetbrains DataGrip](https://www.jetbrains.com/datagrip/).

The results are stored in 2 tables. The first, 'Articles' contains the title, ID, and total number of comments per each article.

The second database, 'Comments' shows all the parsed comment data, with the Comment ID, the Parent (Article) ID, Location, Company Name, and Salary (If Provided), as well as the raw text of the comment.
