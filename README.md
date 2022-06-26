# WDDA Students project

This [repository](https://github.com/HaKePlan/bfh-wdda) is for a students project

Project group members:

## Repository content
* root: organizing files and flask server
  * organizing files: `README.md`, `.gitignore`
  * `requirement.txt`: requirements to install before running flask
  * `erd-ddl.sql`: sql commands for initializing the database and its model
  * `sampledata_clean.csv`: the dataset which we have to process and use for this project cleaned from `N/A`
  * `main.py`: flask server file
  * `erd_diagram.mdj`: erd diagram (staruml)
  * `voters_by_county_clean.csv`: the dataset with the data needed for task C model 2
* scripts: scripts with the needed code to solve all mandatory tasks
  * `import_data.py`: python code for importing the data to the corresponding tables
  * `exercise_a.sql`: sql commands for task A
  * `exercise_b.py`: python code for task B
  * `exercise_c.R`: R code for task C
  * `exercise_c_data_import.py`: python code for importing needed data for model 2 of task C
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

Create all tables with executing all sql commands from `erd-ddl.sql`

Import the `sampledata_clean.csv` in your database as the table `import_data` (use something like a db browser or tool)

<div style="page-break-after: always;"></div>

Change to the script directory and make `import_data.py` executable and run it
```bash
$ cd scripts
$ chmod 755 import_data.py
$ python ./import_data.py
```

Run the sql commands from `exercise_a.sql` in your favorite sql browser, or simply use the command line shell for sqlite

Screencast (only for BFH members): https://bernerfachhochschule-my.sharepoint.com/:v:/g/personal/claus1_bfh_ch/EXD9pS1ZDz1KqvRlJvK86t4B_j9x9M4FCdZ5PsYx6_XVEw?e=fJPPLS

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

Screencast (only for BFH members): https://bernerfachhochschule-my.sharepoint.com/:v:/g/personal/claus1_bfh_ch/Ef0naIz6TwxEvpluKWba3H8BU-7U63rcaabjXt4RIjTkMg?e=mdACtn

<div style="page-break-after: always;"></div>

## Task C
### Preparation
Run the following commands to create the database with all its data needed for task C
```bash
$ python3 -m venv ./venv
$ source ./venv/bin/activate
$ touch project_data.sqlite
$ cd scripts
$ chmod 755 import_data.py
$ python ./import_data.py
```

### Model 1
Documentation and explanation is in `exeercise_c.R` under `Model 1)`.

### Model 2
Model 2 uses data from the Secretary of State's office of California.  
The used dataset is the voter registration statistics from June 7, 2022, Primary Election '15 Day Report of Registration'.   
*source:* https://www.sos.ca.gov/elections/report-registration/15day-primary-2022

Run the following commands before going to Model 2 or use the command in the R script to set up the Voter table:
```bash
$ cd scripts
$ chmod 755 exercise_c_data_import.py
$ python ./exercise_c_data_import.py
```

Documentation and explanation is in `exeercise_c.R` under `Model 2)`.
