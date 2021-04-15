# from main import get_assignments, get_courses
import numpy as np 
from datetime import datetime

class AssignmentSplitter(object):
    def __init__(self, assignments):
        self.assignments = assignments
        self.day_dict = dict()
        self.split_assignments()

    def split_assignments(self):
        assignments =  np.array([[x['name'], x['course'], x['current_date'], x['due_date'], x['hours'], x['user']] for x in self.assignments])
        #TODO: schedule information
        for assignment in assignments:
            name, course, curr_date, due_date, hours, user = assignment
            #nano takes day, month, year so have to split from year, month, day
            # x = str(due_date).split("-")
            # full = x[2] + "." + x[1] + "."+ x[0]
            # full+= ' 11:59:59,76'
            # nano = datetime.strptime(full, '%d.%m.%Y %H:%M:%S,%f')
            # print(nano-curr_date.replace(tzinfo=None))
            #determine number of days in between current and due date
            #determine how many off days exist in between current and due date
            #determine how many actual days exist between the current date and due date
            #determiner number of hours per day
            #determine if any days have a greater number of study hours compared to free time
                # raise warning
            #add hours per day to dictionary
            #iterate to next assignment
        #repeat process for each assignment
        #return the dictionary for dates and study hours per day


    # Draft time
    # def getTimeBlocks(self, num_hours, num_days):
    #     num_hours_per_day = ceil(float(num_hours) / float(num_days))
    #     num_hours_per_day = round(x*2)/2
    #     return num_hours_per_day
            


