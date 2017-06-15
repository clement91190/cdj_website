from server import app, db
from flask import render_template, session, url_for, redirect, request, flash, Response
import functools
from models import Entry, User


@app.route('/test', methods=['POST', 'GET'])
def test():
    return "Hello World"


@app.route('/', methods=['POST', 'GET'])
def main():
    recent_posts = Entry.objects.order_by('-timestamp')[:5]
    posts_authors= []
    for i in range (0, min(5, len(recent_posts))):
        posts_authors.append(','.join(recent_posts[i].get_author_names()))
    print recent_posts
    return render_template('index.html', recent_posts=recent_posts, posts_authors=posts_authors , max_index=min(5, len(recent_posts)))


@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path)) #'url_for' generates an URL to 'login' while passing the following arguments (here, 'next') 
    return inner											 #through the generated URL

@app.route('/dummy')
def create_dummy():
    if not User.userExists('Aaa'):
        dummy=User(username='Aaa', password='pwd', email='dumdum@dummail.com')
        dummy.save()
    return redirect(url_for('login'))

@app.route('/nodummy')
def delete_dummy():
    try:
        User.objects(username='Aaa').get().delete()
        return redirect(url_for('logout'))
    except DoesNotExist:
        return redirect(url_for('logout'))

@app.route('/database')
def print_db():
    print(User._get_db())
    print(app.config['MONGODB_SETTINGS'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') #or request.form.get('next') #Retrieves the next page to serve after successful login from the QUERY STRING (after the '?')
    if request.method == 'POST' and request.form.get('password') and request.form.get('username'):	#in the URL
        password = request.form.get('password')
        username = request.form.get('username')
        user = User.checkCredentials(username, password)
        if user:
            session['logged_in'] = True
            session['user'] = user
            # session.permanent = True  # Use cookie to store session.
            flash('You are now logged in as '+user.username, 'success')
            return redirect(next_url or url_for('main'))
        else:
            flash('Incorrect credentials', 'danger')
    return render_template('login.html', next_url=next_url)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            user=session['user']
            entry = Entry(
                title=request.form['title'],
                content=request.form['content'],
                published=request.form.get('published') or False,
                authors=[user['username']])
            entry.save()
            Entry.objects(id=entry.id).update_one(slug=unicode(entry.id))
            entry.reload() #made to avoid duplicate slugs and to generate an url
            flash('Entry created successfully.', 'success')
            if entry.published:
                return redirect(url_for('detail', slug=entry.slug))
            else:
                return redirect(url_for('edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')
    return render_template('create.html')


@app.route('/drafts')
@login_required
def drafts():
    query = Entry.drafts().order_by('-timestamp')
    return render_template('list.html', query, check_bounds=False)


@app.route('/<slug>')
def detail(slug):
    if session.get('logged_in'):
        entry = Entry.get_entry(slug, public=False)
    else:
        entry = Entry.get_entry(slug, public=True)
    if entry is None:
        return not_found(404)

    return render_template('detail.html', entry=entry)


@app.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    if session.get('logged_in'):
        entry = Entry.get_entry(slug, public=False)
    else:
        entry = Entry.get_entry(slug, public=True)
    if entry is None:
        return not_found(404)

    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry.title = request.form['title']
            entry.content = request.form['content']
            entry.published = request.form.get('published') or False
            entry.save()

            flash('Entry saved successfully.', 'success')
            if entry.published:
                return redirect(url_for('detail', slug=entry.slug))
            else:
                return redirect(url_for('edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')

    return render_template('edit.html', entry=entry)


@app.errorhandler(404)
def not_found(exc):
    print('Debug is set to ')
    print(app.config.get('DEBUG'))
    return Response('<h3>Not found</h3>'), 404


@app.route('/vacances', methods=['POST', 'GET'])
def vacances():
    return render_template('vacances.html')


@app.route('/inscriptions', methods=['POST', 'GET'])
def inscriptions():
    return render_template('inscriptions.html')


@app.route('/projet', methods=['POST', 'GET'])
def projet():
    return render_template('projet.html')


@app.route('/statuts', methods=['POST', 'GET'])
def statuts():
    return render_template('statuts.html')


@app.route('/camps_6_12', methods=['POST', 'GET'])
def camps_6_12():
    return render_template('camps_6_12.html')


@app.route('/camps_13_15', methods=['POST', 'GET'])
def camps_13_15():
    return render_template('camps_13_15.html')


@app.route('/camps_16_17', methods=['POST', 'GET'])
def camps_16_17():
    return render_template('camps_16_17.html')


@app.route('/jvoupas', methods=['POST', 'GET'])
def jvoupas():
    return render_template('jvoupas.html')


@app.route('/news', methods=['POST', 'GET'])
def news():
    return render_template('news.html')


@app.route('/coin_anims', methods=['POST', 'GET'])
def coin_anims():
    return render_template('coin_anims.html')


@app.route('/charte', methods=['POST', 'GET'])
def charte():
    return render_template('charte.html')


@app.route('/conseil', methods=['POST', 'GET'])
def conseil():
    return render_template('conseil.html')


@app.route('/journal', methods=['POST', 'GET'])
def journal():
    return render_template('journal.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    return render_template('contact.html')
