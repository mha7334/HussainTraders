import sqlite3

conn = sqlite3.connect('ht.db')
print("Opened database successfully")

# conn.execute('DROP TABLE installments')
#onn.execute('DROP TABLE customers')
# conn.execute('DROP TABLE logs')


conn.execute('CREATE TABLE customers (name TEXT, father_name TEXT, addr TEXT, cnic TEXT primary key, product TEXT, mobile_number TEXT, guarantor1 TEXT, guarantor2 TEXT, created TEXT)')

conn.execute('CREATE TABLE installments (product TEXT, advance INTEGER,customer_cnic TEXT, sale_price INTEGER, agreed_installment INTEGER, remaining_amount INTEGER, created TEXT, modified TEXT, FOREIGN KEY (customer_cnic) REFERENCES customers(cnic))')

conn.execute('CREATE TABLE logs (id INTEGER primary key AUTOINCREMENT, customer_cnic TEXT, name, TEXT,  product TEXT, paid_amount INTEGER, created TEXT)')

print("Tables created successfully")
conn.close()