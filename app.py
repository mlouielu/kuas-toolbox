# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.debug = False
app.secret_key = 'ggalkjfds;aksjdf@@'



@app.route('/')
def index():
    return render_template("index.html")


@app.route("/capital")
def capital():
    return render_template("capital.html")


@app.route("/club/beginning")
def club_beginning():
    return render_template("club_beginning.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
