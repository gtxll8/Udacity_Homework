# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the CRUDs are done

import os
import sys
from urlparse import urljoin

from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, jsonify, request, redirect, url_for, \
    send_from_directory, make_response, g
from config import CONFIG
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Users, Base, SaleItem
from flask.ext.login import AnonymousUserMixin, LoginManager, UserMixin, login_user, logout_user, \
    current_user, login_required
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.contrib.atom import AtomFeed
import logging
from logging.handlers import RotatingFileHandler
from flask.ext.seasurf import SeaSurf

applicationPath = '/var/www/FlaskApp/FlaskApp'
if applicationPath not in sys.path:
    sys.path.insert(0, applicationPath)

os.chdir(applicationPath)

# Initialize the Flask application
app = Flask(__name__)

# CSRF Protection with Flask seaSurf
# https://flask-seasurf.readthedocs.org/en/latest/
# passing your application object back to the extension
csrf = SeaSurf(app)
# initialize
csrf.init_app(app)

# if you want to use sessions this needs to be set
# to a real secret key !
app.secret_key = '211219898SPKIREW12'

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'development', report_errors=False)
# This is the path to the upload directory
UPLOAD_FOLDER = './static'
# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# Upload folder path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# db location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/FlaskApp/FlaskApp/salesite.db'
# create instance of the salesite.db
engine = create_engine('sqlite:///./salesite.db', connect_args={'check_same_thread':False}) 
# Bind the engine to the metadata of the Base class so that the
# declarative can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
session = DBSession()

# JSON list all items in a category
@app.route('/forsale/<category_name>/JSON')
def forsaleCategoriesJSON(category_name):
    items = session.query(SaleItem).filter_by(category_name=category_name).all()
    return jsonify(SaleItem=[i.serialize for i in items])


# JSOn list items from only one user
@app.route('/forsale/<user_name>/user/JSON')
def forsaleByUserJSON(user_name):
    items = session.query(SaleItem).filter_by(user_name=user_name).all()
    return jsonify(SaleItem=[i.serialize for i in items])


# This is to create an external url
# useful in the RSS feed below
def make_external(url):
    return urljoin(request.url_root, url)


# RSS feeds using AtomFeed
@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Items',
                    feed_url=request.url, url=request.url_root)
    articles = session.query(SaleItem).order_by(desc(SaleItem.last_updated)).all()
    for article in articles:
        feed.add(article.name, unicode(article.description),
                 content_type='html',
                 author=article.name,
                 url=make_external('/forsale/%s/single_item' % article.id),
                 updated=article.last_updated,
                 published=article.last_updated)
    return feed.get_response()


# When there is no user logged in use the 'Guest' account
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = 'Guest'
        self.social_id = 0

# Using flask.ext.login to manage authentication
# for that we need to setup the variables
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = Anonymous


# Load users
class User(UserMixin):
    def __init__(self, user_id, name, social_id, active=True):
        self.id = user_id
        self.name = name
        self.social_id = social_id
        self.active = active

    def is_authenticated(self):
        return True
        # return true if user is authenticated, provided credentials

    def is_active(self):
        return True
        # return true if user is active and authenticated

    def is_annonymous(self):
        return False
        # return true if Annonymous, actual user return false

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


@login_manager.user_loader
def load_user(id):
    # 1. Fetch against the database a user by `id`
    # 2. Create a new object of `User` class and return it.
    # 3. If nothing found return None
    u = session.query(Users).filter_by(id=id).first()
    if u:
        return User(u.id, u.name, u.social_id)
        g.user = current_user
    else:
        return None


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Login form to test the login credentials we are using authomatic
# library to manage that, see code in the login.htm
@app.route('/login_test')
def login_test():
    return render_template('login_test.html')


# Home route
@app.route('/')
def index():
    items = session.query(SaleItem).order_by(desc(SaleItem.id)).all()
    return render_template('index.html', items=items)


# Login handler, must accept both GET and POST to be able to use OpenID.
# note that we also use csrf.include to implement Flask-SeaSurf
@csrf.include
@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    # We need response object for the WerkzeugAdapter.
    response = make_response()

    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            print 'user updated'
            # We need to update the user to get more info.
            result.user.update()
            # Check if this user is already in db
            user = session.query(Users).filter_by(social_id=result.user.id).first()
            if user:
                u = User(user.id, user.name, user.social_id)
                login_user(u)
                # If account exist, greet the user
                if current_user.is_authenticated():
                    flash('Welcome back: %s' % current_user.name)
                # Debug print / turn off for production
                print current_user.name
                print current_user.id
                flash("You are now logged into your profile!")
                print "already registered"

            else:
                # Otherwise create a new user account
                new_user = Users(social_id=result.user.id, name=result.user.name)
                session.add(new_user)
                session.commit()
                flash("New user account added !")
                flash("Welcome: %s !" % new_user.name)
                user = session.query(Users).filter_by(social_id=result.user.id).first()
                u = User(user.id, user.name, user.social_id)
                login_user(u)

        # The rest happens inside the login.html template.
        return render_template('login.html', result=result, email=result.user.email)

    # Don't forget to return the response.
    return response


