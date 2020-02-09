from flask import (
    Blueprint, render_template
)

bp = Blueprint('settings', __name__, url_prefix="/settings")


@bp.route('/')
def get_insight_page():
    return render_template("settings.html")


@bp.route('shipping')
def get_shipping_page():
    return render_template("")


@bp.route('display')
def get_display_page():
    return render_template("")


@bp.route('application')
def get_application_page():
    return render_template("")
