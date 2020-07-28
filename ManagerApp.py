from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.picker import MDDatePicker
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.toast import toast
import db_manager


LAST_NAME = ""
RESULT = 0

class MainWindow(Screen):
    pass


class NewStudentWindow(Screen):
    namee = ObjectProperty(None)
    age = ObjectProperty(None)
    school = ObjectProperty(None)
    address = ObjectProperty(None)
    parent_name = ObjectProperty(None)
    parent_email = ObjectProperty(None)
    contact = ObjectProperty(None)
    fees = ObjectProperty(None)
    sub_but = ObjectProperty(None)

    def submit(self):
        entry = [self.namee.text, self.age.text, self.school.text, self.address.text, self.parent_name.text, self.parent_email.text, self.contact.text, self.fees.text]
        db_manager.addNew(entry)
        self.namee.text = ""
        self.age.text = ""
        self.school.text = ""
        self.address.text = ""
        self.parent_name.text = ""
        self.parent_email.text = ""
        self.contact.text = ""
        self.fees.text = ""


class ShowAllWindow(Screen):
    data = db_manager.data
    def __init__(self, **kwargs):
        super(ShowAllWindow, self).__init__(**kwargs)


class SingleStudentDetails(Screen):
    details = db_manager.data
    students = db_manager.STUDENTS
    def __init__(self, **kwargs):
        super(SingleStudentDetails, self).__init__(**kwargs)
        

    def trigger(self):
        self.namee.text = str(LAST_NAME)
        std_dict = self.details[self.students.index(LAST_NAME)]
        self.age.text = str(std_dict["Age"])
        self.school.text = str(std_dict["School"])
        self.address.text = str(std_dict["Address"])
        self.parent_name.text = str(std_dict["Parents Name"])
        self.parent_email.text = str(std_dict["Parents Email"])
        self.contact.text = str(std_dict["Contact No."])
        self.fees.text = str(std_dict["Fees per class"])
    

class SingleStudentDetailsP2(Screen):
    details = db_manager.data
    students = db_manager.STUDENTS
    list_dict = {}
    def __init__(self, **kwargs):
        super(SingleStudentDetailsP2, self).__init__(**kwargs)


    def trigger(self):
        self.namee.text = str(LAST_NAME)
        std_dict = self.details[self.students.index(LAST_NAME)]
        self.fees.text = str(std_dict["Fees per class"])
        self.amt.text = str(std_dict["Amount Last Paid"])
        self.date.text = str(std_dict["Date last paid"])
        self.classes.text = str(std_dict["No. classes remaining"])
        self.suh()
        

    def suh(self):
        global LAST_NAME
        records = db_manager.payments.get_all_records()
        month = db_manager.return_month()
        count = 6 #Last how many months
        self.ids.container.clear_widgets()
        if len(records) < self.students.index(LAST_NAME):
            list_item = OneLineListItem(text="No records found")
            self.ids.container.add_widget(list_item)
        else:
            while count > 0:
                month_dates, month_amt = list(records[self.students.index(LAST_NAME)].values())[2 * month - 2:2 * month]
                date_list = str(month_dates).splitlines()
                amt_list = str(month_amt).splitlines()
                for i in range(len(date_list)-1, -1, -1):
                    fin_str = "Paid Rs." + amt_list[i] + " on " + date_list[i]
                    list_item = OneLineListItem(text=fin_str)
                    self.ids.container.add_widget(list_item)
                count -= 1
                month -= 1
                if month == 0:
                    month = 12


