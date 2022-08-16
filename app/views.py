from flask import flash , get_flashed_messages , render_template , request , redirect , url_for
from app import app , db , login_manager
from app.forms import RegisterForm , LoginForm
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
def home_page():
    if request.method == 'POST':
        description = request.form['description']
        print(description)
    print(current_user.id)
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks )


@app.route("/delete/<int:id>")
def delete_task_page(id):   
    task_to_delete = Task.query.filter_by(id=int(id)).first()
    print(task_to_delete)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home_page'))


  
@app.route("/about")
def about_page():
    return render_template('about.html')


