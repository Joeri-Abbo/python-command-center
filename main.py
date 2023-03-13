"""Module main flask app"""
import json
import threading
import webbrowser
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
import helpers

app = Flask(__name__)

# Set a constant for the app port number
APP_PORT = 6969


@app.context_processor
def inject_now():
    """Inject the current datetime into templates"""
    return {'now': datetime.utcnow()}


@app.context_processor
def make_template_globals():
    """Register custom context processors"""
    return inject_now()


@app.route('/')
def home():
    """Render the homepage with optional messages"""
    return render_template('index.html', messages=helpers.decode_messages_param())


@app.route('/install', methods=['GET', 'POST'])
def install():
    """Handle form submission for installing/updating settings"""
    if request.method == 'POST':
        ssh_user = request.form.get('ssh_user')
        fetch_command = request.form.get('fetch_command')
        helpers.update_settings({
            'ssh_user': ssh_user,
            'fetch_command': fetch_command
        })
        messages = json.dumps({"main": "Settings are updated!"})
        return redirect(url_for('.home', messages=messages))

    return render_template('install.html')


@app.route('/servers')
def servers():
    """Show the servers"""
    return render_template('servers.html', messages=helpers.decode_messages_param())


@app.route('/fetch')
def fetch():
    """Fetch the latest data from the servers"""

    threading.Thread(target=helpers.update_servers).start()
    messages = json.dumps({"main": "Fetched data updated servers!"})
    return redirect(url_for('.home', messages=messages))


if __name__ == '__main__':
    # Start the app
    app.run(port=APP_PORT, threaded=True)

    # Open the homepage in a web browser
    threading.Thread(target=webbrowser.open, args=(f'http://127.0.0.1:{APP_PORT}/',)).start()
