"""
Group Project 2005

The following module takes the user validated data and sets up the
parameters in the database and it creates a table in the database.
The module displays a form to the user and the type Form are subclasses of WTForms.

Classes:
	SignUpForm - Validates the register form fields
	LoginForm - Validates the login form fields
	ArticleForm - Validates the article form attributes
	CommemtForm - Validates the comment form attributes
	GroupForm - Validates the group form users
	GroupDiscussionForm - Validates the group discussion form attributes
	ArchivePostForm - Validates the archive post form
"""
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, g
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class SignUpForm(Form):
    """
SignUpForm, this class basically validates if the user enters the required
fields such as the name, username,email, password and confirming the password
and once the data is entered WTF form will validate the data entered

	Attributes:
		name: String - validates the name of a users(u) that has been created
		username: String -validates the unique username for a given users(u), used to distinguish the users.
		email: String - validates the unique email address associated of a users(u)
		password: String -validates the password associated with users(u)
		confirm: String - validates confirms the password provided by the user
        """
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
class LoginForm(Form):
    """
LoginForm, this class validates the username and password entered by the user through WTF forms

	Attributes:
		username: String - validates the unique username for a given users(u), used to distinguish the users.
		password: String - validates the password associated with users(u)
        """
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

class TopicForm(Form):
    """
TopicForm, this validates the title and the body for a topic created

	Attributes:
		title: String - validates the title of a the topic created.
		body: Text - validates the body of a topic created.
        """
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])
class PostForm(Form):
    """
PostForm, this validates the title and the body for a post created

	Attributes:
		title: String - validates the title of a post for the topic created.
		body: Text - validates the body of a post for the topic created.
        """
    body = TextAreaField('Body', [validators.Length(min=30)])
class CommentForm(Form):
    """
Validates the comment on the body of the post for a topic

	Attributes:
		body_comment: Text - validates the text written in the comment that would created
        """
    body_comment = TextAreaField('Body', [validators.Length(max=400)])
"""
	This class creates a Group form where it validates the number of people in the group including the creator of the group

	Attributes:
        group_title: String - Validates the name of the group discusion created
        person1: String - Validates the foriegn Key that is the username of the creator of the
                            the group discussion.
        person2: String - Validates the username of the 2nd user added
        person3: String - Validates the username of the 3rd user added
        person4: String - Validates the username of the 3rd user added
        person5: String - Validates the username of the 5th user added

		"""
class GroupForm(Form):
    group_title = StringField('Group Title', [validators.Length(min=1, max=200)])
    creator = StringField('Person 1', [validators.Length(min=4, max=25)])
    person1 = StringField('Person 2', [validators.Length(min=4, max=25)])
    person2 = StringField('Person 3', [validators.Length(min=4, max=25)])
    person3 = StringField('Person 4', [validators.Length(min=4, max=25)])
    person4 = StringField('Person 4', [validators.Length(min=4, max=25)])


"""
Validates the discussion form for the group discussion
	Attributes:
	 body_discussion: Text - Validates the body of discussions the users.
	 """
class GroupDiscussionForm(Form):
    body_discussion = TextAreaField('Message', [validators.Length(max=400)])
class ArchiveTopicForm(Form):
    """
Validates the title and the body for the post to be archived

	Attributes:
	title: String - validates the title of the archive post created.
	body: Text - validates the body of the archive post created.


        """
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])
