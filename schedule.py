from google.cloud import datastore
import numpy as np

class Schedule:
    def __init__(self, num_days, num_hours):
        self.schedule = np.full((num_hours, num_days), True)
    
    def addBusyHour(self, row_num, col_num):
        self.schedule[row_num][col_num] = False
    
    def returnSchedule(self):
        return self.schedule

def generateScheduleID(day, start_num, end_num):
    hours = []
    for hour in range(start_num, end_num):
        hour_id = day + "_" + str(hour) + "_" + str(hour+1)
        hours.append(hour_id)
    return hours

if __name__ == "__main__":
    sched = Schedule(5, 12)

    print(generateScheduleID("MON", 0, 24))

