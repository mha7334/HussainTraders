from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
from datetime import date

app = Flask(__name__)
app.secret_key = 'fasdgfdgdfg'


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/addcust')
def new_customer():
   return render_template('add_customer.html')

@app.route('/addcust',methods = ['POST', 'GET'])
def addcust():
   if request.method == 'POST':
      try:
         cnic = request.form['cnic']
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
                        INSERT INTO customers (name, father_name, addr, cnic, product, mobile_number, guarantor1, guarantor2 , region) VALUES 
                                                (:name, :father_name, :addr, :cnic, :product, :mobile_number, :guarantor1, :guarantor2, :region)""",
                                                (name, father_name, addr, cnic, product, mobile_number, guarntor1, guarntor2, region))
            
           
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
            msg = "RECORD ADDED SUCCESSFULLY!"
     
      except:
         con.rollback()
         msg = "Error occurred in insertion"
      finally:
         return render_template("listcust.html",msg = msg)
         con.close()

@app.route('/listcust')
def listcust():
   con = sql.connect("student_database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from customers")
   
   customers = cur.fetchall();
   return render_template("listcust.html", customers = customers)


if __name__ == '__main__':
   app.run(debug = True)