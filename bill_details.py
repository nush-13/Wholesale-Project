import pymysql
db=pymysql.connect(host='localhost',user="root",password="",database="rbs")
cursor=db.cursor()
SQL="CREATE TABLE bill_products(R_ID INT AUTO_INCREMENT PRIMARY KEY,bill_id INT REFERENCES bill(BillID),product_id INT REFERENCES productdetails(ProductID), product_name varchar(60) NOT NULL, item_price INT NOT NULL, total_product_amount INT NOT NULL)"
cursor.execute(SQL)
db.commit()
db.close()