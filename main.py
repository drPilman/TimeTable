from flask import Flask, render_template, redirect
from db.db import getWeekById, getTime

app = Flask(__name__)
time = getTime()


def print_hi(name):
    print(f'Hi, {name}')


@app.route("/<group_id>/<week>")
def week_by_id(group_id, week):
    return render_template('index.html', data=getWeekById(group_id, week), time=time)


@app.route("/")
def index():
    return redirect("/11/0")


if __name__ == "__main__":
    app.run(debug=True)
