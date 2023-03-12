from flask import Flask, render_template
from datetime import datetime
import webbrowser

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    port = 6969
    # Start Flask app
    app.run(
        port=port,
    )
    webbrowser.open('http://127.0.0.1:{port}/'.format(
        port=port
    ))
