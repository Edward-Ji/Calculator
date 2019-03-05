from setuptools import setup

setup(
    app=["main.py"],
    options={
        'py2app': {'argv_emulation': True,
                   'packages': ['kivy'],
                   'iconfile': 'icon.png'}
    },
    data_files=['calculator.kv'],
    setup_requires=["py2app", "kivy"])
