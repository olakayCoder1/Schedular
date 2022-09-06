from flask import flash , get_flashed_messages , render_template , request , redirect , url_for , session
from app import app , db , login_manager
from app.forms import RegisterForm , LoginForm , UserForm
from app.models import User , Task
from flask_login import login_user , logout_user , login_required , current_user


@app.route("/")
def welcome_page():
    return render_template('welcome.html')


@app.route("/register", methods=['POST','GET'])
def register_page():
    form = RegisterForm()
    if request.method == 'GET':
         return render_template('registration.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user  = User(username=form.username.data, email=form.email.data, password=form.password1.data)
            try:
                db.session.add(new_user)
                db.session.commit()
            except:
                db.session.rollback() 
            return redirect(url_for('login_page'))

        if form.errors != {}:
            for err , message in form.errors.items():
                flash(f"There was an error creating account : { message }", category='danger')
    return render_template('registration.html', form=form)


@app.route("/login", methods=['POST','GET'])
def login_page():
    form = LoginForm()
    if request.method == 'GET':
         return render_template('login.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            attempt_user = User.query.filter_by(username=form.username.data).first()
            if attempt_user and attempt_user.check_password(form.password.data):
                login_user(attempt_user)
                flash(f'You are logged in as {attempt_user.username}', category='success')
                return redirect(url_for('home_page'))
            flash('Invalid login credential', category='danger')
        if form.errors != {}:
            for err , message in form.errors.items():
                flash(f"There was an error creating account : { message }", category='danger')

        
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out. See you next time', category='success')          
    return redirect(url_for('home_page'))





@app.route("/home", methods=['GET','POST'])
@login_required
def home_page():
    user_id = current_user.id
    if request.method == 'POST':
        description = request.form['description']
        new_task = Task(description=description, creator=user_id)
        db.session.add(new_task)
        db.session.commit() 
    tasks = Task.query.filter_by(creator=user_id)
    return render_template('home.html', tasks=tasks )


@app.route("/delete/<int:id>")
def delete_task_page(id):   
    task_to_delete = Task.query.filter_by(id=int(id)).first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home_page'))


  
@app.route("/account" , methods=['GET','POST'])
def account_page():
    form = UserForm()
    print('herere 3')
    if form.validate_on_submit():
        print('herere')
        user = User.query.get_or_404(current_user.id)
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.add(user)
        db.session.commit()

    elif form.errors != {} :
        for err , message in form.errors.items():
            flash(f"There was an error updating account : { message }", category='danger')
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('about.html', form=form)


@app.route("/password-reset", methods=['GET','POST'])
@login_required
def reset_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    user = User.query.filter_by(username = current_user.username ).first()
    if user and user.check_password(old_password):
        if new_password == confirm_password :
            user.password = confirm_password
            db.session.commit()
            logout_user()
            flash(f'You are to re-log in as password updated successfully', category='success')
            return redirect(url_for('login_page')) 
        else:
            flash(f"There was an error updating account : { 'Confirm password did not match new password' }", category='danger')
    else:
        flash(f"There was an error updating account : {'Current password is not correct' }", category='danger')
    
    return redirect(url_for('account_page'))


