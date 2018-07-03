from pymongo import MongoClient


class MongoDB:
    
    def __init__(self,host,port,db):
        self.client = MongoClient(host,port)
        self.db = self.client[db]
        
    
    def check_user(self,user,password):
        try:
            res = self.db.users.find_one({"username":str(user),"password":str(password)})
            return res
        except Exception as e:
            print(e)
            
    
    def get_users(self):
        try:
            res = self.db.users.find({})
            return res
        except Exception as e:
            print(e)
        