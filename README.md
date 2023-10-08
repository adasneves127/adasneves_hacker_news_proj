# Hacker News API Project

## Programmed By: Alex Dasneves

### COMP 490 | Senior Design and Development

---

### Installing

To install this project, create and source a new venv using the following commands

```BASH
python3.10 -m venv venv
```

followed by:

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

To execute the code in this project, execute `flask run` in your terminal. Then, open the [web interface](http://localhost:5000)

To get data from the Agnolia API, press the `Get Data` button. This will begin to get the articles posted on the forum since September 1st, 2022. This will take roughly 5-15 minutes, depending on CPU speed, and network speed.

To view the data, press the `View Data` button. This will load a table on your screen to search through.
