import json
import webbrowser
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
import helpers

app = Flask(__name__)

# Set a constant for the app port number
APP_PORT = 6969


# Inject the current datetime into templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


# Render the homepage with optional messages
@app.route('/')
def home():
    messages = None
    try:
        messages = json.loads(request.args.get('messages', 'null'))
    except json.JSONDecodeError:
        pass
    return render_template('index.html', messages=messages)


# Handle form submission for installing/updating settings
@app.route('/install', methods=['GET', 'POST'])
def install():
    if request.method == 'POST':
        ssh_user = request.form.get('ssh_user')
        helpers.update_settings({'ssh_user': ssh_user})
        messages = json.dumps({"main": "Settings are updated!"})
        return redirect(url_for('.home', messages=messages))
    else:
        return render_template('install.html')


@app.route('/servers')
def servers():
    messages = None
    try:
        messages = json.loads(request.args.get('messages', 'null'))
    except json.JSONDecodeError:
        pass
    return render_template('servers.html', messages=messages)


@app.route('/fetch')
def fetch():
    messages = json.dumps({"main": "Fetched data updated servers!"})
    return redirect(url_for('.home', messages=messages))


if __name__ == '__main__':
    # Start the app and open the homepage in a web browser
    app.run(port=APP_PORT)
    webbrowser.open(f'http://127.0.0.1:{APP_PORT}/')
