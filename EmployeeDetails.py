import pymysql
db=pymysql.connect(host='localhost',user='root',password="",database="rbs")
cursor=db.cursor()
SQL="CREATE TABLE employee_details(E_ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,E_NAME varchar(60) NOT NULL, E_USERNAME varchar(60) NOT NULL UNIQUE, E_PASSWORD varchar(60) NOT NULL)"
cursor.execute(SQL)
db.commit()