import pymysql 
db=pymysql.connect(host='localhost',user="root",password='',database='rbs')
cursor=db.cursor()
SQL="CREATE TABLE admin_details(A_ID int AUTO_INCREMENT PRIMARY KEY,A_NAME varchar(60) NOT NULL,A_USERNAME varchar(60) NOT NULL UNIQUE,A_PASSWORD varchar(60) NOT NULL)"
cursor.execute(SQL)
db.commit()