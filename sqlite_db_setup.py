import sqlite3

conn = sqlite3.connect('ht.db')
print("Opened database successfully")

# conn.execute('DROP TABLE installments')
# conn.execute('DROP TABLE products')
# conn.execute('DROP TABLE customers')

# conn.execute('CREATE TABLE customers (name TEXT, addr TEXT, region TEXT, cnic INTEGER primary key, phonenumber INTEGER)')

# conn.execute('CREATE TABLE products (name TEXT, purchaseprice INTEGER, id INTEGER primary key AUTOINCREMENT)')

conn.execute('CREATE TABLE installments (product_id INTEGER, advance INTEGER,customer_cnic INTEGER, saleprice INTEGER, installment INTEGER, remainingamount INTEGER, FOREIGN KEY (customer_cnic) REFERENCES customers(cnic),FOREIGN KEY (product_id) REFERENCES products(id))')
print("Table created successfully")
conn.close()