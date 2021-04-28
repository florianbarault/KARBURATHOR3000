from flask import Flask, render_template, request, redirect
from APP.data import bdd as b
from APP.controller import formulaire as f

app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "template"
app.config.from_object('config')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/new_route")
def new_route():
    return render_template("new_route.html")


@app.route("/historic")
def historic():
    return render_template("historic.html")


@app.route("/comments")
def comments():
    return render_template("comments.html")

