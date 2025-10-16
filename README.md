## Prerequisites
1. Python
2. Git
3. Postgresql
a. Remember your username and password (default is “postgres” with no “password”)
b. Follow schema.sql to create db, tables, and insert some movies beforehand


## Instructions to run:
1. Clone the repo
   `git clone https://github.com/Ashiq5/demo2cs4604.git`
2. Navigate to the cloned directory
3. Create a virtual environment
    `python3 -m venv .venv/`
4. Activate the environment
    `source .venv/bin/activate`
5. Install requirements
    `pip install -r requirements.txt`
6. Run app.py
   `flask --app app run`