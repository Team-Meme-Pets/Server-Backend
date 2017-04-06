from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "IT'S WORKING THE WORLD SAYS HELLO."
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9800)
