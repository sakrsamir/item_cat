# Imports
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import *
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os, random, string, datetime, json, httplib2, requests
from functools import wraps

app = Flask(__name__)
 
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "menuapp"



#Connect to database
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

#  Routing
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
# index
@app.route('/')
@app.route('/cat/')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('catalog.html',categories = categories)

# add_category
@app.route('/cat/add/', methods=['GET', 'POST'])
@login_required
def addCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('Category Successfully Added!')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('addcategory.html')


# edit_category
@app.route('/catalog/<path:category_name>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_name):
    editedCategory = session.query(Category).filter_by(name=category_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    creator = session.query(User).filter_by(id=editedCategory.user_id).one()
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    if creator.id != login_session['user_id']:
        flash ("You you don't have right to do that . This right belongs to %s" % creator.name)
        return redirect(url_for('showCatalog'))
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash('Cat item successfully edited')
        return  redirect(url_for('showCatalog'))
    else:
        return render_template('editcategory.html', categories=editedCategory, category = category)

# delete_category
@app.route('/catalog/<path:category_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_name):
    categoryToDelete = session.query(Category).filter_by(name=category_name).one()
    creator = session.query(User).filter_by(id=categoryToDelete.user_id).one()
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    if creator.id != login_session['user_id']:
        flash ("You you don't have right to do that . This right belongs to %s" % creator.name)
    if request.method =='POST':
        session.delete(categoryToDelete)
        session.commit()
        flash('Category Successfully Deleted! '+categoryToDelete.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deletecategory.html', category=categoryToDelete)


# show_items_of_category 
@app.route('/catalog/<path:category_name>/items/')
def showCategory(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category_id=category.id).all()
    return render_template('items.html', category = category, items = items)


# add_item
@app.route('/cat/item/add', methods=['GET', 'POST'])
@login_required
def addItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'],
            description=request.form['description'],
            picture=request.form['picture'],
            category=session.query(Category).filter_by(name=request.form['category']).one(),
            date=datetime.datetime.now(),
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('Item Successfully Added!')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('additem.html', categories=categories)


# delete_item
@app.route('/catalog/<path:category_name>/<path:item_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category_name, item_name):
    delItem = session.query(Items).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    creator = session.query(User).filter_by(id=delItem.user_id).one()
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    if creator.id != login_session['user_id']:
        flash ("You you don't have right to do that . This right belongs to %s" % creator.name)
        return redirect(url_for('showCatalog'))
    if request.method =='POST':
        session.delete(delItem)
        session.commit()
        flash('Item Successfully Deleted! '+delItem.name)
        return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template('deleteitem.html', item=delItem)

# edit_item
@app.route('/catalog/<path:category_name>/<path:item_name>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category_name, item_name):
    editedItem = session.query(Items).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    creator = session.query(User).filter_by(id=editedItem.user_id).one()
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    if creator.id != login_session['user_id']:
        flash ("You you don't have right to do that . This right belongs to %s" % creator.name)
        return redirect(url_for('showCatalog'))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        if request.form['category']:
            category = session.query(Category).filter_by(name=request.form['category']).one()
            editedItem.category = category
        time = datetime.datetime.now()
        editedItem.date = time
        session.add(editedItem)
        session.commit()
        flash('Cat item successfully edited!')
        return  redirect(url_for('showCategory', category_name=editedItem.category.name))
    else:
        return render_template('edititem.html', item=editedItem, categories=categories)

#JSON
@app.route('/catsItems/JSON')
def CatsItemsJSON():
    categories = session.query(Category).all()
    category_sic = [c.serialize for c in categories]
    for c in range(len(category_sic)):
        items = [i.serialize for i in session.query(Items)\
                    .filter_by(category_id=category_sic[c]["id"]).all()]
        if items:
            category_sic[c]["Item"] = items
    return jsonify(Category=category_sic)

@app.route('/cat/JSON')
def catsJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/items/JSON')
def itemsJSON():
    items = session.query(Items).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/cat/<path:category_name>/items/JSON')
def catItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category=category).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/cat/<path:category_name>/<path:item_name>/JSON')
def SpecificItemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Items).filter_by(name=item_name,\
                                        category=category).one()
    return jsonify(item=[item.serialize])




# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("token's user iD doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user = session.query(User).filter_by(email=login_session['email']).one()
    user_id = user.id
    if not user_id:
    	newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
        session.add(newUser)
        session.commit()
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Hi, '
    output += login_session['username']
    output += '!</h1>'
    flash("logged in >>  %s" % login_session['username'])
    return output

# disconnect a connected user.
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = redirect(url_for('showCatalog'))
        flash("You are now logged out.")
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

def login_required(u):
    @wraps(u)
    def x(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return x
# End
if __name__ == '__main__':
    app.secret_key = 'Sakr_Secret_Key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
