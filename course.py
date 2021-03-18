from google.cloud import datastore

class Course:
    
    def __init__(self, name, color, user):
        self.name = name
        self.color = color
        self.user = user

    def store_course(self, datastore_client):
        self.datastore_client = datastore_client
        course_key = self.datastore_client.key("Course", self.name)
        course = datastore.Entity(key=course_key)
        course["name"] = self.name
        course["color"] = self.color
        course["user"] = self.user
        self.datastore_client.put(course)


class Assignment:
    
    def __init__(self, name, date, course, hours, user):
        self.name = name
        self.date = date
        self.course = course
        self.hours = hours
        self.user = user

    def store_assignment(self, datastore_client):
        self.datastore_client = datastore_client
        assign_key = self.datastore_client.key("Assign", self.name)
        assign = datastore.Entity(key=assign_key)
        assign["name"] = self.name
        assign["date"] = self.date
        assign["course"] = self.course
        assign["hours"] = self.hours
        assign["user"] = self.user
        self.datastore_client.put(assign)