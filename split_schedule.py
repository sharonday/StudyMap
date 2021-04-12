# from main import get_assignments, get_courses
import numpy as np 
from datetime import datetime

class AssignmentSplitter(object):
    def __init__(self, assignments):
        self.assignments = assignments
        self.split_assignments()

    def split_assignments(self):
        assignments =  np.array([[x['name'], x['course'], x['current_date'], x['due_date'], x['hours'], x['user']] for x in self.assignments])
        #TODO: schedule information
        for assignment in assignments:
            name, course, curr_date, due_date, hours, user = assignment
            


