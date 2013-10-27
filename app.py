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
    json = request.data # get_json()
    print json
    response = Response()
    response.set_cookie(key="success", value="True")
    response.set_cookie(key="num_processed", value="123")
    return response

@app.route('/upload', methods=['GET'])
def upload_page():
    return "Upload to here"

@app.route('/customers')
def customers_page():
    return render_template("customers.html")

@app.route('/customers/<id>')
def customer_s_page(id):
    return render_template("customers.html", id=id)

@app.route('/customers/data/ids', methods=['GET'])
def get_customers():
    return jsonify(query_db("select * from customers"))    

@app.route('/customers/data/actions/<id>', methods=['GET'])
def get_stats(id):
    return jsonify(query_db("select * from customer_actions where customer_id=123 order by timestamp asc"))

if __name__ == "__main__":
    app.run(use_debugger=True, debug=True)
