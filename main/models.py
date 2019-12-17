"""
Group Project- Comp2005

The following module maps a relational database system to objects
and creates a table in the database of the object. The columns of the
table in the database are the attributes that belong to the object created.

Simply construct an object and its attributes for that object will be stored
in the database.

Classes:
    users - Mapping created to a user object
    Topics - Mapping created to a Topics object
    Comments - Mappings created to a Comment object
    GroupDiscussion - Mapping created to the GroupDiscussions


"""

__all__ = ["users", "Topics", "Comments", "Group", "GroupDiscussion","Archive","SubscribedTopic"]

from project_app import db
from datetime import datetime

class users(db.Model):
    """ This creates a table for all the users created

    Attributes:
        id: Integer - the primary key id is given to each a users(u) created
        name: String - the name of a users(u) that has been created
        username: String - the unique username for a given users(u), used to
                    distinguish the users.
        email: String - the unique email address associated of a users(u)
        password: String - the password associated with users(u)

    Examples:


        A single user John added to the table of users,
        (i.e registering to the application :)
        <code>
          newUser = users("John", "johnM", "johnM@domain.com", "myPassword")
          db.session.add(newUser)
          db.session.commit()
        </code>

        """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(60))



    def __init__(self, name, username, email, password):
        """
           Args:

               name - value for name attribute
               username - value for username attribute
               email - value for email attribute
               password - value for password attribute

        """
        self.name = name
        self.username = username
        self.email = email
        self.password = password
    def __repr__(self):
        return '<users %r>' % self.username
class Topics(db.Model):
    """ This creates a table for all Topics created

        Attributes:

            id: Integer - the primary key id given to each topic thats
                been created for a topic.
            title: String - the title of the topic created
            author: String - the foreign key that is different to each
                    user.
            body: Text- the body of the topic created.
            create_date: DateTime - the date of the topic created

        Examples:

            A single topic is created and added to the table associated to all
             all the topics about different topics with a
             title of "This is a topiic" with the contents
            "hello, my name is John" by the user that is logged in.

            topic = Topics("This is a topic" , session[username],
                    "Hello my name is John", None)
            db.session.add(topic)
            db.session.commit()

        <code>

    """
    __tablename__ = 'Topics'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(100), db.ForeignKey('users.username'))
    body = db.Column(db.Text)
    create_date = db.Column(db.DateTime)

    def __init__(self, title, author, body, create_date):
        """
         Args:
         title - the value given the title attribute
         author - the value given the author attribute
         body - the value given the body attribute
         create_date - the value given the create_date attribute

         """

        self.title = title
        self.author = author
        self.body = body
        if create_date is None:
            self.create_date = datetime.utcnow()
        else:
            self.create_date = create_date

    def __repr__(self):
        return '<Topics %r>' % self.title
class Posts(db.Model):
    """
        This creates a table for all posts created

            Attributes:

                id: Integer - the primary key id given to each post thats
                    been created for a post.
                author: String - the foreign key that is different to each
                        user.
                body: Text- the body of the post created.
                create_date: DateTime - the date of the post created

            <code>

            </code>

    """
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(100), db.ForeignKey('users.username'))
    body = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    def __init__(self, author, body, create_date):
        """
         Args:
         author - the value given the author attribute
         body - the value given the body attribute
         create_date - the value given the create_date attribute

         """
        self.author = author
        self.body = body
        if create_date is None:
            self.create_date = datetime.utcnow()
        else:
            self.create_date = create_date

    def __repr__(self):
        return '<Posts %r>' % self.title

class Comments(db.Model):
    """ This creates a table of all the comments created called Comments

        Attributes:

        comment_writer: String - the username of the user posting the comment
        id: Integer - The primary key that is unique to this table that differeniates
            all the comments in the table
        topic_id : Integer - this the foreign key given to each comment which
                    is the id given to each topic.
        body_comment : Text - The text written in the comment that would created

        Examples:
            <code>



            </code>

    """

    __tablename__ = 'Comments'
    comment_writer = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key = True)
    topic_id= db.Column(db.Integer, db.ForeignKey('Topics.id'))
    body_comment = db.Column(db.Text)

    def __init__(self,comment_writer,topic_id,body_comment):
        """

        Args:
            comment_writer - the value given to the comment writer attribute
            topic_id - the value given to the topic_id attribute
            body_comment - the value given to the body_comment attribute

            """
        self.comment_writer = comment_writer
        self.topic_id = topic_id
        self.body_comment = body_comment
    def __repr__(self):
        return '<Topics %r>' % self.body_comment

