from turtle import pos
from flask import Flask, render_template, request,  redirect, session, jsonify
import mysql.connector
import json

# from sqlalchemy import all_
# with open('config.json', 'r') as c:
#     params = json.load(c)["params"]

# local_server = True

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="blogWeb"
)

mycursor = mydb.cursor()

#Home page
@app.route('/', methods=['GET', 'POST'])
def login():
    #Get user input
    if request.method == 'POST':
        username = request.form.get("email")
        password = request.form.get("pass")

        #Check input username and password
        if (username == 'krishnapal.starwebindia@gmail.com' and password == '123456'):
            mycursor.execute('SELECT COUNT(id) FROM category')
            data = mycursor.fetchall()
            
            #For getting all post count
            postCount = mycursor.execute('SELECT COUNT(id) FROM post')
            mycursor.execute(postCount)
            postCount = mycursor.fetchall()
            return render_template('index.html', output_data = data, post_count = postCount)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

#Login page
@app.route('/login')
def logout():
    return render_template('login.html')

#Deshbord
@app.route('/index', methods=['GET','POST'])
def index():
    #For getting all category count
    mycursor.execute('SELECT COUNT(id) FROM category')
    data = mycursor.fetchall()
    
    #For getting all post count
    postCount = mycursor.execute('SELECT COUNT(id) FROM post')
    mycursor.execute(postCount)
    postCount = mycursor.fetchall()
    return render_template('index.html', output_data = data, post_count = postCount)


#For getting all categorys
@app.route('/allCategory', methods=['GET','POST'])
def tables():
    mycursor.execute('SELECT * FROM category')
    name = mycursor.fetchall()

    return render_template('allCategory.html', all_category = name )

# For edit category
@app.route('/category/edit/<int:name>', methods=['GET','POST'])
def edit(name):
    #Select data from category table using category id
    Data = mycursor.execute('SELECT * FROM category where id = %s ', [name])
    mycursor.execute(Data)
    user = mycursor.fetchone()

    #Update data into table
    if (request.method == "POST"):
        category_name = request.form.get('category_name')
        category_image = request.form.get('image')
        sub_category_name = request.form.get('sub_category')
        sub_category_image = request.form.get('sub_category_image')
        parent = request.form.get('get_value')

        mycursor.execute('UPDATE category SET(category_name, category_image, sub_category_name, sub_category_image) values(%s, %s, %s, %s, %s) ' , (category_name, category_image, sub_category_name, sub_category_image,parent))
        mydb.commit()
        
        return render_template('allCategory.html', user = user, all_name = all_name )
    return render_template('edit.html' , user=user, all_name = all_name)

#For delete category
@app.route('/category/delete/<string:name>', methods=['GET','POST'])
def delete(name):
    #Delete data from category table using category id
    mycursor.execute('DELETE FROM category WHERE id = %s',[name])
    delete =  mycursor.fetchone()
    mydb.commit()

    return render_template('allCategory.html', delete = delete , all_name = all_name)


#All post template
@app.route('/allPost')
def allPost():
    #For getting all post names
    all_post = mycursor.execute('SELECT post, id FROM post')
    mycursor.execute(all_post)
    all_post = mycursor.fetchall()

    return render_template('allPost.html' , all_post = all_post)

#For delete post
@app.route('/post/delete/<string:post>', methods=['GET','POST'])
def deletePost(post):
    #Delete row form post table using post id
    mycursor.execute('DELETE FROM post WHERE id = %s', post)
    deletePost =  mycursor.fetchall()
    mydb.commit()

    return render_template('allPost.html', deletePost = deletePost)

#For edit post
@app.route('/post/edit/<string:post>', methods=['GET','POST'])
def editPost(post):
    #Select values from post table using post id
    editPost = mycursor.execute('SELECT * FROM post WHERE id = %s',[post])
    mycursor.execute(editPost)
    edit_post =  mycursor.fetchone()

    #Update data
    if (request.method == 'POST'):
        post = request.form.get('post_name')
        post_image = request.form.get('post_image')
        description = request.form.get('description')
        parent = request.form.get('get_Value')

        mycursor.execute('insert into post (post, post_image, description, parent) values(%s, %s, %s, %s)', (post, post_image, description, parent))
        mydb.commit()

        return render_template('editPost.html', edit_post = edit_post ,all_name = all_name)
    return render_template('editPost.html', edit_post = edit_post, all_name = all_name)


#For getting all category names
all_name = mycursor.execute('SELECT category_name, id FROM category')
mycursor.execute(all_name)
all_name = mycursor.fetchall()

#Category template
@app.route('/category', methods = ['GET', 'POST'])
def category():
    #Insert values in the coulmn of category
    if (request.method == 'POST'):
        category_name = request.form.get('category_name')
        category_image = request.form.get('image')
        sub_category_name = request.form.get('sub_category')
        sub_category_image = request.form.get('sub_category_image')
        parent = request.form.get('get_value')

        mycursor.execute('insert into category (category_name, category_image, sub_category_name,  sub_category_image,category_parent) values(%s, %s, %s, %s, %s)', (category_name, category_image, sub_category_name, sub_category_image, parent))
        mydb.commit()
        # mycursor.close()
        
        return render_template('category.html', all_name = all_name)
    return render_template('category.html', all_name = all_name)


#Insert sub categorys using parent category id
@app.route('/insert', methods=['POST', 'GET'])
def insert():
    #Inserting values
    if request.method=='POST':
        sub_category_name = request.form.get('sub_category')
        sub_category_image = request.form.get('sub_category_image')
        parent = request.form.get('get_value')
        id  = request.form.get('get_Value')
        mycursor.execute('INSERT INTO category (sub_category_name, sub_category_image, parent) values(%s, %s, %s) WHERE id = %s' ,(sub_category_name, sub_category_image, parent, parent))
        mydb.commit()
        return render_template('category.html', all_name = all_name, id=id)
    return render_template('category.html', all_name = all_name , id=id)


#Post template
@app.route('/post', methods=['GET', 'POST'])
def post():
    #Insert post values
    if (request.method == 'POST'):
        post = request.form.get('post_name')
        post_image = request.form.get('post_image')
        description = request.form.get('description')
        parent = request.form.get('get_value')

        mycursor.execute('insert into post (post, post_image, description,category_parent) values(%s, %s, %s,%s)', (post, post_image, description, parent))
        mydb.commit()
        
        return render_template('post.html', all_name = all_name)
    return render_template('post.html', all_name = all_name)

#Profile template
@app.route('/profile')
def profile():
    return render_template('profile.html')

#end of code to run it
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)