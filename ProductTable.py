import pymysql
db=pymysql.connect(host='localhost',user='root',password="",database='rbs')
cursor=db.cursor()
SQL="CREATE TABLE ProductDetails(ProductID INT PRIMARY KEY AUTO_INCREMENT,ProductName varchar(60) NOT NULL,Quantity INT NOT NULL,PurchaseRate INT NOT NULL, SalesRate INT NOT NULL, Profit INT NOT NULL,SupplierID INT REFERENCES supplierdetails(SupplierID))"
cursor.execute(SQL)
cursor.close()