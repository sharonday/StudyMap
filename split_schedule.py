# from main import get_assignments, get_courses
import numpy as np 
from datetime import datetime, date, timedelta
import pandas as pd

class AssignmentSplitter(object):
    def __init__(self, assignments, off_days, free_hours):
        self.assignments = assignments
        self.day_dict = dict()
        self.off_days = self.get_off_days(off_days)
    
    def get_off_days(self, off_days):
        bool_off_days = [False for i in range(7)] #one boolean for each day of week
        for d in off_days:
            # i would store d['mon'], etc to variables if you need to use it later
            if d['sun'] == True:
                bool_off_days[0] = True
            if d['mon'] == True:
                bool_off_days[1] = True
            if d['tue'] == True:
                bool_off_days[2] = True
            if d['wed'] == True:
                bool_off_days[3] = True
            if d['thu'] == True:
                bool_off_days[4] = True
            if d['fri'] == True:
                bool_off_days[5] = True
            if d['sat'] == True:
                bool_off_days[6] = True
        return bool_off_days

    def split_assignments(self):
        assignments =  np.array([[x['name'], x['course'], x['current_date'], x['due_date'], x['hours'], x['user']] for x in self.assignments])
        for assignment in assignments:
            name, course, curr_date, due_date, hours, user = assignment
            #convert due date to NanoDateTime
            #nano takes day, month, year so have to split from year, month, day
            x = str(due_date).split("-")
            full = x[2] + "." + x[1] + "."+ x[0]
            full+= ' 11:59:59,76'
            nano = datetime.strptime(full, '%d.%m.%Y %H:%M:%S,%f')
            #determine number of days in between current and due date
            num_days = nano.replace(tzinfo=None)-curr_date.replace(tzinfo=None)
            #determine dates in between current and due date
            between_days = self.get_between_days(curr_date, num_days)
            #determine any off days and remove from the list of dates
            between_days = self.remove_off_days(between_days)
            #split the assignments (return a dictionary that maps (date) --> (hours))
            self.get_time_per_day(between_days)

    def get_between_days(self, start_date, delta_days):
        between_days = []
        for i in range(delta_days.days + 1):
            between_day = start_date + timedelta(days=i)
            between_days.append(between_day)
        return between_days

    def remove_off_days(self, dates):
        temp_dates = dates.copy()
        day_enum = {"Sunday": 0,
                    "Monday": 1,
                    "Tuesday": 2,
                    "Wednesday": 3,
                    "Thursday": 4,
                    "Friday": 5,
                    "Saturday": 6}
        for date in temp_dates:
            day = date.strftime("%A")
            day_index = day_enum[day]
            if self.off_days[day_index] == True:
                temp_dates.remove(date)
        return temp_dates
    
    def get_between_days(self, between_days):
        print("HERE")

    # Draft time
    # def getTimeBlocks(self, num_hours, num_days):
    #     num_hours_per_day = ceil(float(num_hours) / float(num_days))
    #     num_hours_per_day = round(x*2)/2
    #     return num_hours_per_day
            


