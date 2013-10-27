from flask import Flask
from flask import request
from flask import Response
from flask import render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("landing.html")

@app.route('/upload', methods=['POST'])
def upload():
    json = request.data # get_json()
    print "~", request
    print json
    response = Response()
    response.set_cookie(key="success", value="True")
    response.set_cookie(key="num_processed", value="123")
    return response

@app.route('/upload', methods=['GET'])
def upload_page():
    return "Upload to here"

if __name__ == "__main__":
    app.run(use_debugger=True, debug=True)
