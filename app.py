from flask import Flask
from src.controllers.roi import welcome
app = Flask(__name__)


@app.route('/roi/', methods=['POST'])
def wel():
    return welcome()

@app.route('/test/', methods=['get'])
def welTest():
    return "working"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4005)
