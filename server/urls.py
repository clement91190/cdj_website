from server import app
from flask import render_template, session, url_for, redirect, request, flash, Response
import functools
from models import Entry


@app.route('/test', methods=['POST', 'GET'])
def test():
    return "Hello World"


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('index.html')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next') #Retrieves the next page to serve after successful login from the QUERY STRING (after the '?')
    if request.method == 'POST' and request.form.get('password'):	#in the URL
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('main'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html') #, next_url=next_url)


@app.route('/temp_log', methods=['GET', 'POST'])
def truc():
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry = Entry.create(
                title=request.form['title'],
                content=request.form['content'],
                published=request.form.get('published') or False)
            flash('Entry created successfully.', 'success')
            if entry.published:
                return redirect(url_for('detail', slug=entry.slug))
            else:
                return redirect(url_for('edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')
    return render_template('create.html')


@app.route('/drafts/')
@login_required
def drafts():
    query = Entry.drafts().order_by('-timestamp')
    return render_template('list.html', query, check_bounds=False)


@app.route('/<slug>/')
def detail(slug):
    if session.get('logged_in'):
        entry = Entry.get_entry(slug, public=False)
    else:
        entry = Entry.get_entry(slug, public=True)
    if entry is None:
        return not_found()

    return render_template('detail.html', entry=entry)


@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    if session.get('logged_in'):
        entry = Entry.get_entry(public=False)
    else:
        entry = Entry.get_entry(public=True)
    if entry is None:
        return not_found()

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
