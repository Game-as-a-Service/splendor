from flask.testing import FlaskClient

guest_user = None
guest_email = None
guest_type = None
guest_plan = "Guest"

free_user = "free-user"
free_mail = "free@email.com"
free_type = "normal"
free_plan = "Free"

basic_user = "basic-user"
basic_mail = "basic@email.com"
basic_type = "normal"
basic_plan = "Basic Yearly"

business_user = "business-user"
business_mail = "business@email.com"
business_type = "business"
business_plan = "Basic Yearly"

test_watchlist = [{"name": "test", "symbols": ["AAPL"], "watchlistId": "test"}]


def setup_guest_session(client: FlaskClient):
    with client.session_transaction() as sess:
        sess["user_id"] = guest_user
        sess["email"] = guest_email
        sess["account_type"] = guest_type
        sess["plan"] = guest_plan


def setup_free_session(client: FlaskClient):
    with client.session_transaction() as sess:
        sess["user_id"] = free_user
        sess["email"] = free_mail
        sess["account_type"] = free_type
        sess["plan"] = free_plan


def setup_basic_session(client: FlaskClient):
    with client.session_transaction() as sess:
        sess["user_id"] = basic_user
        sess["email"] = basic_mail
        sess["account_type"] = basic_type
        sess["plan"] = basic_plan


def setup_business_session(client: FlaskClient):
    with client.session_transaction() as sess:
        sess["user_id"] = business_user
        sess["email"] = business_mail
        sess["account_type"] = business_type
        sess["plan"] = business_plan
