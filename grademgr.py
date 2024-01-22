#!/usr/bin/python
import csv, sys
from subprocess import call
from os import system

#define group number of elements range(min,max+1) here
groupr = range(1,4)

#define grade range(min,max+1) here
grader = range(0,21)


#global variable
database = []
eval_items = []

#
# Find index in dict
#
def find_index(dicts, key, value):
    class Null: pass
    for i, d in enumerate(dicts):
        if d.get(key, Null) == value:
            return i
    else:
        raise ValueError('no dict with the key and value combination found')


#
# Save database
#
def saveDB():

    global eval_items

    with open('sdb.csv', 'w') as f:
        writer = csv.DictWriter(f, ['Number', 'Name', 'Group']+eval_items, delimiter=',')
        
        writer.writeheader()
        writer.writerows(database)
        f.close()


#
# Create database
#
def createDB(filename):

    global database
    
    # read students file into dict
    with open(filename,  'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            database.append(line)
        f.close()

    # use these keys only 
    keys = ['Number', 'Name', 'Group']

    # delete other keys
    unwanted = set(database[0].keys()) - set(keys)

    for i in range(len(database)):
        for unwanted_key in unwanted: del database[i][unwanted_key]

    saveDB()

    
#
# Load database
#
def loadDB():
    global eval_items
    with open('sdb.csv',  'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            database.append(line)
        f.close()

    eval_items = [x for x in reader.fieldnames if x not in ['Number','Name','Group']]


#
# Reads student grades from file and inserts in database
#
def insertStudentGrades (studentGrades_file):

    global eval_items
    newitems = []
    
    # load database
    loadDB()

    #create student grade dict
    studentGrades = []
    with open(studentGrades_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            studentGrades.append(line)
        f.close()

    #update eval items
    newitems = reader.fieldnames
    newitems.remove('Number')

    # insert new items in eval items
    eval_items.extend([i for i in newitems if i not in eval_items])

    # insert in database
    for student in studentGrades:
        for eval_item in newitems:
            (database[find_index(database, 'Number', student['Number'])])[eval_item]=student[eval_item]


    # save database
    saveDB()



def insertGroupGrades (groupGrades_file):

    global eval_items
    newitems = []
    
    # load database
    loadDB()
    
    #create group grades dict
    groupGrades = []
    with open(groupGrades_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            groupGrades.append(line)
        f.close()

    #update eval items
    newitems = reader.fieldnames
    newitems.remove('Number')

    # insert new items in eval items
    eval_items.extend([i for i in newitems if i not in eval_items])

    # insert in database
    for group in groupGrades:
        student_list = [student for student in database if student['Group'] == group['Number']]
        
        for student in student_list:
            for eval_item in newitems:
                (database[find_index(database, 'Number', student['Number'])])[eval_item]=group[eval_item]

    # save database
    saveDB()

#
# Display program usage
#
def usage ():
    print('usage: gradmgr --create_db students.csv')
    print('       gradmgr --insert_s sgrades.csv')
    print('       gradmgr --insert_g ggrades.csv')
    
   
####################################################################
# Main
####################################################################
def main () :

    if(len(sys.argv) != 3):
        usage()
        sys.exit(1)

    if( sys.argv[1] == '--create_db' ):
        createDB(sys.argv[2])
    elif( sys.argv[1] == '--insert_s' ):
        insertStudentGrades(sys.argv[2])
    elif( sys.argv[1] == '--insert_g' ):
        insertGroupGrades(sys.argv[2])
    else:
        usage()
                        
if __name__ == "__main__" : main ()

