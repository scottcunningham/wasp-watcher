from flask import Flask
from flask import request
from flask import Response
from flask import render_template
import sqlite3
from flask import jsonify
from flask import g

app = Flask(__name__)

DATABASE = 'sqlite-database.db'

def query_db(query, args=()):
    cur = g.db.execute(query, args)
    return cur.fetchall()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def main():
    return render_template("landing.html")

@app.route('/upload', methods=['POST'])
def upload():
    json = request.get_json()

    response = Response()
    response.set_cookie(key="success", value="True")
    response.set_cookie(key="num_processed", value="123")
    return response

@app.route('/upload', methods=['GET'])
def upload_page():
    return "Upload to here"

@app.route('/customers')
def customers_page():
    all_customers = query_db("select * from customers");
    return render_template("customers.html", customers=all_customers)

@app.route('/customers/<id>')
def customer_overview(id):
    name = query_db("select * from customers where customer_id=" + str(id))
    timestamps = query_db("select * from customer_actions where customer_id="+ str(id) +" order by timestamp asc")
    
    return render_template("graphs.html", id=id, name=name[0], timestamps=timestamps)

@app.route('/customers/data/ids', methods=['GET'])
def get_customers():
   
    resp = Response(response=query_db("select * from customers"),
                    status=200,
                    mimetype="application/json")
    return resp

@app.route('/customers/data/actions/<id>', methods=['GET'])
def get_stats(id):
    a = query_db("select timestamp from customer_actions where customer_id=123 order by timestamp asc")

    '''
    resp = Response(response=query_db("select * from customer_actions where customer_id=123 order by timestamp asc"),
                    status=200,
                    mimetype="application/json")
    
    '''
    return a
if __name__ == "__main__":
    app.run(use_debugger=True, debug=True)
