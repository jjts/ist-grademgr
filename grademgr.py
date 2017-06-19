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
def printStudentGrades(filename, items):
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
def printGroupGrades(filename,itemList):
    if not set(itemList).issubset(data[0].keys()):
        print 'Item(s) not in key list'
        return
    
    groups = []
    for student in data:
        group = getGroupInfo(student["N\xfamero"])
        if not group:
            continue
        for item in itemList:
            group.append(student[item])
        if not(group in groups):
            groups.append(group)

    groups.sort()

    #create file header
    header = "Agrupamento, Grupo, "
    if len(itemList)>0:
        for i in range(0,len(itemList)-1):
            header=header+itemList[i]+', '
        header=header+itemList[len(itemList)-1]
        
    with open(filename, 'wb') as f:
        f.write(header+'\n')
        for group in groups:
            for i in range(0,len(group)-1):
                f.write(group[i]+', ')
            f.write(group[len(group)-1]+'\n')
        f.close()

####################################################################
def saveDB(filename):
    with open(filename+'_filled.csv', 'wb') as f:
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
    agrupamentos.sort()

####################################################################
def getGroupInfo(studentNumber):
    student = listStudent(studentNumber).pop(0)
    groupInfo = []
    for agrupamento in agrupamentos:
        try:
            grpid= int(student[agrupamento])
            groupInfo.append(agrupamento)
            groupInfo.append(student[agrupamento])
        except:
            pass

    return groupInfo


####################################################################
# ls student_number
####################################################################
def listStudent(studentNumber):
    return [student for student in data if student["N\xfamero"] == studentNumber]

####################################################################
# ii item
####################################################################
def insertItems(itemList):
    for student in data:
        for item in itemList:
            if not (item in student.keys()):
                student[item]=''

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

def insertGroupGrade2 (groupGrade):

    if len(groupGrade) != 3:
        print "\nERROR: Number of fields is not 3\n"
        return 0
        
    item = groupGrade[0]
    group_number = groupGrade[1]
    grade = groupGrade[2]


    if not (item in data[0].keys()):
        print "\nERROR: Item does not exist\n"
        return 0

    student_list = [student for student in data if student[agrupamentos[0]] == group_number]

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
        except EOFError:
            print ''
            break

        cmdline = cmdline.split()
        cmd = 'NA'
        try:
            cmd = cmdline.pop(0)
        except:
            pass

        if (cmd[0]=='#' or cmd=='NA'):
            pass
        elif cmd=='ls':
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
            insertItems(cmdline)
        elif cmd=='igg':
            flag = insertGroupGrade(cmdline)
            if flag == 1:
                print "Group grade inserted successfully\n"
            else:
                print "Could not insert group grade\n"
        elif cmd=='igg2':
            flag = insertGroupGrade2(cmdline)
            if flag == 1:
                print "Group grade inserted successfully\n"
            else:
                print "Could not insert group grade\n"
        elif cmd=='psg':
            printStudentGrades(filename+'_sg.csv', cmdline)
        elif cmd=='pgg':
            printGroupGrades(filename+'_gg.csv', cmdline)
        elif cmd=='quit':
            saveDB(filename)
            sys.exit(0)
        else:
            print 'Command not found'
                
if __name__ == "__main__" : main ()

