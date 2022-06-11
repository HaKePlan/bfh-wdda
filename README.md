# WDDA Students project

This repository is for a students project

## Repository content
* root: organising files and flask server
  * organising files: `README.md`, `.gitignore`
  * `requirement.txt`: requirements to install before running flask
  * `erd-ddl.sql`: sql commands for initializing the database and its model
  * `sampledata_clean.csv`: the dataset which we have to process and use for this project cleaned from `N/A`
  * `main.py`: flask server file
* scripts: scripts with the needed code to solve all mandatory tasks
  * `import_data.py`: python code for importing the data to the corresponding tables
  * `exercise_a.sql`: sql commands for task A
  * `exercise_b.py`: python code for task B
  * `exercise_c.R`: R code for task C
* templates: jinja templates for flask

## Task A
Create a new virtual environment and source it
```bash
$ python3 -m venv ./venv
$ source ./venv/bin/activate
```

Create a new sqlite database named `project_data.sqlite` in the project root
```bash
$ touch project_data.sqlite
```

Import the `sampledata_clean.csv` in your database as the table `import_data` (use something like a db browser or tool)

Change to the script directory and make `import_data.py` executable and run it
```bash
$ cd scripts
$ chmod 755 import_data.py
$ python ./import_data.py
```

Run the sql commands from `exercise_a.sql` in your favorite sql browser or simply use the command line shell for sqlite

## Task B
Go in the `scripts` directory and make the script `exercise_b.py` executable
```bash
$ cd scripts
$ chmod 755 exercise_b.py
```

Run the script with its necessary flags (use `-h` for help)
```bash
$ python ./exercise_b.py -y 2020 -c parlier
```

### Task B optional
Install all needed requirements for flask
```bash
$ pip install -r requirements.txt
```

Run the flask server from the command line
```bash
$ export FLASK_APP=main
$ flask run
```

Open your browser on `http://127.0.0.1:5000`

From there on, the web page will show you how to use it ;)

## Task C

