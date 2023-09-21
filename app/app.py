from flask import Flask
import os
from src.controllers.roi import welcome,marvelousRoi
app = Flask(__name__)


APPID = os.environ.get('APPID')

@app.route('/roi/', methods=['POST'])
def wel():
    return welcome()

@app.route('/roi/mining', methods=['POST'])
def marvelous():
    return marvelousRoi()


@app.route('/test/', methods=['get'])
def welTest():
    return "working"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APPID)
