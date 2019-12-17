from project_app import app, db
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, g
from main.form import SignUpForm, TopicForm, CommentForm, GroupForm, GroupDiscussionForm, ArchiveTopicForm, PostForm
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from main.models import users
from main.models import Topics, Comments, Group, GroupDiscussion, Archive, SubscribedTopic, Posts
from datetime import datetime

'''
    Generates the homepage of the application

    Return:
        the home.html page to the viewer

'''
@app.route('/')
def index():
    return render_template('home.html')

'''
    Generates an about page, that describes the purpose of the application

    Return:
        the about.html page to the viewer

'''
@app.route('/about')
def about():
    return render_template('about.html')

'''
    Generates the view page for all the topics

    Return:
        the topics.html page with all the topics that have been created.

    This invocation is also reponsible for getting access to a specfic topic
    that had been created if there are any.
'''
@app.route('/topics')
def topics():
    result = Topics.query.all()

    if result:
        return render_template('topics.html', topics=result)
    else:
        msg = 'No topic Found'
        return render_template('topics.html', msg=msg)

@app.route('/posts')
def posts():
    '''
    Generates the view page for all the posts

    Return:
        the post.html page with all the posts that have been created.

    This invocation is also reponsible for getting access to a specfic posts
    that had been created if there are any.
    '''
    result = Posts.query.all()

    if result:
        return render_template('posts.html', posts=result)
    else:
        msg = 'No topic Found'
        return render_template('posts.html', msg=msg)



        '''
    Generates the html page of a single topic thread created using a given id


    Args:
        id: topic.id - The id given to each topic created.

    Return:
        the topic.html of the single topic and all the comments associated with the topic

    This invocation is also responsible for being able to comment on a particular topic.
    '''

@app.route('/topic/<string:id>/', methods=['GET','POST'])
def topic(id):
    form = CommentForm(request.form)
    topic = Topics.query.filter_by(id=id).first()
    comments = Comments.query.filter_by(topic_id=id).all()
    if request.method == 'POST' and form.validate():
        body = form.body_comment.data
        comment = Comments(session['username'], id , body)
        db.session.add(comment)
        db.session.commit()
    comments = Comments.query.filter_by(topic_id=id).all()
    return render_template('topic.html', form=form, topic=topic, comments=comments)

@app.route('/post/<string:id>/', methods=['GET','POST'])
def post(id):
    post = Posts.query.filter_by(id=id).first()
    return render_template('post.html', post=post)

'''
    Generates the User sign up page

    Return:
        the signup.html page that allows users to sign up

    This invocation is also responsible for allowing a regiestered user to login
    after the viewer has registered.
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user = users(name, username, email, password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered and can log in')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

'''
    Generates the user login page.

    Return:
        the login.html page for the viewer to enter his/her credentials

    This invocation is also responsible for authenticating the viewer credentials and
    redirecting the viewer to his/her page if the credentials have been validated.
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        result = users.query.filter_by(username = username, password = password).first()

        if result:
            session['logged_in'] = True
            session['username'] = username

            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Username and password doesnt match'
            return render_template('login.html', error=error)

    return render_template('login.html')

'''
    Checks if a user is still logged in.

    Return:
        true if the user is still logged in

    This invocation is also resposible for generating the login page if the
    viewer is no longer logged in.
'''
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

'''
    This ends the login session for the user and returns the login page

    Return:
        redirects the viewer to the login page after the viewer has logged out

'''

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

'''
    Generate the dashboard that shows all the
    topics the user has created

    Return:
        The topic posted by the specific user that is logged in, if the viewer
        logged in has no topics created a message is shown.
'''

@app.route('/dashboard')
@is_logged_in
def dashboard():
    user_id = session['username']
    result = Topics.query.filter_by(author=user_id).order_by(Topics.create_date.desc()).all()
    result1 = Posts.query.filter_by(author=user_id).order_by(Posts.create_date.desc()).all()

    if result or result1:
        return render_template('dashboard.html', topics=result, posts=result1)

    else:
        msg = 'No Topics Found'
        return render_template('dashboard.html', msg=msg)

'''
    Generates the page to add a topic about a certain topic to the viewer

    Return:
        The page for adding a topic to the viewer called add_topic.html

    This invocation is also responsible for adding any new topic to the viewer's dashboard
'''
@app.route('/add_topic', methods=['GET', 'POST'])
@is_logged_in
def add_topic():
    form = TopicForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        topic = Topics(title, session['username'], body, None)

        db.session.add(topic)
        db.session.commit()
        flash('Topic Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_topic.html', form=form)

@app.route('/add_post', methods=['GET', 'POST'])
@is_logged_in
def add_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        body = form.body.data
        post = Posts(session['username'], body, None)

        db.session.add(post)
        db.session.commit()
        flash('Post Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_post.html', form=form)
