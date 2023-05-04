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
    if rows ==[]:
      print("資料庫連線進INSERT")
      cur.execute(f"INSERT INTO trishtalk (key,value,userid,username) VALUES('{key}','{val}','{self.uid}','{self.user_name}')")
    else:
      print("資料庫連線進UPDATE")
      cur.execute(f"UPDATE trishtalk set value = '{val}' where key='{key}'")

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
  
  def getAll(self):
    conn = psycopg2.connect(self.Internal_Database_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT key,value FROM trishtalk")
    rows = cur.fetchall()
    res=dict()
    if rows!=0:
      for row in rows:
        res.update({row[0]:row[1]})
    conn.commit()
    cur.close()
    conn.close()
    return res
  
  #分錢的fun從這開始---------------------------------
  #建群(LINE群組列USER表的api要錢媽的)
  def w0w0_createGroup(self,groupid):
    res=False
    conn = psycopg2.connect(self.Internal_Database_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM linegroup WHERE groupid='{groupid}'")
    rows = cur.fetchall()
    if rows ==[]:
      cur.execute(f"INSERT INTO linegroup (groupid,groupname,createdate) VALUES('{groupid}','',NOW())")
      print("攤錢群組建立成功")
      res=True

    conn.commit()
    cur.close()
    conn.close()
    return res
  
  #新增攤錢人員
  def w0w0_createMember(self,groupid,userid,username):
    res=False
    conn = psycopg2.connect(self.Internal_Database_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM linegroupMEMBER WHERE groupid='{groupid}' and userid='{userid}'")
    rows = cur.fetchall()
    if rows ==[]:
      cur.execute(f"INSERT INTO linegroupMEMBER (userid,username,groupid,createdate) VALUES('{userid}','{username}','{groupid}',NOW())")
      print("攤錢人員新增成功")
      res=True

    conn.commit()
    cur.close()
    conn.close()
    return res
