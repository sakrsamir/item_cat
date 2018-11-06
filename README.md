# Item Catalog Web App :

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

# Startup :
before using this web app you  have to install flask framework and SQLalchemy using pip and the app imports requests Run sudo pip install requests or follow this steps to get VM with proper environment
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile 
3. Run Vagrant VM (`vagrant up`)
4. Then log into Vagrant VM (`vagrant ssh`)
5. Go to `cd/vagrant`  in terminal
6. Run sudo pip install requests
7. Setup application database with data `python /item-cat/database_init.py`
8. Run application using `python /item-cat/item_project.py`
9. Access app by http://localhost:5000/

# features :
- provide authentication Sign in with google account.
- provide authorization for each resouce.
- provide RESTful APIs with JSON .

# Skills Used
1. Python 
2. Flask framework
3. SQLAlchemy
4. OAuth
5. HTML
6. CSS


# JSON APIS
1.  `/catsItems/JSON`
    - Displays Categories and all items.

2. `/cat/JSON`
    - Displays all categories

3.  `/items/JSON`
    - Displays all items

4.  `/cat/<path:category_name>/items/JSON`
    - Displays items for a specific category.

5.  `/cat/<path:category_name>/<path:item_name>/JSON`
    - Displays a specific item.

# Using Google Login
follow these steps:
1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up 
3. Go to Credentials
4. Select Create Crendentials : OAuth Client ID
5. Select Web application
6. Enter name 'menuapp'
7. Authorized JavaScript origins = 'http://localhost:5000'
8. Authorized redirect URIs = 'http://localhost:5000/login' && 'http://localhost:5000/gconnect'
9.  Click on Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. Then Download JSON file with new name client_secrets.json
13. Move JSON file in item-cat directory 
14. Run application using `python /item-project/app.py`

