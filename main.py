"""Flask application entry point."""

from __future__ import annotations

import json
import threading
import webbrowser
from datetime import datetime
from typing import Any, Dict

from flask import Flask, redirect, render_template, request, url_for

import helpers
import server_helper

APP_PORT = 6969


def create_app() -> Flask:
    app = Flask(__name__)

    @app.context_processor
    def inject_now() -> Dict[str, Any]:
        return {"now": datetime.utcnow()}

    @app.route("/")
    def home() -> str:
        return render_template("index.html", messages=helpers.decode_messages_param())

    @app.route("/install", methods=["GET", "POST"])
    def install():
        if request.method == "POST":
            helpers.update_settings(
                {
                    "ssh_user": request.form.get("ssh_user", ""),
                    "fetch_command": request.form.get("fetch_command", ""),
                }
            )
            messages = json.dumps({"main": "Settings are updated!"})
            return redirect(url_for("home", messages=messages))

        return render_template("install.html")

    @app.route("/servers")
    def servers() -> str:
        return render_template(
            "servers.html",
            messages=helpers.decode_messages_param(),
            servers=helpers.get_servers(),
        )

    @app.route("/server/<string:server_name>")
    def server(server_name: str):
        server = server_helper.get_server(server_name)
        if server is None:
            messages = json.dumps({"main": f"No server found with slug {server_name}!"})
            return redirect(url_for("servers", messages=messages))

        return render_template(
            "server.html",
            server=server,
            messages=helpers.decode_messages_param(),
            server_helper=server_helper,
        )

    @app.route("/server/<string:server_name>/reboot")
    def server_reboot(server_name: str):
        server = server_helper.get_server(server_name)
        if server is None:
            messages = json.dumps({"main": f"No server found with slug {server_name}!"})
            return redirect(url_for("servers", messages=messages))

        threading.Thread(
            target=server_helper.run_reboot,
            args=(server.get("host"),),
            daemon=True,
        ).start()
        messages = json.dumps({"main": f"Server reboot {server.get('title')}!"})
        return redirect(url_for("servers", messages=messages))

    @app.route("/server/<string:server_name>/docker-prune")
    def docker_prune(server_name: str):
        server = server_helper.get_server(server_name)
        if server is None:
            messages = json.dumps({"main": f"No server found with slug {server_name}!"})
            return redirect(url_for("servers", messages=messages))

        threading.Thread(
            target=server_helper.run_docker_system_prune,
            args=(server.get("host"),),
            daemon=True,
        ).start()
        messages = json.dumps({"main": f"Docker system prune {server.get('title')}!"})
        return redirect(url_for("servers", messages=messages))

    @app.route("/fetch")
    def fetch():
        threading.Thread(target=helpers.update_servers, daemon=True).start()
        messages = json.dumps({"main": "Fetched data updated servers!"})
        return redirect(url_for("home", messages=messages))

    return app


app = create_app()


def main() -> None:
    url = f"http://127.0.0.1:{APP_PORT}/"
    threading.Thread(target=lambda: webbrowser.open(url), daemon=True).start()
    app.run(port=APP_PORT, threaded=True)


if __name__ == "__main__":
    main()
