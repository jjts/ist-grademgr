#!/usr/bin/python
import csv, sys
from subprocess import call
from os import system

#define group number of elements range(min,max+1) here
groupr = range(1,4)

#define grade range(min,max+1) here
grader = range(0,21)


#global variables 
data = []
agrupamentos = []

####################################################################
def printGrades(filename, items):
    if not (set(items).issubset(data[0].keys())):
        print 'Some items are not valid. Try again.'
        return
    keys = ['N\xfamero', 'Nome']+agrupamentos+items
    with open(filename, 'wb') as f:
        writer = csv.DictWriter(f, keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
        f.close()

####################################################################
def saveDB(filename):
    system('mv '+filename+' '+filename+'.bak')
    with open(filename, 'wb') as f:
        writer = csv.DictWriter(f, data[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(data)
        f.close()

####################################################################
def loadDB(filename):
    global agrupamentos
    with open(filename,  'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            data.append(line)
        f.close()
    agrupamentos = [s for s in data[0].keys() if "Agrup" in s]

####################################################################
def listGroupElements(agrupamento, groupname):
    return [item for item in data if item[agrupamento] == groupname]

####################################################################
def getGroupInfo(studentNumber):
    student = listStudent(studentNumber).pop(0)
    print agrupamentos
    for agrupamento in agrupamentos:
        agrup = agrupamento
        if student[agrupamento] != '':
            print agrup
            break
    groupInfo = []
    groupInfo.append(agrup)
    groupInfo.append(student[agrupamento])
    return groupInfo


    
####################################################################
# ls student_number
####################################################################
def listStudent(studentNumber):
    return [student for student in data if student["N\xfamero"] == studentNumber]

####################################################################
# ii item
####################################################################
def insertItem(itemname):
    for student in data:
        student[itemname]=''

####################################################################
# isg item student_number grade
####################################################################
def insertStudentGrade (studentGrade):

    if len(studentGrade) != 3:
        print "\nERROR: Number of fields must be 3\n"
        return 0
        
    item = studentGrade[0]
    if not (item in data[0].keys()):
        print "\nERROR: Item does not exist\n"
        return 0

    grade = studentGrade[2]
    if not (int(grade) in grader):
        print "\nERROR: Grade is not in the range "+str(min(grader))+" "+str(max(grader))+"\n"
        return 0

    student_number = studentGrade[1]    
    student_list = [ student for student in data if student['N\xfamero'] == student_number ]

    try:
        student = student_list.pop(0)
    except:
        print "\nERROR: Student not found\n"
        return 1

    student[item] = grade
    return 0

####################################################################
# igg item group_member grade
####################################################################
def insertGroupGrade (groupGrade):

    if len(groupGrade) != 3:
        print "\nERROR: Number of fields is not 3\n"
        return 0
        
    item = groupGrade[0]
    group_member = groupGrade[1]
    grade = groupGrade[2]


    if not (item in data[0].keys()):
        print "\nERROR: Item does not exist\n"
        return 0

    if not (int(grade) in grader):
        print "\nERROR: Grade is not in the range "+str(min(grader))+" "+str(max(grader))+"\n"
        return 0

    agrupamento, group = getGroupInfo(group_member)
    
    student_list = [student for student in data if student[agrupamento] == group]

    for student in student_list:
        student[item] = grade

    return 1


####################################################################
# Main
####################################################################
def main () :

    if(len(sys.argv) != 2):
        print 'usage: gradmgr infile'
        sys.exit(1)

    loadDB(sys.argv[1])

    filename = sys.argv[1].split('.').pop(0)

    while 1:
        try:
            cmdline = raw_input("gm> ")
        except:
            continue

        cmdline = cmdline.split()
        cmd = 'NA'
        try:
            cmd = cmdline.pop(0)
        except:
            pass

        if cmd=='ls':
            student = listStudent(cmdline[0])
            if student:
                print student.pop(0)
            
        elif cmd=='isg':
            flag = insertStudentGrade(cmdline)
            if flag == 1:
                print "Student grade inserted successfully\n"
            else:
                print "Could not insert student grade\n"
        elif cmd=='ii':
            insertItem(cmdline[0])
        elif cmd=='igg':
            flag = insertGroupGrade(cmdline)
            if flag == 1:
                print "Group grade inserted successfully\n"
            else:
                print "Could not insert group grade\n"
        elif cmd=='pg':
            printGrades(filename+'_pg.csv', cmdline)
        elif cmd=='quit':
            saveDB(filename+'.csv')
            sys.exit(0)
        else:
            print 'Command not found'
                
if __name__ == "__main__" : main ()

