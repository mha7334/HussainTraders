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
         
         remaining_amount = int(price) - int(advance)
         agreed_installment = (int(price) - int(advance))/10
         
         with sql.connect("ht.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO customers (cnic,name,father_name, addr,mobile_number,product, guarantor1, guarantor2) VALUES (?,?,?,?,?,?,?,?)",(cnic, name,father_name, addr,mobile_number,product,guarntor1, guarntor2))
            
            cur.execute("INSERT INTO installments (customer_cnic,advance,sale_price,remaining_amount, agreed_installment, created ) VALUES (?,?,?,?,?,?)",(cnic, advance,price,remaining_amount, agreed_installment, str(date.today())) )
            # cur.execute("INSERT INTO logs (customer_cnic, name, product, paid_amount, created) VALUES (?, ?, ?, ?, ?)", (cnic, name, product, advance, date.today ))
          
            con.commit()
            msg = "findisted"
     
      except:
         con.rollback()
         msg = "some error occuurred"
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