class SingleStudentDetailsP3(Screen):
    details = db_manager.data
    students = db_manager.STUDENTS
    schedule = db_manager.sched[0]
    month_keys = list(db_manager.clss[0].keys())
    list_dict = {}
    def __init__(self, **kwargs):
        super(SingleStudentDetailsP3, self).__init__(**kwargs)


    def trigger(self):
        self.namee.text = str(LAST_NAME)
        std_dict = self.details[self.students.index(LAST_NAME)]
        self.amt.text = str(std_dict["Amount Last Paid"])
        self.date.text = str(std_dict["Date last paid"])
        self.classes.text = str(std_dict["No. classes remaining"])
        days = ""
        for day in self.schedule.keys():
            day_list = str(self.schedule[day]).splitlines()
            for name in day_list:
                if name == LAST_NAME:
                    if days == "":
                        days = str(day)
                    else:
                        days = days + ", " + str(day)
        self.days.text = days
        self.suh()


    def suh(self):
        records = db_manager.clss
        month = db_manager.return_month()
        count = 6 #Last how many months
        self.ids.container.clear_widgets()
        if len(records) < self.students.index(LAST_NAME):
            list_item = OneLineListItem(text="No records found")
            self.ids.container.add_widget(list_item)
        else:
            while count > 0:
                month_dates = records[self.students.index(LAST_NAME)][self.month_keys[month-1]]
                date_list = str(month_dates).splitlines()
                for i in range(len(date_list)-1, -1, -1):
                    fin_str = "Class held on " + date_list[i]
                    list_item = OneLineListItem(text=fin_str)
                    self.ids.container.add_widget(list_item)
                count -= 1
                month -= 1
                if month == 0:
                    month = 12

class FeesManagementWindow(Screen):
    pass


class PendingFees(Screen):

    def suh(self):
        self.ids.container.clear_widgets()
        pending_list = db_manager.checkFees()
        pending_list.sort()
        for name in pending_list:
            list_item = OneLineListItem(text=str(name))
            self.ids.container.add_widget(list_item)


class RegisterPayment(Screen):
    namee = ObjectProperty(None)
    amt = ObjectProperty(None)
    sub_but = ObjectProperty(None)
    students = db_manager.STUDENTS.copy()
    students.sort()
    def select_name(self):
        bottom_sheet_menu = MDListBottomSheet()
        for name in self.students:
            bottom_sheet_menu.add_item(
                f"{name}",
                lambda x, y=name: self.callback_for_menu_items(
                    f"{y}"
                ),
            )
        bottom_sheet_menu.open()

    def callback_for_menu_items(self, *args):
        toast("Selected "+str(args[0]))
        self.namee.text = args[0]

    def submit(self):
        global RESULT
        std = self.namee.text
        fees = self.amt.text
        result = db_manager.payment(std, fees)
        RESULT = result
        self.namee.text = "Select name"
        self.amt.text = ""
        return result


class TotalIncome(Screen):
    month = ObjectProperty(None)
    amount = ObjectProperty(None)

    def suh(self):
        strMonth, money = db_manager.income()
        self.month.text = str(strMonth) + " is"
        self.amount.text = str(money)

    def callback_for_menu_items(self, *args):
        toast("Selected "+str(args[0]))
        strMonth, money = db_manager.income(args[0])
        self.month.text = str(strMonth) + " is"
        self.amount.text = str(money)


    def change_month(self):
        bottom_sheet_menu = MDListBottomSheet()
        for name in db_manager.MONTH_LIST:
            bottom_sheet_menu.add_item(
                f"{name}",
                lambda x, y=name: self.callback_for_menu_items(
                    f"{y}"
                ),
            )
        bottom_sheet_menu.open()

class PaymentRecords(Screen):
    pass

class ClassManagement(Screen):
    pass


