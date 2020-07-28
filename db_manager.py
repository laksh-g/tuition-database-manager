import gspread
import os
import calendar
import datetime
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


#IMPORTANT fill the following lines with strings of the name of your google sheet
#-------------------------------------------------------------------------------------------------------------------------------------------------
sheets = client.open("<Insert name of google_sheet>").get_worksheet(0)
payments = client.open("<Insert name of google_sheet>").get_worksheet(1)
classes = client.open("<Insert name of google_sheet>").get_worksheet(2)
schedule = client.open("<Insert name of google_sheet>").get_worksheet(3)
#-------------------------------------------------------------------------------------------------------------------------------------------------


sched = schedule.get_all_records()
clss = classes.get_all_records()
data = sheets.get_all_records()
keys = sheets.row_values(1)
IMP_ROWS = 7
FIELDS = keys[0:IMP_ROWS]
AMT_PAID_COL = 9
DATE_COL = 10
NUM_CLASS_COL = 11
STUDENTS = [d["Name"] for d in data]
month_dict = {'Jan': '', 'Feb': '', 'Mar': '', 'Apr': '', 'May': '', 'Jun': '', 'Jul': '', 'Aug': '', 'Sep': '', 'Oct': '', 'Nov': '', 'Dec': '', 'Last Updated': ''}
MONTH_LIST = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']


def addNew(entry):
    newEntry = {}
    for field in range(len(FIELDS)):
        txt = entry[field]
        newEntry[FIELDS[field]] = txt

    newEntry["Fees per class"] = entry[-1]
    newEntry["No. classes remaining"] = 0
    STUDENTS.append(newEntry["Name"])
    sheets.insert_row(list(newEntry.values()), len(sheets.col_values(1))+1)
    sheets.update_cell(len(sheets.col_values(1)), NUM_CLASS_COL,0)
    data.append(newEntry)
    print("data successfully entered")


def findName():
    allDetails = {}
    print("Type quit to go back")
    name = input("Type the name of the ward: ")
    cell = sheets.findall(name)
    if len(cell) == 0:
        allDetails = {}
    else:
        allDetails = data[cell[0].row - 2]
        print("1. show contact details")
        print("2. show fees details")
        choice = input("")

        if choice == "1":
            for field in FIELDS:
                print(field + ": " + str(allDetails[field]))
        elif choice == "2":
            for field in keys[IMP_ROWS:]:
                print(field + ": " + str(allDetails[field]))
        else:
            print("invalid choice")



def checkFees():
    pending = []
    for row in data:
        if row["No. classes remaining"] == 0:
            pending.append(row["Name"])
    return pending


def payment(name, amt):
    allDetails = {}
    if name not in STUDENTS:
        return -1
    elif not str(amt).isdecimal():
        return -2
    else:
        row = STUDENTS.index(name) + 2
        allDetails = data[STUDENTS.index(name)]
        dt = datetime.datetime.today()
        date = dt.date()
        month = dt.month
        classes = float(allDetails["No. classes remaining"]) + float(amt) / float(allDetails["Fees per class"])
        allDetails["Date last paid"] = str(date)
        allDetails["Amount Last Paid"] = str(amt)
        allDetails["No. classes remaining"] = str(classes)
        data[STUDENTS.index(name)] = allDetails
        dates = payments.cell(row, month * 2 - 1).value
        dates = dates + "\n" + str(date)
        amts = payments.cell(row, month * 2).value
        amts = amts + "\n" + str(amt)

        sheets.update_cell(row, AMT_PAID_COL, str(amt))
        sheets.update_cell(row, DATE_COL, str(date))
        sheets.update_cell(row, NUM_CLASS_COL, str(classes))
        payments.update_cell(row, month * 2 - 1, dates)
        payments.update_cell(row, month * 2, amts)
        print("Data successfully updated")
        return 0


def income(strMonth = datetime.datetime.today().strftime("%b")):
    records = payments.get_all_records()
    sum = 0
    for dict in records:
        fees = str(dict[strMonth])
        feesList = fees.splitlines()
        for item in feesList:
            sum += float(item)
    return [strMonth, sum]

