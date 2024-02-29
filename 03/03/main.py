from flask import Flask, redirect, url_for, session, request, render_template
from settings import *
from db_scripts import *

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = getUser()
    return render_template('about.html', user=user)

@app.route('/post/category/<category_name>', methods=['POST', 'GET'])
def postCategory(category_name):
    category_id = getIdByCategory(category_name)
    errors = []

    if request.method == 'POST':

        if request.form['title'] == '':
            errors.append('Заголовок не може бути порожнім!')

        if request.form['post'] == '':
            errors.append('Текст не може бути порожнім!')

        filename = None
        if request.files['image'].filename != '':
            print('POPITKA!', request.files['image'])
            image = request.files['image']
            image.save(f"{PATH_UPLOADS}{image.filename}")
            filename = image.filename   

        if len(errors) == 0:
            addPost(request.form['category_id'], request.form['post'], request.form['title'], filename)

    posts = getPostsByCategory(category_name)

    return render_template('post_category.html', category_name=category_name, posts=posts, category_id=category_id, errors=errors)

@app.route('/post/delete/<post_id>/<category_name>')
def deletePost(post_id, category_name):
    delPost(post_id)
    return redirect(f'/post/category/{category_name}')

@app.route('/post/view')
def postView():
    return '<h1>post View</h1>'

@app.route('/about')
def about():
    return '<h1>About</h1>'

app.config['SECRET_KEY'] = 'VeryStrongKey'

if __name__ == '__main__':
    app.run(debug=True, port=5000)