class Scheduler(Screen):
    students = db_manager.STUDENTS
    sched = db_manager.sched
    selected_kid=None
    selected_day=None
    list_dict={}
    mon_list=[]
    tue_list=[]
    wed_list=[]
    thu_list=[]
    fri_list=[]
    sat_list=[]
    sun_list=[]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.inside = GridLayout()
        self.inside.cols = 1

    def trigger(self):
        self.ids.Monday.clear_widgets()
        self.ids.Tuesday.clear_widgets()
        self.ids.Wednesday.clear_widgets()
        self.ids.Thursday.clear_widgets()
        self.ids.Friday.clear_widgets()
        self.ids.Saturday.clear_widgets()
        self.ids.Sunday.clear_widgets()
        mon_stds = self.sched[0]["Monday"]
        self.mon_list = str(mon_stds).splitlines()
        self.mon_list.sort()
        for name in self.mon_list:
            list_item = OneLineListItem(text=name)
            self.ids.Monday.add_widget(list_item)

        tue_stds = self.sched[0]["Tuesday"]
        self.tue_list = str(tue_stds).splitlines()
        self.tue_list.sort()
        for name in self.tue_list:
            list_item = OneLineListItem(text=name)
            self.ids.Tuesday.add_widget(list_item)

        wed_stds = self.sched[0]["Wednesday"]
        self.wed_list = str(wed_stds).splitlines()
        self.wed_list.sort()
        for name in self.wed_list:
            list_item = OneLineListItem(text=name)
            self.ids.Wednesday.add_widget(list_item)

        thu_stds = self.sched[0]["Thursday"]
        self.thu_list = str(thu_stds).splitlines()
        self.thu_list.sort()
        for name in self.thu_list:
            list_item = OneLineListItem(text=name)
            self.ids.Thursday.add_widget(list_item)

        fri_stds = self.sched[0]["Friday"]
        self.fri_list = str(fri_stds).splitlines()
        self.fri_list.sort()
        for name in self.fri_list:
            list_item = OneLineListItem(text=name)
            self.ids.Friday.add_widget(list_item)

        sat_stds = self.sched[0]["Saturday"]
        self.sat_list = str(sat_stds).splitlines()
        self.sat_list.sort()
        for name in self.sat_list:
            list_item = OneLineListItem(text=name)
            self.ids.Saturday.add_widget(list_item)

        sun_stds = self.sched[0]["Sunday"]
        self.sun_list = str(sun_stds).splitlines()
        self.sun_list.sort()
        for name in self.sun_list:
            list_item = OneLineListItem(text=name)
            self.ids.Sunday.add_widget(list_item)

    def add(self, day):
        print(day)

    def callback_for_menu_items(self, *args):
        self.selected_kid=args[0]
        self.dialog_done()
        #self.dialog = MDDialog(
        #    title="Add/Remove " + str(args[1])+"?",
        #    #text_color=[0,0,0,1],
        #    buttons=[
        #        MDFlatButton(
        #            text="CANCEL", text_color=[1,0,0,1],
        #            on_release=self.dialog_close
        #        ),
        #        MDFlatButton(
        #            text="PROCEED", text_color=[1,0,0,1],
        #            on_release=self.dialog_done
        #        ),
        #    ],
        #)
        #self.dialog.open()


    def dialog_done(self, *args):
        self.update_sched()
        toast(self.selected_kid)

    def update_sched(self):
        operation, name = str(self.selected_kid).split(" ", 1)
        std_list = db_manager.update_schedule(self.selected_day, operation, name)
        cont = None
        if self.selected_day == 1:
            cont = self.ids.Monday
            self.mon_list = std_list
        elif self.selected_day == 2:
            cont = self.ids.Tuesday
            self.tue_list = std_list
        elif self.selected_day == 3:
            cont = self.ids.Wednesday
            self.wed_list = std_list
        elif self.selected_day == 4:
            cont = self.ids.Thursday
            self.thu_list = std_list
        elif self.selected_day == 5:
            cont = self.ids.Friday
            self.fri_list = std_list
        elif self.selected_day == 6:
            cont = self.ids.Saturday
            self.sat_list = std_list
        else:
            cont = self.ids.Sunday
            self.sun_list = std_list

        cont.clear_widgets()
        for name in std_list:
            list_item = OneLineListItem(text=name)
            cont.add_widget(list_item)


    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def show_bottom_sheet(self, day, operation):
        bottom_sheet_menu = MDListBottomSheet()
        stdList = self.students.copy()
        stdList.sort()
        day_list=[]
        self.selected_day=day
        if day == 1:
            day_list = self.mon_list
        elif day == 2:
            day_list = self.tue_list
        elif day == 3:
            day_list = self.wed_list
        elif day == 4:
            day_list = self.thu_list
        elif day == 5:
            day_list = self.fri_list
        elif day == 6:
            day_list = self.sat_list
        else:
            day_list = self.sun_list

        if operation == 1:
            for name in stdList:
                if name not in day_list:
                    bottom_sheet_menu.add_item(
                        f"{name}",
                        lambda x, y=name: self.callback_for_menu_items(
                            f"added {y}",
                            y
                        ),
                    )
        else:
            for name in day_list:
                bottom_sheet_menu.add_item(
                    f"{name}",
                    lambda x, y=name: self.callback_for_menu_items(
                        f"removed {y}",
                        y
                    ),
                )
        bottom_sheet_menu.open()


