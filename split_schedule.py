# from main import get_assignments, get_courses
import numpy as np 
from datetime import datetime, date, timedelta
import pandas as pd
from pytz import timezone
import math
from flask import Flask, flash

eastern = timezone('US/Eastern')
threshold = 0.8 #80% threshold
scale = 2 #30 min scale

class AssignmentSplitter(object):
    def __init__(self, assignments, off_days, free_hours):
        self.assignments = assignments
        self.day_dict = dict() #key: date value: number hours allocated
        self.off_days = self.get_off_days(off_days)
        self.free_hours = self.get_free_hours(free_hours)
    
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

    def get_free_hours(self, free_hours):
        num_free_hours = [0 for i in range(7)] #assume no hours free in day
        for d in free_hours:
            if d["day"] == "SUN":
                num_free_hours[0] = len(d["hours"])                
            if d["day"] == "MON":
                num_free_hours[1] = len(d["hours"])
            if d["day"] == "TUE":
                num_free_hours[2] = len(d["hours"])
            if d["day"] == "WED":
                num_free_hours[3] = len(d["hours"])
            if d["day"] == "THU":
                num_free_hours[4] = len(d["hours"])
            if d["day"] == "FRI":
                num_free_hours[5] = len(d["hours"])
            if d["day"] == "SAT":
                num_free_hours[6] = len(d["hours"])
        return num_free_hours
    
    def split_assignments(self):
        assignments =  np.array([[x['name'], x['course'], x['current_date'], x['due_date'], x['hours'], x['user']] for x in self.assignments])
        for assignment in assignments:
            name, course, curr_date, due_date, hours, user = assignment
            curr_date = curr_date.astimezone(eastern)
            x = str(due_date).split("-")
            full = x[2] + "." + x[1] + "."+ x[0]
            full+= ' 11:0:0,0'
            due_date = datetime.strptime(full, '%d.%m.%Y %H:%M:%S,%f')
            num_days = due_date.replace(tzinfo=None)-curr_date.replace(tzinfo=None)
            between_days = self.get_between_days(curr_date, num_days)
            between_days = self.remove_off_days(between_days)
            blocks_per_day = self.get_time_per_day(between_days, hours)            
            self.split_blocks_per_day(between_days, blocks_per_day, float(hours), [name, course])
        return self.day_dict
    
    def get_curr_assign_sum(self, assign_list):
        total_sum = 0
        for assign in assign_list:
            num_hours = assign[0]
            total_sum += num_hours
        return total_sum        
    
    def split_blocks_per_day(self, between_days, blocks_per_day, hours, assignment_info):
        total_hours = 0
        for date in between_days:
            #divide by two for number of hours
            num_hours = float(blocks_per_day) / scale
            if date.date() in self.day_dict:
                #get current number of allocated hours
                current_hours = self.get_curr_assign_sum(self.day_dict[date.date()])
                #determine max hours for that day
                max_hours = self.get_available_hours(date)
                #check to see that current hours and new hours don't exceed threshold hours
                if current_hours + num_hours < max_hours:
                    #append to dictionary
                    self.day_dict[date.date()].append((num_hours, assignment_info))
                    #add current hours to running sum
                    total_hours += num_hours
                    if total_hours >= hours:
                        break
                else:
                    #overscheduled for day
                    flash('Error: overscheduled for day')
                    continue

            else:
                #insert into dictionary
                self.day_dict[date.date()] = [(num_hours, assignment_info)]
                #add current hours to running sum
                total_hours += num_hours
                #determine if we've reached the allocated hours
                if total_hours >= hours:
                    break
    
    def get_between_days(self, start_date, delta_days):
        between_days = []
        for i in range(1, delta_days.days+1):
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
    
    def get_curr_hours(self, dates):
        total_curr_hours = 0
        temp_dates = dates.copy()
        for date in temp_dates:
            if date in self.day_dict:
                curr_num_hours = self.day_dict[date]
                default_free_hours = self.get_available_hours(date) #add one for including final date
                hours_left = default_free_hours - curr_num_hours
                total_curr_hours += hours_left
            else:
                default_free_hours = self.get_available_hours(date)
                total_curr_hours += default_free_hours
        return total_curr_hours

    def get_time_per_day(self, between_days, hours):
        hours_available = self.get_curr_hours(between_days)
        if float(hours) < hours_available:
            #multiply by scale 
            num_hours = float(hours) * scale #change factor based on discretization
            #divide by number of days (round up)
            num_blocks_per_day = math.ceil(num_hours/len(between_days))
        #no hours left to work
        else:
            flash('Error: overscheduled')
        return num_blocks_per_day

    def get_available_hours(self, date):
        day_enum = {"Sunday": 0,
                    "Monday": 1,
                    "Tuesday": 2,
                    "Wednesday": 3,
                    "Thursday": 4,
                    "Friday": 5,
                    "Saturday": 6}
        day = date.strftime("%A")
        day_index = day_enum[day]
        num_free_hours = self.free_hours[day_index]
        return num_free_hours