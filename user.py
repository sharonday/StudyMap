from google.cloud import datastore

class User:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verify_password(self, datastore_client):
        self.datastore_client = datastore_client
        user_key = self.datastore_client.key("Login", self.username)
        user = self.datastore_client.get(user_key)
        if not user:
            return None
        if self.password != user["password"]:
            return None
        return user

    def store_user(self, datastore_client):
        self.datastore_client = datastore_client
        user_key = self.datastore_client.key("Login", self.username)
        user = datastore.Entity(key=user_key)
        user["username"] = self.username
        user["password"] = self.password
        self.datastore_client.put(user)
