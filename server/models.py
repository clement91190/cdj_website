from server import db, oembed_providers, app
import datetime
from micawber import parse_html
from flask import Markup
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from mongoengine import DoesNotExist


class Entry(db.Document):
    title = db.StringField()
    slug = db.StringField(default='default_slug')
    content = db.StringField()
    published = db.BooleanField()
    timestamp = db.DateTimeField(default=datetime.datetime.now)

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
