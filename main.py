from flask import Flask
from flask import render_template #to render html
app = Flask(__name__, template_folder="WebFrontEndCode/templates", static_folder="WebFrontEndCode/static/")


@app.route('/')
@app.route('/index.html')
def home_page():
    return render_template("index.html")


@app.route('/ask.html')
def ask_page():
    return render_template("ask.html")


@app.route('/dashboard-settings.html')
def dashboard_settings_page():
    return render_template("dashboard-settings.html")


@app.route('/locations.html')
def location_page():
    return render_template("locations.html")


@app.route('/product.html')
def product_page():
    return render_template("product.html")


@app.route('/settings.html')
def settings_page():
    return render_template("settings.html")


if __name__ == '__main__':
    app.run()
