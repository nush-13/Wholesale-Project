import pymysql
db=pymysql.connect(host='localhost',user='root',password='',database='rbs')
cursor=db.cursor()
SQL="CREATE TABLE BILL(BillID INT PRIMARY KEY AUTO_INCREMENT, CustomerName varchar(60) NOT NULL,CustomerNumber numeric(10,0),DateOfPurchase DATE, TotalAmount decimal(10,2), PaymentMethod VARCHAR(60) NOT NULL)"
cursor.execute(SQL)