#!/usr/bin/python
import csv, sys

#define eval items here
#items = ["Lab1","Lab2","Lab3","Lab4","Lab5","Lab6"]
items = []

#define group number of elements range(min,max+1) here
groupr = range(1,4)

#define grade range(min,max+1) here
grader = range(0,21)


#global variables 
data = []
agrupamentos = []

####################################################################
def saveDB(filename):
            keys = ['N\xfamero', 'Nome']+agrupamentos+items
            with open(filename, 'wb') as f:
                writer = csv.DictWriter(f, keys, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
                f.close()

####################################################################
def loadDB(filename):
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
    for agrupamento in agrupamentos:
        if student[agrupamento] != '':
            break
    groupInfo = []
    groupInfo.append(agrupamento)
    groupInfo.append(student[agrupamento])
    return groupInfo


    
####################################################################
# ls student_number
####################################################################
def listStudent(studentNumber):
    return [item for item in data if item["N\xfamero"] == studentNumber]

####################################################################
# ii item
####################################################################
def insertItem(itemname):
    items.append(itemname)

####################################################################
# isg item student_number grade
####################################################################
def insertStudentGrade (studentGrade):

    if len(studentGrade) != 3:
        print "\nERROR: Number of fields must be 3\n"
        return 0
        
    item = studentGrade[0]
    if not (item in items):
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
            b = groupGrade

            if len(b) != 3:
                        print "\nERROR: Number of fields is not 3\n"
                        return 0
        
            if not (b[0] in groups):
                        print "\nERROR: Group does not exist\n"
                        return 0

            if not (b[1] in items):
                        print "\nERROR: Item does not exist\n"
                        return 0

            if not (int(b[2]) in grader):
                        print "\nERROR: Grade is not in the range "+str(min(grader))+" "+str(max(grader))+"\n"
                        return 0

            studentFound = 0;
            for student in data:
                        if student['Group'] == b[0]:
                                    student[b[1]] = b[2]
                                    studentFound = 1

            if studentFound == 0:
                        print "\nERROR: Group empty or non-existing\n"
                        return 0

            return 1


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
        elif cmd=='quit':
            saveDB(filename+'_out.csv')
            sys.exit(0)
        else:
            print 'Command not found'
                
if __name__ == "__main__" : main ()