# Logout current user using flask's LoginManager
@app.route('/logout')
@login_required
def logout():
    # get the current user logged in to use it when you say 'bye'
    user = g.user
    # logout current user
    logout_user()
    # following used only in Debug, turn off when in production
    print user.name, user.social_id
    print "logged out!"
    flash("You are now logged out!")
    items = session.query(SaleItem).all()
    # redirect Guest to main page
    return render_template('index.html', items=items)


# Update global user before request in order
# to cache it for further use
@app.before_request
def before_request():
    g.user = current_user
    g.search_form = SearchForm()
    print g.user


# Route that will process the file upload
@csrf.include
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basically show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))


# Add new image to product
@csrf.include
@app.route('/forsale/<int:user_id>/<int:item_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_file(item_id, user_id):
    if request.method == 'POST':
        file = request.files['file']
        # check if the file extension is an allowed one
        if file and allowed_file(file.filename):
            # Using secure here to prevent any security issues that may
            # appear if user is trying to inject malicious code in the request form
            # for the file's path
            filename = secure_filename(file.filename)
            # save file in teh static folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            editedItem = session.query(SaleItem).filter_by(id=item_id).one()
            # replace spaces with underscores in teh file's name
            editedItem.image_name = file.filename.replace(" ", "_")
            session.add(editedItem)
            session.commit()
            flash("New image added !")
            return redirect(url_for('sellerPage', user_id=user_id))


# Used to browse an image file from teh static directory
@app.route('/static/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# Add new items
@csrf.include
@app.route('/')
@app.route('/forsale/<user_id>/new', methods=['GET', 'POST'])
@login_required
def newSaleItem(user_id):
    user = session.query(Users).filter_by(id=user_id).first()
    if request.method == 'POST':
        # first add the item's details in the database
        newItem = SaleItem(name=request.form['name'], description=request.form['description'],
                           price=request.form['price'], image_name='', user_id=user_id, user_name=user.name,
                           contact=request.form['contact'], category_name=request.form['category'], last_updated=None)
        session.add(newItem)
        session.commit()
        flash("New sale item created !")
        item = session.query(SaleItem).order_by(SaleItem.id.desc()).first()
        # the if there is an image file for the product upload it to
        # the static folder and add the image name in the db.
        # This way we are not storing them directly in the db
        file = request.files['file']
        if file and allowed_file(file.filename):
            # clean path string with secure_filename
            filename = secure_filename(file.filename)
            # save file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # get the item details
            editedItem = session.query(SaleItem).filter_by(id=item.id).one()
            # replace teh blank spaces in the name and add it to the image_name column
            editedItem.image_name = file.filename.replace(" ", "_")
            session.add(editedItem)
            session.commit()
            flash("New image added !")
            # all good redirect to teh seller's admin page
        return redirect(url_for('sellerPage', user_id=user_id))
    else:
        return render_template('newitem.html', user=user, user_id=user_id)


# Edit items
@csrf.include
@app.route('/')
@app.route('/forsale/<int:user_id>/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(user_id, item_id):
    user = session.query(Users).filter_by(id=user_id).first()
    editeditem = session.query(SaleItem).filter_by(id=item_id).one()
    # get all the forms values
    if request.method == 'POST':
        if request.form['name']:
            editeditem.name = request.form['name']
        if request.form['category']:
            editeditem.category_name = request.form['category']
        if request.form['description']:
            editeditem.description = request.form['description']
        if request.form['contact']:
            editeditem.contact = request.form['contact']
        if request.form['price']:
            editeditem.price = request.form['price']
        # update teh item with the new changes, if any
        session.add(editeditem)
        session.commit()
        flash("Change saved !")
        # if user had uploaded a new image file, search for the old
        # file and delete it before adding the new one
        product_file = request.files['file']
        if product_file and allowed_file(product_file.filename):
            # Remove the old image file from folder
            if editeditem.image_name and os.path.isfile(
                    os.path.join(app.config['UPLOAD_FOLDER'], editeditem.image_name)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], editeditem.image_name))
            # add the new one here, after cleaning the path string
            filename = secure_filename(product_file.filename)
            product_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # make sure file name does not have any spaces
            editeditem.image_name = product_file.filename.replace(" ", "_")
            # add the replacing image to the item
            session.add(editeditem)
            session.commit()
            flash("New image added !")
            # all good redirect to teh seller's admin page
        return redirect(url_for('sellerPage', user_id=user_id))
    else:
        return render_template('edititem.html', user=user, user_id=user_id, item=editeditem)


# Delete items
@csrf.include
@app.route('/forsale/<user_id>/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(user_id, item_id):
    deletedItem = session.query(SaleItem).filter_by(id=item_id).one()
    item = session.query(SaleItem).filter_by(id=item_id).one()
    print item_id
    if request.method == 'POST':
        # delete the file from the upload folder too
        if item.image_name and os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], item.image_name)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.image_name))
        session.delete(deletedItem)
        session.commit()
        flash("Item deleted !")
        # redirect back to the user's admin page
        return redirect(url_for('sellerPage', user_id=user_id))
    else:
        return render_template('deleteitem.html', user_id=user_id, item_id=item_id, item=deletedItem)


