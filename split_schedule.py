# from main import get_assignments, get_courses
import numpy as np 
from datetime import datetime, date, timedelta
import pandas as pd

class AssignmentSplitter(object):
    def __init__(self, assignments, off_days, free_hours):
        self.assignments = assignments
        self.day_dict = dict()
        self.off_days = off_days

        if self.off_days['mon'] == True:
            print("OFF MONDAY")
        if self.off_days['tues'] == True:
            print("OFF TUESDAY")
        if self.off_days['wed'] == True:
            print("OFF WEDNESDAY")
        if self.off_days['thurs'] == True:
            print("OFF THURS")
        if self.off_days['fri'] == True:
            print("OFF FRIDAY")
        if self.off_days['sat'] == True:
            print("OFF SAT")
        if self.off_days['sun'] == True:
            print("OFF SUN")

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
            #determine any off days
            #between_days = self.remove_off_days(between_days)

    def get_between_days(self, start_date, delta_days):
        between_days = []
        for i in range(delta_days.days + 1):
            between_day = start_date + timedelta(days=i)
            between_days.append(between_day)
        return between_days
    
    def remove_off_days(self, dates):
        day_enum = {'Monday': 'mon',
                    'Tuesday': 'tues',
                    'Wednesday': 'wed',
                    'Thursday': 'thurs',
                    'Friday': 'fri',
                    'Saturday': 'sat',
                    'Sunday': 'sun'}
        for date in dates:
            day = date.strftime("%A")
            if self.off_days[day_enum[day]] == True:
                print(day + " OFF DAY")
        

    # Draft time
    # def getTimeBlocks(self, num_hours, num_days):
    #     num_hours_per_day = ceil(float(num_hours) / float(num_days))
    #     num_hours_per_day = round(x*2)/2
    #     return num_hours_per_day
            


