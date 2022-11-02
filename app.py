from crypt import methods
from flask import Flask, render_template, request,  redirect, session, jsonify
import mysql.connector
import json
from flask_session import Session

app = Flask(__name__)

app.secret_key = 'login'

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
            session["username"] = username
            session["password"] = password
            mycursor.execute('SELECT COUNT(id) FROM category')
            data = mycursor.fetchall()
            
            #For getting all post count
            postCount = mycursor.execute('SELECT COUNT(id) FROM post')
            mycursor.execute(postCount)
            postCount = mycursor.fetchall()
            return render_template('index.html', output_data = data, post_count = postCount)
        else:
            msg = 'Invalid email or password'
            return render_template('login.html', msg = msg)
    else:
        return render_template('login.html')

#Login page
@app.route('/login')
def logout():
    if session['username']:
        session.pop('username', None)
        session.pop('password', None)
        return redirect('/')
    return redirect('/')

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

ROWS_PER_PAGE = 5
#For getting all categorys
@app.route('/allCategory', methods=['GET','POST'])
def tables():
    mycursor.execute('SELECT * FROM category')
    name = mycursor.fetchall()
    page = request.args.get('page', 1, type=int)
    
    return render_template('allCategory.html', all_category = name , all_subname=all_subname, page=page)

# For edit category
@app.route('/category/edit/<name>', methods=['GET','POST', 'PATCH'])
def edit(name):
    #Select data from category table using category id
    mycursor.execute("SELECT * FROM category where id = '" +name +"'")
    user = mycursor.fetchone()
    #Update data into table
    if request.method == "POST":
        category_name = request.form.get('category_name')
        category_image = request.form.get('image')
        sub_category_name = request.form.get('sub_category')
        sub_category_image = request.form.get('sub_category_image')
        parent = request.form.get('get_value')
        
        query = '''UPDATE category
                SET category_name = %s, category_image = %s, sub_category_name = %s, sub_category_image = %s ,parent = %s   
                WHERE id = %s ''' 
        values =  (category_name, category_image, sub_category_name, sub_category_image, parent, name)
        mycursor.execute(query, values)
        mydb.commit()
    
        return redirect('/allCategory')
    return render_template('edit.html' , user = user, all_name = all_name, name = name)

#For edit sub category
@app.route('/category/editsubcategory/<id>', methods= ['GET', 'POST'])
def editsubcategory(id):
    #Select sub category name, image and parent it form category
    mycursor.execute("SELECT sub_category_name, sub_category_image, parent FROM category WHERE id = '"+ id + "'")
    subcate = mycursor.fetchone()

    #update data into table
    if request.method == 'POST':
        sub_category_name = request.form.get('sub_category')
        sub_category_image = request.form.get('sub_category_image')
        parent = request.form.get('get_value')

        query = '''UPDATE category
                SET sub_category_name = %s, sub_category_image = %s, parent = %s
                WHERE id = %s'''
        values = (sub_category_name, sub_category_image ,parent, id)
        mycursor.execute(query, values)
        mydb.commit()

        return redirect('/allCategory')
    return render_template('editsubcategory.html', subcate = subcate, all_name=all_name, id = id)

#Delete one or more category
@app.route('/moredelete', methods= ['POST', 'GET'])
def moredelete():
    if request.method == 'POST':
        for gt in request.form.getlist('clinic_info'):
            print(gt)
            mycursor.execute("DELETE FROM category WHERE id = {0}" .format(gt))
            mydb.commit()
    return redirect('/allCategory')

#Delete one or more post
@app.route("/deletemorepost", methods=['POST', 'GET'])
def deletemorepost():
    if request.method == 'POST':
        for gt1 in request.form.getlist('clinic_info1'):
            mycursor.execute("DELETE FROM post WHERE id = {0}" .format(gt1))
            mydb.commit()
    return redirect('/allPost')

#For delete category
@app.route('/category/delete/<name>', methods=['GET','POST'])
def delete(name):
    #Delete data from category table using category id
    mycursor.execute('DELETE FROM category WHERE id = %s',[name])
    delete =  mycursor.fetchall()
    mydb.commit()
    return redirect('/allCategory')

#For delete sub category
@app.route('/category/deletesubcategory/<id>')
def deletesubcategory(id):
    #Delete sub category data from category using id
    sub_category_name = 'NULL'
    sub_category_image = 'NULL'
    parent = 0

    query = '''UPDATE category
            SET sub_category_name = %s, sub_category_image = %s, parent = %s
            WHERE id = %s'''
    values = (sub_category_name, sub_category_image, parent,id)
    mycursor.execute(query, values)
    mydb.commit()
    return redirect('/allCategory')

#All post template
@app.route('/allPost')
def allPost():
    #For getting all post names
    all_post = mycursor.execute('SELECT post, id FROM post')
    mycursor.execute(all_post)
    all_post = mycursor.fetchall()

    return render_template('allPost.html' , all_post = all_post)

#For delete post
@app.route('/post/delete/<post>', methods=['GET','POST'])
def deletePost(post):
    #Delete row form post table using post id
    mycursor.execute('DELETE FROM post WHERE id = %s', [post])
    deletePost =  mycursor.fetchall()
    mydb.commit()

    return redirect('/allPost')

#For edit post
@app.route('/post/edit/<post>', methods=['GET','POST'])
def editPost(post):
    mycursor.execute("SELECT * FROM post where id = '" +post +"'")
    edit_post =  mycursor.fetchone()
    #Update data
    if (request.method == 'POST'):
        post = request.form.get('post_name')
        post_image = request.form.get('post_image')
        description = request.form.get('description')
        parent = request.form.get('clinic_info1')
        print(post)

        querys = '''UPDATE post
                SET post = %s, post_image = %s, description = %s, category_parent = %s
                WHERE id = %s '''
        valuess = (post, post_image, description, parent, post)
        mycursor.execute(querys, valuess)
        mydb.commit()

        return redirect('/allPost')
    return render_template('editPost.html', edit_post = edit_post, all_name = all_name)


#For getting all category names
all_name = mycursor.execute('SELECT category_name, id, sub_category_name FROM category')
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

        mycursor.execute('insert into category (category_name, category_image, sub_category_name,  sub_category_image, parent) values(%s, %s, %s, %s, %s)', (category_name, category_image, sub_category_name, sub_category_image, parent))
        mydb.commit()
        
        return redirect('/category')
    return render_template('category.html', all_name = all_name, all_subname=all_subname)


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
        return render_template('category.html', all_name = all_name)
    return render_template('category.html', all_name = all_name)


#For getting all values of category table
all_subname = mycursor.execute('SELECT * FROM category')
mycursor.execute(all_subname)
all_subname = mycursor.fetchall()

#Post template
@app.route('/post', methods=['GET', 'POST'])
def post():
    #Insert post values
    if (request.method == 'POST'):
        post = request.form.get('post_name')
        post_image = request.form.get('post_image')
        description = request.form.get('description')
        parent = request.form.getlist('get_value1')
        
        t = []
        for i in parent:
            a = i
            t.append(a)
        
        ta = str(t)
        print(t)
        mycursor.execute('insert into post (post, post_image, description, category_parent) values(%s, %s, %s,%s)', (post, post_image, description, ta))
        mydb.commit()
        
        return render_template('post.html', all_name = all_name, all_subname = all_subname)
    return render_template('post.html', all_name = all_name)

#Profile template
@app.route('/profile')
def profile():
    return render_template('profile.html')

#end of code to run it
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)