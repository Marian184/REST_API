from flask import Flask

app = Flask(__name__)

#ruta donde va a preguntar o realizar el request
@app.route('/') #/ home page del decorator puede ir 'http://www.google.com/
def home():
    return "Hello, world"

app.run(port=5000)