# Delete user account
@csrf.include
@app.route('/admin/<user_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteAccount(user_id):
    deletedItems = session.query(SaleItem).filter_by(user_id=user_id).all()
    user = session.query(Users).filter_by(id=user_id).first()
    if request.method == 'POST':
        # delete all the files from the upload folder too !
        for item in deletedItems:
            # check if the file is present in the static directory
            if item.image_name and os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], item.image_name)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.image_name))
                session.delete(item)
        # find the user and delete the record
        session.query(Users).filter(Users.id == user_id).delete()
        session.commit()
        flash("Your account has been deleteded !")
        items = session.query(SaleItem).all()
        # since there is not a user logged in redirect to the main page
        render_template('index.html', items=items)
    else:
        return render_template('deleteaccount.html', user_id=user_id, user_name=user.name)
    # make sure you logout the user or an error will be raised
    items = session.query(SaleItem).all()
    logout_user()
    # redirect to hom epage
    return render_template('index.html', items=items)


# Return single item
@csrf.include
@app.route('/forsale/<int:item_id>/single_item', methods=['GET', 'POST'])
def singleItem(item_id):
    items = session.query(SaleItem).filter_by(id=item_id).all()
    return render_template('index.html', items=items)


# Main seller's page
@app.route('/admin/')
@login_required
def sellerPage():
    # return user's id and teh items for that user
    user = session.query(Users).filter_by(id=g.user.id).first()
    items = session.query(SaleItem).order_by(desc(SaleItem.id)).filter_by(user_id=g.user.id)
    return render_template('seller_page.html', user=user, items=items)


# Category showing
@csrf.include
@app.route('/category/<category_name>/', methods=['GET', 'POST'])
def showCategory(category_name):
    # find all the items on a certain category
    items = session.query(SaleItem).filter_by(category_name=category_name).all()
    return render_template('index.html', items=items)


# This is needed it so you can pass the search value from the base template
# , using global g.search_form to get it in the searchWord() def. Note
# we use Flask-WTF here, which by default is CSRF proofed
class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


# Simple search; the searched word is used for querying description field in sale_item
@csrf.exempt
@app.route('/search', methods=['GET', 'POST'])
def searchWord():
    items = session.query(SaleItem).all()
    if request.method == 'POST':
        items = session.query(SaleItem).filter(SaleItem.description.like('%' + request.form['search'] + '%')).all()
        # check if any results returned and flash messages accordingly
        items_count = len(items)
        if items_count:
            flash("Your search returned %s results" % items_count)
        else:
            flash("Your search returned no results")
        return render_template('index.html', items=items)
    # return teh results in the main page
    return render_template('index.html', items=items)


@login_manager.unauthorized_handler
def unauthorized():
    # in case Guest user is trying to access resources which are meant for logged in
    # users only then warn user that it needs to be logged in.
    items = session.query(SaleItem).all()
    flash("Hello Guest, you need to login!")
    return render_template('index.html', items=items)


# 404 page error handling , give user some viable helping choices
@app.errorhandler(404)
def page_not_found(e):
    # Logging this error in the log file (example implementing logging)
    app.logger.error('404 error occurred')
    return render_template('doesnotexist.html'), 404


if __name__ == '__main__':
    app.debug = True
    # This can be used as default implementation for logs
    # Flask does not perform any logging by default
    handler = RotatingFileHandler('setup_logging.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    app.logger.addHandler(handler)
    # test-environment
    # app.run(host='0.0.0.0', port=8080)
    # production
    app.run(host='127.0.0.1')
