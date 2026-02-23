import pymysql
db=pymysql.connect(host='localhost',user='root',password='',database='rbs')
cursor=db.cursor()
SQL="CREATE TABLE removed_employees(R_ID INT AUTO_INCREMENT PRIMARY KEY, E_ID INT REFERENCES employee_details(E_ID),E_NAME VARCHAR(60) NOT NULL,Reason VARCHAR(60) NOT NULL,DateFired DATE NOT NULL, TimeFired TIME NOT NULL)"
cursor.execute(SQL)
db.commit()