from flask import Flask
from flask import request
from flask import Response
from flask import render_template
import sqlite3
from flask import g
from flask import jsonify
import json
import time

app = Flask(__name__)

ONE_SECOND_MILLIS = 1000
ONE_MINUTE_MILLIS = ONE_SECOND_MILLIS * 60
ONE_HOUR_MILLIS = ONE_MINUTE_MILLIS * 60 
ONE_DAY_MILLIS = ONE_HOUR_MILLIS * 24
ONE_WEEK_MILLIS = ONE_DAY_MILLIS * 7

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
    query_db("insert into customer_actions values (" + request.values["uid"] + ", " + str(int(time.time()*1000)) + ")")
    return Response(status=200)

@app.route('/upload', methods=['GET'])
def upload_page():
    return "Upload to here"

@app.route('/customers')
def customers_page():
    all_customers = query_db("select * from customers");
    return render_template("customers.html", customers=all_customers)

@app.route('/customers/<id>')
def customer_overview(id):
    ts_one_week_ago = int(time.time() * 1000) - ONE_DAY_MILLIS*7
    # The SQL gets all door activity between now and exactly one week ago, and figures out how many days ago each movement
    # was by getting (timestamp - timestamp of one week ago) / the number of ms in one day
    timestamps = query_db(" SELECT (timestamp - " + str(ts_one_week_ago) + ")/" + str(ONE_DAY_MILLIS) + " AS days_ago, COUNT(customer_id) as count FROM customer_actions WHERE customer_id=" + str(id) + " AND timestamp > " + str(ts_one_week_ago) + " AND customer_id=" + str(id) + " GROUP BY days_ago ORDER BY days_ago DESC")
    # print timestamps
    name = query_db("select * from customers where customer_id=" + str(id))
    return render_template("graphs.html", id=id, name=name[0][1], timestamps=timestamps)

@app.route('/customers/data/ids', methods=['GET'])
def get_customers():
    return query_db("select * from customers")

@app.route('/customers/data/actions/<id>', methods=['GET'])
def get_stats(id):
    a = query_db("select timestamp from customer_actions where customer_id=" + str(id) + " ORDER BY timestamp asc")
    return a

if __name__ == "__main__":
    app.run(use_debugger=True, debug=True)
