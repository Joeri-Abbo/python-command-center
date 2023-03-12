from setuptools import setup

setup(
    app=["main.py"],
    data_files=[
        "templates", "static"
    ],
    options={
        "py2app": {
            "iconfile": "logo.icns"
        }
    },
    setup_requires=["py2app"]
)
