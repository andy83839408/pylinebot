import psycopg2
import os

#連資料庫撈--render-postgreSQL
class database:
  def __init__(self,user_name,uid):
    self.user_name = user_name
    self.uid = uid
    self.Internal_Database_URL = os.getenv('Internal_Database_URL')
    print("資料庫連線字串:"+os.getenv('Internal_Database_URL'))
  def add_test(self,key,val):
    conn = psycopg2.connect(self.Internal_Database_URL)
    cur = conn.cursor()
    cur.excute(f"SELECT value,username FROM trishtalk WHERE key='{key}'")
    rows = cur.cur.fetchall()
    if rows ==[]:
      cur.execute(f"INSERT INTO trishtalk (key,value,userid,username) VALUSE('{key},'{val}','{self.uid}','{self.user_name}')")
    else:
      cur.execute(f"UPDATE trishtalk set val = {val} where key='{key}'")

    conn.commit()
    conn.close()
    return True