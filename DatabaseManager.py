import sqlite3


class sqliteData():
    def __init__(self):
        pass

    def Connect(self):
        connection = sqlite3.connect("quizApp.db")
        cursor = connection.cursor()
        list = [connection,cursor]
        return list

    
    def UsersAdd(self,username,passwd,e_mail,name_lastname,point=0,role="user"):
        conn = self.Connect()
        conn[1].execute(f"INSERT INTO users (username,passwd,e_mail,name_lastname,point,role) VALUES (?,?,?,?,?,?)",
                       (username, passwd,e_mail,name_lastname, point,role))
        conn[0].commit()
        conn[0].close()
        print("işlem Tamamlandı.")

    def QuestionAdd(self,question,a,b,c,d,answer,point):
        conn = self.Connect()
        conn[1].execute(f"INSERT INTO questions (question,a,b,c,d,answer,point) VALUES (?,?,?,?,?,?,?)",
                       (question, a, b, c,d,answer,point))
        conn[0].commit()
        conn[0].close()
        print("işlem Tamamlandı.")

    def getData(self,tblname,id=None,username=None,all=True,):
        if all == True:
            conn = self.Connect()
            conn[1].execute(f"Select * from {tblname}")
            data = conn[1].fetchall()
            conn[0].close()
            return data
        else :
            if id == None:
                conn = self.Connect()
                conn[1].execute(f"Select * from {tblname} where username='{username}'")
                data = conn[1].fetchone()
                conn[0].close()
                return data
            else :
                conn = self.Connect()
                conn[1].execute(f"Select * from {tblname} where id={id}")
                data = conn[1].fetchone()
                conn[0].close()
                return data

    def pointUpdate(self,id,point):
        conn = self.Connect()
        conn[1].execute(f"Update users Set point=point+{point} where username='{id}'")
        conn[0].commit()
        conn[0].close()
        print("işlem Tamamlandı.")
