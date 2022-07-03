

from market import app
from flask import flash, render_template,redirect, request,url_for
from market.models import Item, User
from market.forms import LoginForm, RegisterForm,PurchaseItemForm,SellItemForm
from market import db
from market import bcrypt
from market import login_manager
from flask_login import current_user, login_user,logout_user,login_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_item_form = PurchaseItemForm()
    sell_item_form = SellItemForm()

    if request.method=='POST':
        purchase_item = request.form.get('purchased_item')
        sold_item = request.form.get('sold_item')
        
        p_item_object = Item.query.filter_by(name=purchase_item).first()
        #purchase item logic
        if p_item_object:
            if p_item_object.buy(current_user):
                flash(f'You have purchased {p_item_object.name} for {p_item_object.price} $',category='success')
            else:
                flash(f'You do not have enough money to purchase {p_item_object.name}',category='danger')

        #sell item logic
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if s_item_object.sell(current_user):
                flash(f'You have sold {s_item_object.name} for {s_item_object.price} $',category='success')
            else:
                flash(f'You do not own {s_item_object.name}',category='danger')
        
        return redirect(url_for('market_page'))

    if request.method=='GET':
        items =Item.query.filter_by(user_id=None).all()
        owned_items = Item.query.filter_by(user_id=current_user.id).all()
        return render_template('market.html',owned_items = owned_items, items=items, purchase_form=purchase_item_form, sell_form=sell_item_form)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
         email=form.email.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account Created successfully ! you are loged in as   {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))

    if(form.errors != {}):
            for err_msg in form.errors.values():
                flash(f'There was an error in creating your account: {err_msg}', category='danger')    

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password_correction(form.password.data):
            login_user(user)
            flash(f'Welcome {user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')

    return render_template('login.html',form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect(url_for('home_page'))
