from server import db, oembed_providers, app
import datetime, bcrypt 
from micawber import parse_html
from flask import Markup
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from mongoengine import DoesNotExist


class User(db.Document):
    username = db.StringField(required = True, unique = True)
    pwHash = db.StringField(required = True)
    email = db.EmailField(required = True)
    first_name = db.StringField()
    last_name = db.StringField()
    birthday = db.DateTimeField()
    address = db.StringField()

    @classmethod
    def userExists(cls, name):
        try: 
            return User.objects(username=name).get()
        except DoesNotExist:
            return None

    @classmethod
    def checkCredentials(cls, name, passwd):
        try:
            checkedUser = User.objects(username=name).get()
            #The passwords are hashed and checked with bcrypt. Bcrypt checking method only accepts byte strings,
            #while mongodb stores them as unicode strings, hence the need to reencode them;
            encodedPasswd = passwd.encode('utf8')
            if bcrypt.checkpw(encodedPasswd, checkedUser.pwHash.encode('utf8')):
                return checkedUser
            else:
                return None
        except DoesNotExist:
            return None

class Entry(db.Document):
    title = db.StringField()
    slug = db.StringField(unique=True, default='temp_slug')
    content = db.StringField()
    published = db.BooleanField()
    timestamp = db.DateTimeField(default=datetime.datetime.now)
    authors = db.ListField(db.ReferenceField(User))

    @property
    def html_content(self):
        """
        Generate HTML representation of the markdown-formatted blog entry,
        and also convert any media URLs into rich media objects such as video
        players or images."""
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)

    @classmethod
    def public(cls):
        return Entry.objects(published=True)

    @classmethod
    def drafts(cls):
        return Entry.objects(published=False)

    @classmethod
    def get_entry(cls, slug, public=True):
        try:
            if public:
                return Entry.objects(published=True, slug=slug).first()
            else:
                return Entry.objects(slug=slug).first()
        except DoesNotExist:
            return None
    
    def get_author_names(self):
        author_names = []
        for author_ref in self.authors:
            author = User.objects(username=author_ref.id).get()
            author_names.append(author.username)
        return author_names

    def get_short_text(self):
        if len(self.content) <= 150:
            return self.content
        else:
            for i in range(150, len(self.content)):
                if self.content[i] == ' ':
                    return self.content[:i]
            return self.content

    def is_shortened(self):
        return len(self.content) > 150