class RegisterClass(Screen):
    namee = ObjectProperty(None)
    selected_day = ObjectProperty(None)
    selected_operation = ObjectProperty(None)
    sub_but = ObjectProperty(None)
    students = db_manager.STUDENTS.copy()
    students.sort()
    operations = ["Add", "Remove"]

    def select_name(self):
        bottom_sheet_menu = MDListBottomSheet()
        for name in self.students:
            bottom_sheet_menu.add_item(
                f"{name}",
                lambda x, y=name: self.callback_for_menu_items(
                    f"{y}"
                ),
            )
        bottom_sheet_menu.open()

    def select_operation(self):
        bottom_sheet_menu = MDListBottomSheet()
        for name in self.operations:
            bottom_sheet_menu.add_item(
                f"{name}",
                lambda x, y=name: self.callback_for_menu_operation(
                    f"{y}"
                ),
            )
        bottom_sheet_menu.open()

    def callback_for_menu_items(self, *args):
        toast("Selected "+str(args[0]))
        self.namee.text = args[0]

    def callback_for_menu_operation(self, *args):
        toast("Selected "+str(args[0]))
        self.selected_operation.text = args[0]

    def get_date(self, date):
        '''
        :type date: <class 'datetime.date'>
        '''
        self.selected_day.text = str(date)

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    def submit(self):
        if self.namee.text == "Select name" or self.selected_day.text == "Select Date" or self.selected_operation.text == "Select Operation":
            self.dialog = MDDialog(
                title="Invalid selection",
            )
            self.dialog.open()
        else:
            db_manager.addClass(self.namee.text, self.selected_day.text, self.selected_operation.text)
            self.namee.text = "Select name"
            self.selected_day.text = "Select Date"
            self.selected_operation.text = "Select Operation"



class ClassRecords(Screen):
    students = db_manager.STUDENTS

    def open_class_details(self):
        data = db_manager.display_class_rec()
        self.class_details = MDDataTable(
            size_hint=(1, 0.7),
            use_pagination=True,
            column_data=[(name, dp(30)) for name in self.students],
            row_data=data,
        )
        self.class_details.open()


class WindowManager(ScreenManager):
    pass









sm = WindowManager()

class MyMainApp(MDApp):
    students = db_manager.STUDENTS
    data = db_manager.data
    payments = db_manager.showAllPayments()
    names = None

    def build(self):
        db_manager.last_updated()
        self.fees = MDDataTable(
            size_hint=(1, 0.7),
            use_pagination=True,
            column_data=[
                ("Name", dp(30)),
                ("January", dp(30)),
                ("February", dp(30)),
                ("March", dp(30)),
                ("April", dp(30)),
                ("May", dp(30)),
                ("June", dp(30)),
                ("July", dp(30)),
                ("August", dp(30)),
                ("September", dp(30)),
                ("October", dp(30)),
                ("November", dp(30)),
                ("December", dp(30)),
            ],
            row_data=self.payments,
        )

        self.invalid_name = MDDialog(
            text="Invalid Name",
        )

        self.invalid_amount = MDDialog(
            text="Invalid Amount",
        )

        self.all_details = MDDataTable(
            size_hint=(1, 0.7),
            rows_num=len(self.students),
            column_data=[
                ("Name", dp(30)),
                ("Age", dp(30)),
                ("School", dp(30)),
                ("Address", dp(30)),
                ("Parent's Name", dp(30)),
                ("Paren's Email", dp(30)),
                ("Contact No.", dp(30)),
                ("Fees/Class", dp(30)),
                ("Amt Last Paid", dp(30)),
                ("Date Last Paid", dp(30)),
                ("No. Classes Remaining", dp(30)),
            ],
            row_data=[list(row.values()) for row in self.data
                      ],
        )
        self.all_details.bind(on_row_press=self.on_row_press)
        kv = Builder.load_file("AIM.kv")
        self.root_widget = kv
        return self.root_widget

    def open_table(self):
        self.all_details.open()

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        global LAST_NAME
        val = instance_row.index / 11
        name = self.students[int(val)]
        self.all_details.dismiss()
        self.root.current = "single_student"
        LAST_NAME = name

    def open_dialogue(self):
        if RESULT == -1:
            self.invalid_name.open()
        elif RESULT == -2:
            self.invalid_amount.open()
        return RESULT

    def open_payment_details(self):
        self.fees.open()


if __name__ == "__main__":
    MyMainApp().run()