def showAllPayments():
    records = payments.get_all_records()

    result = [[] for i in range(len(STUDENTS))]
    count = 0
    for name in STUDENTS:
        result[count] = [name]
        count += 1

    rowNum = 0
    for rowdict in records:
        rowlist = rowdict.values()
        count = 0
        tempStr = ""
        for item in rowlist:
            if count == 0:
                tempStr = str(item)
                count += 1
            else:
                tempStr = tempStr + " - "+str(item)
                count = 0
                temp = result[rowNum]
                temp.append(tempStr)
                result[rowNum] = temp
        rowNum += 1

    return result


def addClass(name, date, option):
    global clss
    idx = STUDENTS.index(name)
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    currMonth = dt.strftime("%b")
    if idx < len(clss):
        class_rec = str(clss[idx][currMonth])
    else:
        class_rec = ""

    num_class = str(data[idx]["No. classes remaining"])
    amt = 1
    new_amt = 0
    add_str = ""
    if option == "Add":
        new_amt = int(num_class)+int(amt)
        add_str = " added " + str(amt)
    elif option == "Remove":
        new_amt = int(num_class) - int(amt)
        add_str = " subtracted " + str(amt)
    else:
        print("invalid")

    data[idx]["No. classes remaining"] = str(new_amt)
    sheets.update_cell(idx+2, 11, str(new_amt))
    classes.update_cell(idx+2, dt.month, class_rec + "\n" + str(dt.date()) + add_str)
    clss = classes.get_all_records()

def update_schedule(d, operation, name):
    #Returns list of updated students for that day
    records = sched[0]
    flag = True
    student_list = None
    os.system('cls')
    day = list(records.keys())[d-1]
    add_rem = operation

    student_list = str(records[day]).splitlines()
    if add_rem == "added":
        student_list.append(name)
    elif add_rem == "removed":
        student_list.remove(name)
    if student_list == []:
        student_string = ""
    else:
        student_string = str(student_list[0])
        for idx in range(1, len(student_list)):
            student_string += "\n" + str(student_list[idx])
    records[day] = student_string
    sched[0] = records
    schedule.update_cell(2, list(records.keys()).index(day)+1, student_string)
    return student_list


def display_class_rec():
    result = [[] for i in range(10)]
    keyList = list(clss[0].keys())
    for dict in clss:
        idx = 0
        month = return_month()
        iter = 0
        while idx < 10:
            month_rec = dict[keyList[month-1]]
            month_list = str(month_rec).splitlines()
            for element in reversed(month_list):
                if idx < 10:
                    result[idx].append(element)
                    idx += 1
            month -= 1
            iter += 1
            if month == 0:
                month = 12
            if iter > 6:
                while idx < 10:
                    result[idx].append("")
                    idx += 1
                iter = 0
    return result



def last_updated():
    dt = datetime.date.today()
    d = clss[0]["Last Updated"]
    remaining_to_update = []
    classes_to_update = {}
    global month_dict
    currd = dt.isoformat() # USE .today() instead of .isoformat()
    if d == "" or d is None:
        d = currd
    if currd != d:
        print("Updating records please wait")
        delta = datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime(d, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(currd, '%Y-%m-%d')

        while start_date < end_date:
            start_date += delta
            weekd = calendar.day_name[start_date.weekday()]
            std_list = str(sched[0][weekd]).splitlines()
            for std in std_list:
                while STUDENTS.index(std) > len(clss)-1:
                    clss.append(month_dict.copy())
                if clss[STUDENTS.index(std)][start_date.strftime("%b")] == "":
                    clss[STUDENTS.index(std)][start_date.strftime("%b")] = str(start_date.date())
                else:
                    clss[STUDENTS.index(std)][start_date.strftime("%b")] += "\n" + str(start_date.date())
                classes_to_update[(STUDENTS.index(std)+2, start_date.month)] = clss[STUDENTS.index(std)][start_date.strftime("%b")]
                data[STUDENTS.index(std)]["No. classes remaining"] -= 1
                if std not in remaining_to_update:
                    remaining_to_update.append(std)

        d = currd
    clss[0]["Last Updated"] = d
    classes.update_cell(2,13,str(d))
    for name in remaining_to_update:
        sheets.update_cell(STUDENTS.index(name)+2, 11, data[STUDENTS.index(name)]["No. classes remaining"])

    for row, col in classes_to_update.keys():
        classes.update_cell(row, col, classes_to_update[(row, col)])



def return_month():
    dt = datetime.datetime.today()
    date = dt.date()
    month = dt.month
    return month

