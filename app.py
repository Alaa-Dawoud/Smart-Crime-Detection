from flask import Flask, request, render_template, Response
from make_cams import create_cams
app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('/start-analyzing', methods=['POST'])
def start_analyze():
    create_cams()
    # vid_info = request.args.get("cam-data")
    return "Cameras Created and processing done"

if __name__ == '__main__':
    app.run(port=5000)