import sqlite3

conn = sqlite3.connect('ht.db')
print("Opened database successfully")


conn.execute('CREATE TABLE regions (id INTEGER primary key AUTOINCREMENT, name TEXT, value TEXT)')

data = [
    {
    'name': 'kotkhizri',
    'value': 'Kot Khizri'
    },  
    {
    'name': 'dhaunkal',
    'value': 'Dhaunkal'
    },
    {
    'name': 'manzoorabad',
    'value': 'Mazoorabad'
    },
    {
    'name': 'veroke',
    'value': 'Veroke'
    },
    {
    'name': 'baroki',
    'value': 'Baroki'
    },
    {
    'name': 'khasray',
    'value': 'Khasray'
    },
    {
    'name': 'qudratabad',
    'value': 'Qudratabad'
    },
    {
    'name': 'alinagar',
    'value': 'Ali Nagar'
    },
    {
    'name': 'ahmadnagar',
    'value': 'Ahmad Nagar'
    },
    {
    'name': 'thatafaqirullah',
    'value': 'Thata Faqirullah'
    },
    {
    'name': 'bhattikay',
    'value': 'Bhatti Kay'
    },
    {
    'name': 'railwaycolony',
    'value': 'Railway Colony'
    },
    {
    'name': 'wazirabad',
    'value': 'Wazirabad'
    },
    {
    'name': 'nizamabad',
    'value': 'Nizamabad'
    },
    {
    'name': 'allhabad',
    'value': 'Allhabad'
    },
    {
    'name': 'daskaroad',
    'value': 'Daska abad'
    },
    {
    'name': 'wingowali',
    'value': 'Wingo wali'
    },
    {
    'name': 'Sodra',
    'value': 'sodra'
    },
    {
    'name': 'gujrat',
    'value': 'Gujrat'
    },
    {
    'name': 'kolar',
    'value': 'Kolar'
    }
]

conn.executemany("""
    INSERT INTO regions (name, value)
    VALUES (:name, :value)
""", data)

conn.commit()

conn.execute('DROP TABLE IF EXISTS installments')
conn.execute('DROP TABLE IF EXISTS customers')
conn.execute('DROP TABLE IF EXISTS logs')


conn.execute('CREATE TABLE IF NOT EXISTS customers (id INTEGER primary key AUTOINCREMENT, name TEXT, father_name TEXT, account_number TEXT, addr TEXT, cnic TEXT, product TEXT, mobile_number TEXT, guarantor1 TEXT, guarantor2 TEXT, created DATETIME DEFAULT CURRENT_TIMESTAMP, region TEXT)')

conn.execute('CREATE TABLE IF NOT EXISTS installments (id INTEGER primary key AUTOINCREMENT, customer_id INTEGER, product TEXT, advance INTEGER, sale_price INTEGER, agreed_installment INTEGER, remaining_amount INTEGER, modified DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (customer_id) REFERENCES customers(id))')

conn.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER primary key AUTOINCREMENT,customer_id INTEGER, installment_id INTEGER, paid_amount INTEGER, created DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (installment_id) REFERENCES installments(id) )')


print("Tables created successfully")
conn.close()