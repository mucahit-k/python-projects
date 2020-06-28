from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World from me'

if __name__ == '__main__':
    # app.run('localhost', port=5000, debug=True)
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)