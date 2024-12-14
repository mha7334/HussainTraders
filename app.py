from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

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
         addr = request.form['address']
         region = request.form['region']
                 
         with sql.connect("student_database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO customers (cnic,name,addr,region) VALUES (?,?,?,?)",(cnic, name, addr,region) )
            con.commit()
            msg = "Record successfully added!"
      except:
         con.rollback()
         msg = "error in insert operation"
      finally:
         return render_template("listcust.html",msg = msg)
         con.close()


# @app.route('/list')
# def list():
#    con = sql.connect("student_database.db")
#    con.row_factory = sql.Row
   
#    cur = con.cursor()
#    cur.execute("select * from students")
   
#    students = cur.fetchall();
#    return render_template("list.html", students = students)

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