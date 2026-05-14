from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

@main_bp.route("/beta")
def beta():
    return render_template("beta.html")

@main_bp.route("/results")
def results():
    return render_template("results.html")