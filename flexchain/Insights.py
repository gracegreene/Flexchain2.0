from flask import (
    Blueprint, render_template
)

bp = Blueprint('insight', __name__, url_prefix="/insight")


@bp.route('/')
def get_insight_page():
    return render_template("ask.html")


@bp.route('stock-level')
def get_stock_level_page():
    return render_template("stock-levels.html")
