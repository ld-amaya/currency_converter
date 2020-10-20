from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates
from convert import Conversion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

currency = CurrencyRates()


@app.route('/')
def home():
    """Return home page"""
    cnyFrom = session.get('from', '')
    cnyTo = session.get('to', '')
    amount = session.get('amount', 0)
    return render_template('index.html', cnyFrom=cnyFrom, cnyTo=cnyTo, amount=amount)


@app.route('/checkInput', methods=['POST'])
def checkInput():
    """Check if user input is valid"""
    cnyFrom = request.form['cnyFrom'].upper()
    session['from'] = cnyFrom

    cnyTo = request.form['cnyTo'].upper()
    session['to'] = cnyTo

    amount = request.form['amount']
    session['amount'] = amount

    convert = Conversion(cnyFrom, cnyTo, amount)

    # Check if user input is valid
    isValid = convert.checkCurrency()
    if (isValid == "Invalid from"):
        flash(f"Currency from not a valid code: {cnyFrom}", "error")
        return redirect('/')
    elif (isValid == "Invalid to"):
        flash(f"Currency to not a valid code: {cnyTo}", "error")
        return redirect('/')
    elif(isValid == 'Invalid amount'):
        flash("Invalid amount", "error")
        return redirect('/')
    else:
        return redirect('/convert')


@app.route('/convert')
def convert():
    """Returns the conversion value"""
    convert = Conversion(session['from'], session['to'], session['amount'])
    val = convert.convertCurrency()
    return render_template("conversion.html", val=val)


@app.route("/reset")
def reset():
    """Resets the session"""
    session['from'] = ''
    session['to'] = ''
    session['amount'] = 0
    return redirect('/')
