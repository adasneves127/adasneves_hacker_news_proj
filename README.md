# Hacker News API Project
## Alex Dasneves
### COMP 490 | Senior Design and Development

---

### INSTALLATION
This project required Node.js Version 20. Please follow these instructions to update your version of Node.

To install Node,js 20, I have provided a shell script to automate this task.
```bash
sudo bash ./install_node.sh
```

If you are getting an issue with installing, please run:
```bash
sudo apt-get purge nodejs npm
sudo apt-get autoremove
```
then run the installation script again.


Once Node.js is installed, please run
```npm install``` to install all required packages.

---
### COMPILING
This project is written in Typescript, which Node.js cannot run natively.

To compile this into JavaScript, please run:
```bash
npm run compile
```

---

### EXECUTING

To execute this program, type ```node index.js```. The program will start gathering data from the Agnolia API provided, and save its results to 'output.txt'
