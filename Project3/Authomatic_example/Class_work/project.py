from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
session = DBSession()

# JSON list all items
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

# JSOn list only one item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:MenuID>/JSON')
def singleMenuJSON(restaurant_id, MenuID):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    items = session.query(MenuItem).filter_by(id=MenuID).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu item created !")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant=restaurant, restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter_by(id=MenuID).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Changed saved !")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, MenuID=MenuID, item=editedItem)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, MenuID):
    deletedItem = session.query(MenuItem).filter_by(id=MenuID).one()
    print MenuID
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Item deleted !")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, MenuID=MenuID, item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
