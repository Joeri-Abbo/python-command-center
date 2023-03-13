"""Module main flask app"""
import json
import threading
import webbrowser
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
import helpers
import server_helper

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
    return render_template('servers.html', messages=helpers.decode_messages_param(), servers=helpers.get_servers())


@app.route('/server/<string:server_name>')
def server(server_name):
    server = server_helper.get_server(server_name)

    if server is None:
        messages = json.dumps({"main": "No server found with slug" + server_name + "!"})

        return redirect(url_for('.servers', messages=messages))
    """Show the server"""
    return render_template(
        'server.html',
        server=server,
        messages=helpers.decode_messages_param(),
        server_helper=server_helper
    )


@app.route('/server/<string:server_name>/reboot')
def server_reboot(server_name):
    server = server_helper.get_server(server_name)
    if server is None:
        messages = json.dumps({"main": "No server found with slug" + server_name + "!"})

        return redirect(url_for('.servers', messages=messages))
    threading.Thread(target=server_helper.run_reboot(server.get('host'))).start()
    messages = json.dumps({"main": "Server reboot " + server.get('title') + "!"})
    return redirect(url_for('.servers', messages=messages))


@app.route('/server/<string:server_name>/docker-prune')
def docker_prune(server_name):
    server = server_helper.get_server(server_name)
    if server is None:
        messages = json.dumps({"main": "No server found with slug" + server_name + "!"})

        return redirect(url_for('.servers', messages=messages))
    threading.Thread(target=server_helper.run_docker_system_prune(server.get('host'))).start()
    messages = json.dumps({"main": "Docker system prune " + server.get('title') + "!"})
    return redirect(url_for('.servers', messages=messages))


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
