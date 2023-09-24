
# Freeze the current PIP Requirements
pip3.10 freeze > requirements.txt

python -m black *.py

#LINT!
flake8 *.py
# If the linter fails, then the script should exit.

# Add all files
git add .

# Commit with the argument provided by the user as the message
git commit
# Push to github
git push