from flask import Flask, render_template, request, redirect, session, flash
import sqlite3 as sql
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'fasdgfdgdfg'

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/addcust')
def new_customer():    
    with sql.connect("ht.db") as con:            
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT name, value FROM regions")
      regions = cur.fetchall()
      return render_template('add_customer.html', regions=regions)

@app.route('/pay', methods = ['POST'])
def pay_installment():
   if request.method == 'POST':
      try:
         customer_id = request.form['customerid']
         installment_id = request.form['installmentid']
         amount = request.form['amount']

         with sql.connect("ht.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            cur.execute("SELECT * FROM installments WHERE customer_id = ? AND id = ?", (customer_id, installment_id))

            installment = cur.fetchone()
            remaining_amount = int(installment['remaining_amount']) - int(amount)      

            modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cur.execute("""
            UPDATE installments 
               SET remaining_amount = :remaining_amount,
                   modified = :modified     
               WHERE customer_id = :customer_id AND id = :installment_id
            """, {
            'remaining_amount': remaining_amount,
            'customer_id': customer_id,
            'installment_id': installment_id,
            'modified': modified})

            cur.execute("""
                        INSERT INTO logs (customer_id, installment_id, paid_amount) VALUES 
                        (:customer_id, :installment_id, :paid_amount)""", 
                        (customer_id,installment_id, amount))
            msg = "Success!"          
            con.commit()            
      except:
         con.rollback()
         msg = "Error occurred in update"
      finally: 
         return fetchAllInstallments(msg) 
         con.close()

@app.route('/addregion', methods = ['GET'])
def addregion_get():
   return render_template("add_region.html")

@app.route('/addregion', methods = ['POST'])
def addregion():
   if(request.method == 'POST'):
      try:
         regionname = request.form['regionname']

         name = regionname.lower().replace(" ", "")

         with sql.connect("ht.db") as con:
               cur = con.cursor()

               cur.execute("""
                        INSERT INTO regions (name, value) VALUES 
                                                (:name, :value)""",
                                                (name, regionname))
            
               con.commit()
               msg = "NEW REGION ADDED"
     
      except:
            con.rollback()
            msg = "Error occurred in insertion"
      finally:
            return render_template("add_region.html", msg=msg)       
            con.close()

@app.route('/addcust',methods = ['POST', 'GET'])
def addcust():
   if request.method == 'POST':
      try:
         cnic = request.form['cnic']
         account = request.form['account']
         name = request.form['name']
         father_name = request.form['father']
         mobile_number = request.form['mobile']
         guarntor1 = request.form['guarantor1']
         guarntor2 = request.form['guarantor2']
         product = request.form['product']
         advance = request.form['advance']
         price = request.form['price']
         addr = request.form['address']
         region = str(request.form['region'])
         
         remaining_amount = int(price) - int(advance)
         agreed_installment = (int(price) - int(advance))/10
         
         with sql.connect("ht.db") as con:
            cur = con.cursor()

            cur.execute("""
                        INSERT INTO customers (name, father_name, addr, cnic, account_number, product, mobile_number, guarantor1, guarantor2 , region) VALUES 
                                                (:name, :father_name, :addr, :cnic, :account_number, :product, :mobile_number, :guarantor1, :guarantor2, :region)""",
                                                (name, father_name, addr, cnic, account, product, mobile_number, guarntor1, guarntor2, region))
            
           
            customer_id = cur.lastrowid

            cur.execute("""
                        INSERT INTO installments (customer_id,product, advance,sale_price,remaining_amount, agreed_installment) VALUES 
                                                (:customer_id, :product, :advance, :sale_price, :remaining_amount, :agreed_installment)""",
                                                (customer_id, product, advance,price,remaining_amount, agreed_installment))
            
            installment_id = cur.lastrowid

            cur.execute("""
                        INSERT INTO logs (customer_id, installment_id, paid_amount) VALUES 
                        (:customer_id, :installment_id, :paid_amount)""", 
                        (customer_id,installment_id, advance))
          
            con.commit()
            msg = "NEW SALE ADDED!"
     
      except:
         con.rollback()
         msg = "Error occurred in insertion"
      finally:
         return fetchAllInstallments(msg)       
         con.close()

@app.route('/listcust')
def listcust():
   msg = ""
   return fetchAllInstallments(msg)

def fetchAllInstallments(msg):
   con = sql.connect("ht.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from installments Inner join customers on installments.customer_id = customers.id ORDER BY MODIFIED DESC LIMIT 100")
   customers = cur.fetchall()

   cur.execute("SELECT name, value FROM regions")
   regions = cur.fetchall()
   
   return render_template("listcust.html", customers=customers, regions=regions, msg=msg)
   
def fetchAllInstallmentsByRegion(msg,region):
   con = sql.connect("ht.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("""select * from installments Inner join customers on installments.customer_id = customers.id ORDER BY MODIFIED DESC LIMIT 100
               WHERE region = ?
               """, (region,))
   customers = cur.fetchall()

   cur.execute("SELECT name, value FROM regions")
   regions = cur.fetchall()
   
   return render_template("listcust.html", customers=customers, regions=regions, msg=msg, selectedregion=region)

@app.route('/shortpayments', methods = ['POST'])
def short_installments():
   region = request.form['region']
   con = sql.connect("ht.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()

   now = datetime.now()
   current_month_5th = now.replace(day=18).strftime('%Y-%m-%d %H:%M:%S')

   cur.execute("SELECT name, value FROM regions")
   regions = cur.fetchall()

   if region == 'all':
# Query for records modified on or after the 5th of the current month
      cur.execute("""
         select * from installments Inner join customers on installments.customer_id = customers.id
         WHERE modified <= ?
      """, (current_month_5th,))

      customers = cur.fetchall()
      return render_template("listcust.html", customers = customers, regions=regions, selected_region='all')
   else:
      cur.execute("""
         select * from installments Inner join customers on installments.customer_id = customers.id
         WHERE modified <= ? AND region = ?
      """, (current_month_5th,region))

      customers = cur.fetchall()
      return render_template("listcust.html", customers = customers, regions=regions, selected_region=region)

@app.route('/ledger', methods = ['POST'])
def ledger():
   customer_id = request.form['customerid']
   installment_id = request.form['installmentid']
   
   con = sql.connect("ht.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("""
      select * from installments Inner join customers on installments.customer_id = customers.id
      WHERE installments.id = ? AND customers.id = ?
   """, (installment_id,customer_id))

   customers = cur.fetchall()

   cur.execute("""
      select * from logs
      WHERE customer_id = ?
               """, (customer_id,))

   logs = cur.fetchall()
   return render_template("result.html", msg="", customers=customers, logs=logs)



@app.route('/searchcnic', methods = ['POST'])
def searchcnic():

   cnic = request.form['cnic']
   con = sql.connect("ht.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()

   # cur.execute("select * from customers where cnic = ?", (cnic))

   # customer = cur.fetchone()

   cur.execute("select * from installments Inner join customers on installments.customer_id = customers.id where customers.cnic = ?", (cnic,))
   
   customers = cur.fetchall()
   return render_template("listcust.html", customers = customers)


@app.route('/searchmobile', methods = ['POST'])
def searchmobile():

   mobile = request.form['mobile']
   con = sql.connect("ht.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()

   cur.execute("select * from installments Inner join customers on installments.customer_id = customers.id where customers.mobile_number = ?", (mobile,))
   customers = cur.fetchall()
   return render_template("listcust.html", customers = customers)

@app.route('/searchname', methods = ['POST'])
def searchname():

   name = request.form['name']
   con = sql.connect("ht.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()

   cur.execute("SELECT * FROM installments INNER JOIN customers ON installments.customer_id = customers.id WHERE customers.name LIKE ?", (f"%{name}%",)
)

   customers = cur.fetchall()
   return render_template("listcust.html", customers = customers)


if __name__ == '__main__':
   app.run(debug = True)