class Group(db.Model):
    __tablename__ = 'Group'
    id = db.Column(db.Integer, primary_key = True)
    group_title = db.Column(db.String(80))
    creator = db.Column(db.String(25), db.ForeignKey('users.username'))
    person1 = db.Column(db.String(25))
    person2 = db.Column(db.String(25))
    person3 = db.Column(db.String(25))
    person4 = db.Column(db.String(25))


    def __init__(self, group_tittle, creator, person1, person2, person3, person4):
        self.group_tittle = group_tittle
        self.creator = creator
        self.person1 = person1
        self.person2 = person2
        self.person3 = person3
        self.person4 = person4

    def __repr__(self):
        return '<Group %r>' % self.title

class GroupDiscussion(db.Model):
    """ This create the table that maps to the object GroupDiscussion
        The group discussion created can only have up to 5 members only.

        Attributes:
        id: Integer -  the primary key associated to every entry in the table of group discussion
        group_title: String - the name of the group discusion created
        person1: String - This a foriegn Key that is the username of the creator of the
                            the group discussion.
        person2: String - the username of the 2nd user added
        person3: String - the username of the 3rd user added
        person4: String - the username of the 3rd user added
        person5: String - the username of the 5th user added
        body_discussion: Text - the body of discussions the users.

        Examples:
        Creating a group discussion with 4 other users:


        <code>

        </code>


        """
    __tablename__ = 'GroupDiscussion'
    id = db.Column(db.Integer, primary_key = True)
    writer = db.Column(db.String(50))
    group_id= db.Column(db.Integer, db.ForeignKey('Group.id'))
    body_discussion = db.Column(db.Text)

    def __init__(self, group_id, body_discussion):
        """
    Args:

        group_title - the value of the group-title attribute
        person1 - the value of the person1 attribute
        person2 - the value of the person2 attribute
        person3 - the value of the person3 attribute
        person4 - the value of the person4 attribute
        person5 - the value of the person5 attribute
        body_discussion - the value of the body_discussion attribute

        """
        self.writer = db.Column(db.String(50))
        self.group_id = group_id
        self.body_discussion = body_discussion
    def __repr__(self):
         return '<GroupDiscussion %r>' % self.body_discussion
class Archive(db.Model):
    """ This creates a table of all the archived Topics called Archive

        Attributes:

        id: Integer - The primary key that is unique to this table that differeniates
            all the comments in the table
        title : String - the value given the title attribute.
        author : String - the value given the author attribute
	body : Text - the body of the archived Topics
	create_date : DateTime - Generates the date and time for the archived Topics

        Examples:
            <code>



            </code>

    """
    __tablename__ = 'Archive'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(100))
    body = db.Column(db.Text)
    create_date = db.Column(db.DateTime)

    def __init__(self, title, author, body, create_date):
        """
         Args:
         title - the value given the title attribute
         author - the value given the author attribute
         body - the value given the body attribute
         create_date - the value given the create_date attribute

         """
        self.title = title
        self.author = author
        self.body = body
        if create_date is None:
            self.create_date = datetime.utcnow()
        else:
            self.create_date = create_date

    def __repr__(self):
        return '<Archive %r>' % self.title

class SubscribedTopic(db.Model):
    """ This creates a table of all the subscribed topics called SubscribedTopics

            Attributes:

            id: Integer - The primary key that is unique to this table that differeniates
                all the comments in the table
            user_sub : String - The users subscribed to a specific topic.
            pst_id : Integer - the value given the topic subscribed

            Examples:
                <code>



                </code>
    """
    __tablename__ = 'SubscribedTopic'
    id = db.Column(db.Integer, primary_key = True)
    user_sub = db.Column(db.String(25), db.ForeignKey('users.username'))
    topic_id = db.Column(db.Integer, db.ForeignKey('Topics.id'))
    def __init__(self, user_sub, topic_id):
        '''Args:
         user_sub - the value given to the user subscribed
         topic_id - the value given the id of the topics created
         '''
        self.user_sub = user_sub
        self.topic_id = topic_id
    def __repr__(self):
        return '<SubscribedTopic %r>' %self.topic_id
