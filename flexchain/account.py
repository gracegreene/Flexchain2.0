from flask import (
    Blueprint, render_template
)

bp = Blueprint('account', __name__, url_prefix="/account")


@bp.route('/')
def get_account_page():
    return render_template("account.html")
