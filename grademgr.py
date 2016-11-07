import csv, sys

#define eval items here
items = ["Lab1","Lab2","Lab3","Lab4","Lab5","Lab6"]

#define group number of elements range(min,max+1) here
groupr = range(1,4)

#define grade range(min,max+1) here
grader = range(0,21)


#global variables 
data = []
groups = []

####################################################################
def listGroups():
    for group in groups:
        sys.stdout.write(group+' ')
    print '\n'

####################################################################
def listStudent(student):
    try:
        b = student.pop(0)
    except:
        return

    studentFound = 0;
    for student in data:
        if student['Number'] == b:
            print b
            for y in student:
                print y+' : '+student[y]        
            studentFound = 1
            return

    if studentFound == 0:
        print "\nERROR: Student not found\n"
        return 0

####################################################################
def insertStudentGrade (studentGrade):
    b = studentGrade

    if len(b) != 3:
        print "\nERROR: Number of fields must be 3\n"
        return 0
        
    if not (b[1] in items):
        print "\nERROR: Item does not exist\n"
        return 0

    if not (int(b[2]) in grader):
        print "\nERROR: Grade is not in the range "+str(min(grader))+" "+str(max(grader))+"\n"
        return 0

    studentFound = 0;
    for student in data:
        if student['Number'] == b[0]:
            student[b[1]] = b[2]
            studentFound = 1
            return 1

    if studentFound == 0:
        print "\nERROR: Student not found\n"
        return 0

####################################################################
def insertGroupGrade (groupGrade) :
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

####################################################################
def insertGroup (group) :
    b = group

    if not (len(b) in range(3,max(groupr)+2)):
        print "\nERROR: Number of fields must be in range 2 to "+str(max(groupr)+2)+"\n"
        return 0
        
    if b[0] in groups:
        print "\nERROR: Group already exists\n"
        return 0

    groupName = b[0]
    b.pop(0)

    #check all members
    for member in b:
        studentFound = 0
        for student in data:
            if student['Number'] == member:
                if(student['Group'] == 'NA'):
                    studentFound = 1
                    continue
                else:
                    print "\nERROR: Group member "+member+" already belongs in a group"
                    return 0

        if studentFound == 0:
            print "Group member "+member+" not found\n"
            return 0

    #create group and insert all members
    groups.append(groupName)
    for member in b:
        for student in data:
            if student['Number'] == member:
                student['Group'] = groupName
                continue

    return 1

def main () :

    while 1:
        try:
            cmdline = raw_input("gm> ")
        except:
            continue

        cmdline = cmdline.split()
        cmd = 'NA'
        try:
            cmd = cmdline.pop(0);
        except:
            pass

        if cmd=='isg':
            flag = insertStudentGrade(cmdline)
            if flag == 1:
                print "Student grade inserted successfully\n"
            else:
                print "Could not insert student grade\n"
        elif cmd=='ls':
            listStudent(cmdline)
        elif cmd=='lg':
            listGroups()
        elif cmd=='igg':
            flag = insertGroupGrade(cmdline)
            if flag == 1:
                print "Group grade inserted successfully\n"
            else:
                print "Could not insert group grade\n"
        elif cmd=='ig':
            flag = insertGroup(cmdline)
            if flag == 1:
                print "Group inserted successfully\n"
            else:
                print "Could not insert group\n"
        elif cmd=='save':
            keys = ['Number', 'Name', 'Group']
            for item in items:
                keys.append(item)
            with open(cmdline[0], 'wb') as f:
                writer = csv.DictWriter(f, keys, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
                f.close()
        elif cmd=='load':
            with open(cmdline[0],  'r') as f:
                reader = csv.DictReader(f, delimiter=';')
                for line in reader:
                    line['Number'] = line.pop('N\xfamero')
                    line['Name'] = line.pop('Nome')
                    for item in items:
                        if not (item in line):
                            line[item] = 'NA'
                    try:
                        line['Group'] = line['Group']
                    except:
                        line['Group'] = 'NA'

                    data.append(line)
                f.close()
        elif cmd=='quit':
            sys.exit(0)
        else:
            print 'Command not found'
                
if __name__ == "__main__" : main ()
