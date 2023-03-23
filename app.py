from flask import Flask, render_template, request, flash, session, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# ALLOWED_MEDIA_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'ogg', 'webm'}
# IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# VIDEO_EXTENSIONS = {'mp4', 'ogg', 'webm'}
# ALLOWED_OBJ_EXTENSIONS = {'obj'}
# UPLOAD_FOLDER = '/home/max66778/mysite/static/'
# UPLOAD_FOLDER = 'static/'
PSW_HASH = 'pbkdf2:sha256:260000$NlYgVqtVblDaBLXU$09d0433d6e4851fe37fbb2fa4f20a2221142929278f9d676d90c333a14cac13f'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fwihf9fghhjdyhtrrwwsc;iolu348fhr9h9hc023ecn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    msg = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<users {self.id}>'


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    cover_id = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(150), nullable=False)
    images_id = db.Column(db.Text, nullable=False)
    videos_id = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    obj_id = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Projects {self.id}>'


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/portfolio')
def portfolio():
    if Projects.query.all():
        projs = Projects.query.order_by(Projects.id.desc()).all()
        items = []
        for item in projs:
            items.append([item.id, item.title, item.cover_id, item.short])
        # print(items)

        return render_template('portfolio.html', title='Portfolio', items=items)

    return render_template('portfolio.html', title='Portfolio')


@app.route('/item-page/<project>')
def item_page(project):
    if request.method == 'GET':
        try:
            item = Projects.query.filter(Projects.id == project).first()
            images = [img for img in item.images_id.split('|')]
            videos = [vid for vid in item.videos_id.split('|')]
            objs = [obj for obj in item.obj_id.split('|')]
            # video = [vid for vid in item.media_id.split('|')]
            # images = [img for img in item.media_id.split('|')]
            # images = [img for img in item.media_url.split('|') if img.split('.')[-1].lower() in IMAGE_EXTENSIONS]
            # video = [vid for vid in item.media_url.split('|') if vid.split('.')[-1].lower() in VIDEO_EXTENSIONS]
            # objs = [obj for obj in item.obj_url.split('|')]
            return render_template('item_page.html',
                                   title=item.title,
                                   item=item,
                                   images=images,
                                   videos=videos,
                                   objs=objs)
        except Exception as e:
            print(e)
            return redirect('/portfolio')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/resume')
def resume():
    return render_template('resume.html', title='Resume')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    res = Comments.query.order_by(Comments.id.desc()).limit(10).all()

    if request.cookies.get('commented'):
        return render_template('feedback.html', title='Feedback', comments=res, isComm=True)
    else:
        if request.method == 'POST':
            try:
                comm = Comments(name=request.form['name'], email=request.form['email'], msg=request.form['msg'])
                db.session.add(comm)
                db.session.commit()
                flash('Commented successfully', 'success')
                res = Comments.query.order_by(Comments.id.desc()).limit(10).all()
                result = make_response(render_template('feedback.html', title='Feedback', comments=res, isComm=True))
                result.set_cookie('commented', '1', 30*24*3600)
                return result

            except Exception as e:
                db.session.rollback()
                flash('Commenting error', 'error')
                print('DB adding error', e)

    return render_template('feedback.html', title='Feedback', comments=res, isComm=False)


@app.route('/comments_manage', methods=['POST', 'GET'])
def comments_manage():
    if not isLogged():
        return redirect('/login')

    res = Comments.query.order_by(Comments.id.desc()).all()
    return render_template('comments_manage.html', title='Feedback', comments=res)


@app.route('/delete_comment/<comm_id>', methods=['GET'])
def delete_comment(comm_id):
    if not isLogged():
        return redirect('/login')

    if request.method == 'GET':
        try:
            Comments.query.filter(Comments.id == comm_id).delete()
            db.session.commit()

            flash('Comment deleted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Comment deleting error', 'error')
            print('DB deleting error', e)

    return redirect('/comments_manage')


@app.route('/my_account')
def admin_index():
    if not isLogged():
        return redirect('/login')

    return render_template('admin_index.html', title='Admin Home')