@app.route('/edit_post/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_post(id):

    post = Posts.query.filter_by(id=id).first_or_404()

    form = PostForm(request.form)

    form.body.data = post.body

    if request.method == 'POST' and form.validate():
        body = request.form['body']


        repost = Topics.query.filter_by(id=id).first_or_404()
        repost.body = body

        db.session.commit()

        flash('Post Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_post.html', form=form)

'''
    Generates the page for editing a specific topic to the viewer if the viewer has any
    topic created.

    Args:
        id: Topic.id - the id given to a specfic topic about a certain topic

    Return:
        the page for editing a topic selected by the viewer to the viewer.

    This invocation is also responsible for generating the changed topic to the dashboard
'''
@app.route('/edit_topic/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_topic(id):

    topic = Topics.query.filter_by(id=id).first_or_404()

    form = TopicForm(request.form)


    form.title.data = topic.title
    form.body.data = topic.body

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']


        repost = Topics.query.filter_by(id=id).first_or_404()
        repost.title = title
        repost.body = body

        db.session.commit()

        flash('Topic Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_topic.html', form=form)

'''
    Generates the dashboard after a a topic has
    been deleted

    Args:
        id: Topic.id - the id given to a specfic topic

    Return:
        redirects the viewer to the dashboard of the viewer.

    This invocation is also responsible for generating the dashboard with the changes made.
'''
@app.route('/delete_topic/<string:id>', methods=['POST'])
@is_logged_in
def delete_topic(id):

    topic = Topics.query.filter_by(id=id).first()

    db.session.delete(topic)

    db.session.commit()

    flash('Topic Deleted', 'success')

    return redirect(url_for('dashboard'))
@app.route('/delete_post/<string:id>', methods=['POST'])
@is_logged_in
def delete_post(id):

    post = Posts.query.filter_by(id=id).first()

    db.session.delete(post)

    db.session.commit()

    flash('Post Deleted', 'success')

    return redirect(url_for('dashboard'))
    '''
    Creates the group for the user

    Args:
        group_id: - the group id given to a specfic topic about a certain topic
	group_title - title of the group
    creator: - the creator of the group
    person1: - the first person in the group
    person2: - the second person in the group
    person3: - the third person in the group
    person4: - the fourth person in the group


    Return:
        redirects the allgroups and show user all the groups created

    This invocation is also responsible for creating the group.
    '''
@app.route('/creategroup', methods=['GET', 'POST'])
@is_logged_in
def creategroup():
    form = GroupForm(request.form)
    if request.method == 'POST' and form.validate():
        group_title = form.group_title.data
        creator = session['username']
        person1 = form.person1.data
        person2 = form.person2.data
        person3 = form.person3.data
        person4 = form.person4.data
        group = Group(group_title, creator, person1, person2, person3, person4)
        db.session.add(group)
        db.session.commit()
        flash('Succesfully, created group')
        return redirect(url_for('allgroups'))
    return render_template('creategroup.html', form=form)
    """
    Shows all the group created by user

    Args:
        user_id: - the group id given to a specfic topic about a certain topic
        Return:
            redirects the allgroups and show user all the groups created
    """
@app.route('/allgroups')
@is_logged_in
def allgroups():
    user_id = session['username']
    result = Group.query.filter_by(creator=user_id).all()
    if result:
        return render_template('allgroups.html', groups=result)
    else:
        msg = 'GroupNotFound'
        return render_template('allgroups.html', msg=msg)
        """
    Generate the group the user has been added to

    Args:
        id= id: - the group id given to a specfic group
        body = the group message where the user will write his/her message
        Return:
            redirects the the same group where the user is in
    """
@app.route('/GroupDiscussion/<string:id>/', methods=['GET','POST'])
@is_logged_in
def GroupDiscussion(id):
    form = GroupForm(request.form)
    group = Group.query.filter_by(id=id).first()
    discussions = GroupDiscussion.query.filter_by(group_id=id).all()
    if request.method == 'POST' and form.validate():
        body = form.body_discussion.data
        discussion = GroupDiscussion(session['username'], id , body)
        db.session.add(discussion)
        db.session.commit()

    return render_template('GroupDiscussion.html', form=form, group=group, discussions=discussions)

'''
    Generates the page for archiving a specific topic to the viewer if any
    topic has been created.

    Args:
        id: Topic.id - the id given to a specfic topic about a certain topic

    Return:
        redirects the viewer to the topics page.

    This invocation is also responsible for generating the archived topics by the viewer.
'''
@app.route('/archive_topic/<string:id>', methods=['GET','POST'])
@is_logged_in
def archive_topic(id):
    form = ArchiveTopicForm(request.form)
    result= Topics.query.filter_by(id=id).first()
    if result:
        archive_topic = Archive(result.title, result.author, result.body, result.create_date)
        db.session.add(archive_topic)
        db.session.commit()
        topic = Topics.query.filter_by(id=id).first()
        db.session.delete(topic)
        db.session.commit()
        flash('Topic Archived')
        return (redirect(url_for('topics')))
    return render_template('topics.html', form=form)

'''
    Generates the page to all the archived topics

    Return:
        The page for archived topics to the viewer called all_archived_topics.html

    This invocation is also responsible for adding any new archived topics to the viewer's dashboard
'''
@app.route('/all_archived_topics')
def all_archive_topics():
    result = Archive.query.all()
    if result:
        return render_template('all_archived_topics.html', topics=result)
    else:
        msg = 'No Topics Found'
        return render_template('all_archived_topics.html', msg=msg)

'''
    Generates the page for viewing archive topics to the viewer

    Args:
        id: Topic.id - the id given to a specfic topic about a certain topic

    Return:
        redirects the viewer to the view_archive_topics.html.

    This invocation is also responsible for generating the archived topics by the viewer.
'''

@app.route('/view_archive_topic/<string:id>/')
def view_archive_topic(id):
    topic = Archive.query.filter_by(id=id).first()
    return render_template('view_archive_topic.html', topic=topic)

'''
    Generates the message for subscribed topic to the viewer

    Args:
        id: Topic.id - the id given to a specfic topic about a certain topic
	username - the unique username for a given users(u), used to
                    distinguish the users

    Return:
        redirects the viewer to the topics dashboard.

    This invocation is also responsible for generating the subscribed topics by the viewer.
'''
@app.route('/topic_subscription/<string:id>', methods=['GET','POST'])
@is_logged_in
def topic_subscription(id):
    user = session['username']
    result = SubscribedTopic(user, id)
    db.session.add(result)
    db.session.commit()
    flash("Subscribed")
    return redirect(url_for('topics'))
    return render_template('topics.html')
