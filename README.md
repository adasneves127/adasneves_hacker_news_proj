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

### Installing Selenium requirements

To use Selenium, please install [geckodriver](https://github.com/mozilla/geckodriver/releases) and Firefox. If you are on Linux, please make sure that your Firefox is installed via Apt, and not Snap.

Please follow [these](https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04) instructions to install Firefox via Apt.

---

### Usage

To execute the code in this project, execute `flask run` in your terminal. Then, open the [web interface](http://localhost:5000)

To get data from the Agnolia API, press the `Get Data` button. This will begin to get the articles posted on the forum since September 1st, 2022. This will take roughly 5-15 minutes, depending on CPU speed, and network speed. The page will automatically refresh once per second, to show the most up-to-date status.

To view the data, press the `View Data` button. This will load a table on your screen to search through.

---

### Testing

Before Testing, please run the program through the steps above to properly fill out the database, as the test of GUI Components requires the `output.db` file to have all the data in it.

Once the database has been populated, run the automated tests with `pytest`

### Additional Test

For my final test, I wrote a test to ensure that my GUI was displaying all the results in the table.
