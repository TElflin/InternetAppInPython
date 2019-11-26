from app import app
from flask import flash, redirect, url_for, render_template, request
from app.forms import LoginForm, RegistrationForm, IndexForm, CheckForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, StockShares, Date, UserShares, Company
from app import db
from werkzeug.urls import url_parse




@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    indexForm = IndexForm()
    checkForm = CheckForm()
    newestday = Date.query.order_by(Date.day.desc()).first()  # THis way our newest day is first in table
    date = str(newestday.day)
    shares = StockShares.query.filter_by(date=newestday.day).all()
    indexForm.date.list=('db_dates')
    dates = Date.query.order_by(Date.day.desc()).all()
    if current_user.is_authenticated:
        usershares = StockShares.query.filter_by(date=date).join(UserShares, UserShares.user_company == StockShares.stockName).filter_by(user_id=current_user.id).all()
        if indexForm.submitDate.data and indexForm.validate_on_submit():
            date = indexForm.date.data
            shares = StockShares.query.filter_by(date=date).all()
            usershares = StockShares.query.filter_by(date=date).join(UserShares, UserShares.user_company == StockShares.stockName).filter_by(user_id = current_user.id).all()
        return render_template('index.html', title="Porzadna praca", indexForm=indexForm, shares=shares,
                               checkForm=checkForm, usershares=usershares, dates=dates)
    else:
        if indexForm.submitDate.data and indexForm.validate_on_submit():
            date = indexForm.date.data
            shares = StockShares.query.filter_by(date=date).all()
    return render_template('index.html', title="Porzadna praca", indexForm=indexForm, shares=shares,
                           checkForm=checkForm, dates=dates)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return  redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title ='Sign In', form = form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    indexForm = IndexForm()
    checkForm = CheckForm()
    newestday = Date.query.order_by(Date.day.desc()).first()  # THis way our newest day is first in table
    date = newestday.day
    indexForm.date.choices = [(str(date.day), str(date.day)) for date in Date.query.order_by(Date.day.desc()).all()]
    usershares = StockShares.query.filter_by(date=date).join(UserShares, UserShares.user_company == StockShares.stockName).filter_by(user_id = current_user.id).all()
    if indexForm.submitDate.data and indexForm.validate_on_submit():
        date = indexForm.date.data
        usershares = StockShares.query.filter_by(date=date).join(UserShares, UserShares.user_company == StockShares.stockName).filter_by(user_id = current_user.id).all()
    return render_template('myshares.html', user=user, usershares=usershares, indexForm=indexForm, checkForm=checkForm )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title = 'New player', form = form)


@app.route('/statistics/<sharesName>')
def statistics(sharesName):
    axislenght = 10
    shares=StockShares.query.filter_by(stockName=sharesName).order_by( StockShares.date.desc()).limit(axislenght)
    return render_template('statistics.html', title='Statistics', shares = shares)

@app.route('/update', methods=['POST'])
@login_required
def update():
    results = request.form.getlist('check')
    for result in results:
        exist = UserShares.query.filter_by(user_id=current_user.id).filter_by(user_company=result).scalar() is not None
        if exist:
            flash('{} already in observed by user'.format(result))
            continue
        us = UserShares(user_id=current_user.id, user_company=result)
        db.session.add(us)
        db.session.commit()
        flash('{} added to observed by user'.format(result))
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
@login_required
def remove():
    results = request.form.getlist('check')
    for result in results:
        us = UserShares.query.filter_by(user_id=current_user.id).filter_by(user_company=result).first()
        record = UserShares.query.get(us.id)
        db.session.delete(record)
        db.session.commit()
        flash('{} removed from observed by user'.format(result))
    return redirect(url_for('user', username=current_user.username))
