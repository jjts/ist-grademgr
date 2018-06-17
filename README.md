# grademgr - a Python script to insert student or student group grades in a global grade sheet

Written by Jose T. de Sousa (jts@inesc-id.pt)

## Make sure you have Python installed. The script has been tested in Python version 2.7.9


## Go to Fenix and generate the student spreadsheet (for example students.csv). Make sure ut contains information on student gropus, if you want to insert group grades in all students of the group.


## Open the spreadsheet and write it out as CSV file in the same directory where you will run grademgr

## Prepare your grade files

### Individual student grades file format

    	    Number,		EvalItem1, ...,		EvalItemN
	    [student number]	[EvalItem1 grade]	[EvalItemN grade]
	    ...	     		...	   		...
	    [student number]	[EvalItem1 grade]	[EvalItemN grade]

	    * Rows do not need to be ordered


### Group grades file format

    	    Number,		EvalItem1, ...,		EvalItemN
	    [group number]	[EvalItem1 grade]	[EvalItemN grade]
	    ...	     		...	   		...
	    [group number]	[EvalItem1 grade]	[EvalItemN grade]

	    * Rows do not need to be ordered


## Run the porgram to generate a database

$ grademgr --create_db students.csv

This creates a database stored in file sdb.csv containing students' number, name and group


## Run the program to insert individual  grades

$ grademgr --insert_s your_students_grades.csv

The new evaluation items in your_students_grades.csv will be added to sdb.csv. Existing items will be updated.


## Run the program to insert group grades

$ grademgr --insert_g your_groups_grades.csv

The new evaluation items in your_students_grades.csv will be added to sdb.csv. Existing items will be updated.


* Enjoy and feel free to comment, fix, upgrade, etc.
