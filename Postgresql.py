import psycopg2
import os

#連資料庫撈--render-postgreSQL
class database:
  def __init__(self,user_name,uid):
    self.user_name = user_name
    self.uid = uid
    self.Internal_Database_URL = os.getenv('Internal_Database_URL')
    #print("資料庫連線字串:"+os.getenv('Internal_Database_URL'))
  def add_test(self,key,val):
    conn = psycopg2.connect(self.Internal_Database_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT value,username FROM trishtalk WHERE key='{key}'")
    rows = cur.fetchall()
    print("資料庫連線進")
    if rows ==[]:
      print("資料庫連線進IF")
      cur.execute(f"INSERT INTO trishtalk (key,value,userid,username) VALUES('{key}','{val}','{self.uid}','{self.user_name}')")
    else:
      print("資料庫連線進ELSE")
      cur.execute(f"UPDATE trishtalk set val = {val} where key='{key}'")

    conn.commit()
    cur.close()
    conn.close()
    return True
  
  def show(self,key):
    conn = psycopg2.connect(self.Internal_Database_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT value FROM trishtalk WHERE key='{key}'")
    rows = cur.fetchall()
    res=""
    if rows!=0:
      res = f"{rows[0][0]}"
    conn.commit()
    cur.close()
    conn.close()
    return res