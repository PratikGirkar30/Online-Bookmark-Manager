from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import BookmarkForm, LoginForm, RegisterForm

# Initialize Flask and extensions
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bookmark_info'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bookmarks = db.relationship('Bookmark', backref='owner', lazy=True)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500))
    category = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def index():
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', bookmarks=bookmarks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Login unsuccessful. Check username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/add_bookmark", methods=['GET', 'POST'])
@login_required
def add_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        new_bookmark = Bookmark(
            url=form.url.data, 
            description=form.description.data, 
            category=form.category.data, 
            user_id=current_user.id
        )
        db.session.add(new_bookmark)
        db.session.commit()
        flash("Bookmark added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_bookmark.html', form=form)

@app.route("/edit_bookmark/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    if bookmark.user_id != current_user.id:
        flash("You don't have permission to edit this bookmark.", "danger")
        return redirect(url_for('index'))
    
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        bookmark.url = form.url.data
        bookmark.description = form.description.data
        bookmark.category = form.category.data
        db.session.commit()
        flash("Bookmark updated successfully!", "success")
        return redirect(url_for('index'))
    
    return render_template('edit_bookmark.html', form=form, bookmark=bookmark)

@app.route("/delete_bookmark/<int:id>", methods=['GET','POST'])
@login_required
def delete_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    if bookmark.user_id != current_user.id:
        flash("You don't have permission to delete this bookmark.", "danger")
        return redirect(url_for('index'))
    
    db.session.delete(bookmark)
    db.session.commit()
    flash("Bookmark deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
