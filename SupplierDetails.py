import pymysql
db=pymysql.connect(host='localhost',user='root',password="",database='rbs')
cursor=db.cursor()
SQL="CREATE TABLE SupplierDetails(SupplierID INT AUTO_INCREMENT PRIMARY KEY, SupplierName varchar(60) NOT NULL, DateAdded Date NOT NULL, TimeAdded time NOT NULL)"
cursor.execute(SQL)
db.close()