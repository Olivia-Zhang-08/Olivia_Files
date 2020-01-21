import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    shares = db.execute("SELECT DISTINCT Symbol FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    current_cash = cash[0]["cash"]
    total_cash = current_cash
    total_shares_in_comp_list = []
    total_price_in_comp_list = []
    names_list = []
    prices_list = []
    for share in shares:
        names_list.append(lookup(share["Symbol"])["name"])
        prices_list.append(lookup(share["Symbol"])["price"])
        total_shares_in_comp = (db.execute("SELECT SUM(Shares) FROM portfolio WHERE Symbol = :symbol AND user_id = :user_id",
                                           symbol=share["Symbol"], user_id=session["user_id"]))[0]["SUM(Shares)"]
        total_shares_in_comp_list.append(total_shares_in_comp)
        total_price_in_comp_list.append((lookup(share["Symbol"]))["price"] * total_shares_in_comp)
        total_cash += lookup(share["Symbol"])["price"] * total_shares_in_comp
    return render_template("index.html", names=names_list, prices=prices_list, shares=shares, current_cash=current_cash, total_cash=total_cash, total_shares_in_comp_list=total_shares_in_comp_list, length=len(shares), total_price_in_comp_list=total_price_in_comp_list)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol_get = request.form.get("symbol")
        try:
            shares_get = float(request.form.get("shares"))
        except:
            return apology("invalid shares")
        if not shares_get.is_integer() or shares_get < 0:
            return apology("shares must be positive integer")
        symbol_lookup = lookup(request.form.get("symbol"))

        current_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        shares = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
        if not symbol_get:
            return apology("missing symbol", 400)
        elif not symbol_lookup:
            return apology("invalid symbol", 400)
        elif not shares_get:
            return apology("missing shares", 400)

        if current_cash[0]['cash'] < shares_get * symbol_lookup["price"]:
            return apology("can't afford", 400)
        else:
            db.execute("UPDATE users SET cash = cash - :TOTAL WHERE id = :user_id",
                       user_id=session["user_id"], TOTAL=shares_get * symbol_lookup["price"])
            db.execute("INSERT INTO portfolio (user_id, Symbol, Name, Shares, Price, TOTAL) VALUES (:user_id, :Symbol, :Name, :Shares, :Price, :TOTAL)",
                       user_id=session["user_id"], Symbol=symbol_get, Name=symbol_lookup["name"], Shares=shares_get, Price=symbol_lookup["price"], TOTAL=shares_get*symbol_lookup["price"])
            db.execute("INSERT INTO history (user_id, Symbol, Shares, Price) VALUES (:user_id, :Symbol, :Shares, :Price)",
                       user_id=session["user_id"], Symbol=symbol_get, Shares=shares_get, Price=symbol_lookup["price"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/addcash", methods=["GET","POST"])
def addcash():
    if request.method == "POST":
        amt = request.form.get("cashtoadd")
        db.execute("UPDATE users SET cash = cash + :amt WHERE id = :user_id", user_id=session["user_id"], amt=amt)
        return redirect("/")
    else:
        return render_template("addcash.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    username = request.args.get("username")
    username_list = db.execute("SELECT username FROM users WHERE username = :username",
                               username=username)
    if not username_list and len(username) > 0:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    allhistory = db.execute("SELECT * FROM history WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", allhistory=allhistory)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("missing symbol")

        quote_lookup = lookup(request.form.get("symbol"))
        if not quote_lookup:
            return apology("invalid symbol")
        return render_template("quoted.html", quote=quote_lookup)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("passwords don't match")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        hashed = generate_password_hash(request.form.get("password"))

        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hashed)

        if not result:
            return apology("username is not available")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol_get = request.form.get("symbol")
        shares_get = int(request.form.get("shares"))
        symbol_lookup = lookup(request.form.get("symbol"))

        current_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        shares = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
        numshares = db.execute("SELECT Shares FROM portfolio WHERE user_id = :user_id AND Symbol = :symbol",
                               user_id=session["user_id"], symbol=symbol_get)

        if not symbol_get:
            return apology("missing symbol")
        elif not shares_get:
            return apology("missing shares")

        if shares_get > numshares[0]["Shares"]:
            return apology("too many shares")
        else:
            db.execute("UPDATE users SET cash = cash + :TOTAL WHERE id = :user_id",
                       user_id=session["user_id"], TOTAL=shares_get * symbol_lookup["price"])
            db.execute("UPDATE portfolio SET Shares = Shares - :sharestosell", sharestosell=shares_get)
            db.execute("INSERT INTO history (user_id, Symbol, Shares, Price) VALUES (:user_id, :Symbol, :Shares, :Price)",
                       user_id=session["user_id"], Symbol=symbol_get, Shares=-(shares_get), Price=symbol_lookup["price"])
        return redirect("/")
    else:
        symbols = db.execute("SELECT DISTINCT Symbol FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
        symbols_list = []
        for sym in symbols:
            symbols_list.append(sym["Symbol"])
        return render_template("sell.html", symbols=symbols, symbols_list=symbols_list, length=len(symbols))


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
