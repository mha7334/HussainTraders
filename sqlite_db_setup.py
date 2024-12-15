import sqlite3

conn = sqlite3.connect('ht.db')
print("Opened database successfully")

conn.execute('DROP TABLE IF EXISTS installments')
conn.execute('DROP TABLE IF EXISTS customers')
conn.execute('DROP TABLE IF EXISTS logs')


conn.execute('CREATE TABLE IF NOT EXISTS customers (id INTEGER primary key AUTOINCREMENT, name TEXT, father_name TEXT, addr TEXT, cnic TEXT, product TEXT, mobile_number TEXT, guarantor1 TEXT, guarantor2 TEXT, created DATETIME DEFAULT CURRENT_TIMESTAMP, region TEXT)')

conn.execute('CREATE TABLE IF NOT EXISTS installments (id INTEGER primary key AUTOINCREMENT, customer_id INTEGER, product TEXT, advance INTEGER, sale_price INTEGER, agreed_installment INTEGER, remaining_amount INTEGER, modified DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (customer_id) REFERENCES customers(id))')

conn.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER primary key AUTOINCREMENT,customer_id INTEGER, installment_id INTEGER, paid_amount INTEGER, created DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (installment_id) REFERENCES installments(id) )')



print("Tables created successfully")
conn.close()