@app.route('/add_project', methods=['POST', 'GET'])
def add_project():
    if not isLogged():
        return redirect('/login')

    if request.method == 'POST':
        try:
            cover_id = request.form['cover'][32:-20]
            images_id = request.form['images'].replace(' ', '|').split('|')
            images_id = [form[32:-20] for form in images_id]
            videos_id = request.form['videos'].replace(' ', '|').split('|')
            videos_id = [form[32:-20] for form in videos_id]

            # print(media_id)
            obj_id = request.form['object'].replace(' ', '|').split('|')
            obj_id = [form[32:-20] for form in obj_id]
            # print(obj_id)
            # approved_media_files = []
            # approved_obj_files = []
            # media_iterations = 1
            # obj_iterations = 1



            # if Projects.query.all():
            #     proj_id = Projects.query.order_by(Projects.id.desc()).limit(1).all()[0].id

            #
            #     cover_url = f'{proj_id+1}.{cover_file.filename.split(".")[-1].lower()}'
            #     cover_file.save(f'{UPLOAD_FOLDER}covers/{cover_url.lower()}')
            #
            #     for file in media_files:
            #         approved_media_files.append(f'{proj_id+1}_{media_iterations}.{file.filename.split(".")[-1].lower()}')
            #         file.save(f'{UPLOAD_FOLDER}media/{proj_id+1}_{media_iterations}.{file.filename.split(".")[-1].lower()}')
            #         media_iterations += 1
            #
            #     for file in obj_files:
            #         approved_obj_files.append(f'{proj_id+1}_{obj_iterations}.{file.filename.split(".")[-1].lower()}')
            #         file.save(f'{UPLOAD_FOLDER}objs/{proj_id+1}_{obj_iterations}.{file.filename.split(".")[-1].lower()}')
            #         obj_iterations += 1
            #
            # else:
            #     cover_url = f'1.{cover_file.filename.split(".")[-1].lower()}'
            #     cover_file.save(f'{UPLOAD_FOLDER}covers/{cover_url.lower()}')
            #
            #     for file in media_files:
            #         approved_media_files.append(f'1_{media_iterations}.{file.filename.split(".")[-1].lower()}')
            #         file.save(f'{UPLOAD_FOLDER}media/1_{media_iterations}.{file.filename.split(".")[-1].lower()}')
            #         media_iterations += 1
            #
            #     for file in obj_files:
            #         approved_obj_files.append(f'1_{obj_iterations}.{file.filename.split(".")[-1].lower()}')
            #         file.save(f'{UPLOAD_FOLDER}objs/1_{obj_iterations}.{file.filename.split(".")[-1].lower()}')
            #         obj_iterations += 1

            item = Projects(title=request.form['title'],
                            cover_id=cover_id,
                            short=request.form['short'],
                            images_id='|'.join(images_id),
                            videos_id='|'.join(videos_id),
                            description=request.form['description'],
                            obj_id='|'.join(obj_id))

            db.session.add(item)
            db.session.commit()

            flash('New project added to your portfolio successfully', 'success')

        except Exception as e:
            db.session.rollback()
            flash('Project adding error', 'error')
            print('DB adding error', e)

    return render_template('add_project.html', title='Add Project')


@app.route('/projects_manage', methods=['GET'])
def projects_manage():
    if not isLogged():
        return redirect('/login')

    if Projects.query.all():
        projs = Projects.query.order_by(Projects.id.desc()).all()
        items = []
        for item in projs:
            items.append([item.id, item.title, item.cover_id, item.short])
        print(items)

        return render_template('projects_manage.html', title='Projects manage', items=items)

    else:
        return render_template('projects_manage.html', title='Projects manage')


@app.route('/delete_card/<item_id>', methods=['POST', 'GET'])
def delete_card(item_id):
    if not isLogged():
        return redirect('/login')

    if request.method == 'GET':
        try:
            # cover_id = Projects.query.filter(Projects.id == item_id).first().cover_id
            # media_id = Projects.query.filter(Projects.id == item_id).first().media_id.split(' ')
            # obj_id = Projects.query.filter(Projects.id == item_id).first().obj_id.split(' ')
            # os.remove(f'{UPLOAD_FOLDER}covers/{cover_url}')
            # for media_file in media_id:
            #     os.remove(f'{UPLOAD_FOLDER}media/{media_file}')
            # for obj_file in obj_id:
            #     os.remove(f'{UPLOAD_FOLDER}objs/{obj_file}')
            #print(cover_url, media_url, obj_url)
            Projects.query.filter(Projects.id == item_id).delete()
            db.session.commit()

            flash('Project deleted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Project deleting error', 'error')
            print('DB removing error', e)

    return redirect('/projects_manage')


@app.route('/edit_page/<item_id>', methods=['POST', 'GET'])
def edit_page(item_id):
    if not isLogged():
        return redirect('/login')

    if request.method == 'GET':
        try:
            item = Projects.query.filter(Projects.id == item_id).first()
            images = [img for img in item.images_id.split('|')]
            videos = [vid for vid in item.videos_id.split('|')]
            objs = [obj for obj in item.obj_id.split('|')]

            return render_template('edit_page.html',
                                   title=item.title,
                                   item=item,
                                   images=images,
                                   videos=videos,
                                   objs=objs)

        except Exception as e:
            print(e)
            return redirect('/projects_manage')

    if request.method == 'POST':
        try:
            item = Projects.query.filter(Projects.id == item_id).first()
            item.title = request.form['title']
            item.description = request.form['desc']
            item.short = request.form['short']
            db.session.commit()

            flash('Project updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Project updating error', 'error')
            print('DB updating error', e)

        return redirect('/projects_manage')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if isLogged():
        return redirect('/my_account')

    if request.method == 'POST':
        if request.form['user'] == 'admin' and check_password_hash(PSW_HASH, request.form['psw']):
            login_admin()
            return redirect('/my_account')
        else:
            flash('Incorrect login or password.', 'error')

    return render_template('login.html', title='Admin panel')


@app.route('/logout')
def logout():
    if not isLogged():
        return redirect('/login')

    logout_admin()

    return redirect('/login')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found'), 404


if __name__ == '__main__':
    app.run(debug=True)