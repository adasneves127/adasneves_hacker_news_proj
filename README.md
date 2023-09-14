# Hacker News API Project
## Alex Dasneves
### COMP 490 | Senior Design and Development

---

### INSTALLATION
This project required NodeJS Version 20. Please follow these instructions to update your version of Node.

To install NodeJS 20, I have provided a shell script to automate this task.
```bash
bash ./install_node.sh
```

If you are getting an issue with installing, please run:
```bash
sudo apt-get purge nodejs npm
sudo apt-get autoremove
```
then run the install script again.


Once NodeJS is installed, please run
```npm install``` to install all required packages.

---
### COMPILING
This project is written in Typescript, which NodeJS cannot run natively.

To compile this into JavaScript, please run:
```bash
npm run compile
```

---

### EXECUTING

To execute this program, type ```node index.js```. The program will start gathering data from the Agnolia API provided, and save its results to 'output.txt'
