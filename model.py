from google.appengine.ext import db
from google.appengine.api import users
from time import mktime

import datetime
import feedparser
import logging

class User(db.Model):
    google_user = db.UserProperty()
    nickname = db.StringProperty()
    nickname_lower = db.StringProperty()
    deleted = db.BooleanProperty(default=False)
    
    def fetch_feeds(self):
        return {}
    
    def to_struct(self):
        if self.deleted:
            return None
        else:
            return {
                'id': self.key().id(),
                'email': self.google_user.email(),
                'nickname': self.nickname
            }

class InviteToken(db.Model):
    email = db.StringProperty()
    token = db.StringProperty()
    
    # The user who initiated the invite process
    sender = db.IntegerProperty()
    
    # If set, this indicates that the invite code has been used
    user_signed_up = db.ReferenceProperty(reference_class=User)

class InputFeed(db.Model):
    # parent(User)
    title = db.StringProperty()
    logo = db.StringProperty()
    url = db.StringProperty()
    time_fetched = db.DateTimeProperty(auto_now_add=True)
    deleted = db.BooleanProperty(default=False)
    language = db.StringProperty(default='none')
    
    def fetch_entries(self, fetch_all=True):
        """Fetches new entries
        
        If fetch_all is set to true, all entries will be fetched, regardless
        if their published date is before the last time this feed was fetched.
        """
        parsed_feed = feedparser.parse(self.url)
        entries = parsed_feed.get('entries')
        
        for entry in entries:
            # http://pythonhosted.org/feedparser/date-parsing.html
            tuple = entry.get('published_parsed')
            
            if tuple == None:
                tuple = entry.get('updated_parsed')
                
            published = datetime.datetime(*tuple[:6])
            
            content = None
            if len(entry.get('content', [])) > 0:
                content = entry.get('content')[0].get('value')

            if not content:
                content = entry.get('summary')

            if fetch_all or (published > self.time_fetched):
                existing_entry = Entry.all().ancestor(self).filter('guid =', entry.get('guid')).count(read_policy=db.EVENTUAL_CONSISTENCY, limit=1) 
                if not existing_entry:
                    m = Entry(
                        guid=entry.get('guid'),
                        link=entry.get('link'),
                        parent=self,
                        user=self.parent(),
                        content=content,
                        title=entry.get('title'),
                        time_published=published,
                    )
                    m.put()
            
        self.time_fetched = datetime.datetime.utcnow()
        self.save()

    def to_struct(self):
        return {
            'id': self.key().id(),
            'title': self.title,
			'logo': self.logo,
            'url': self.url,
            'time_fetched': mktime(self.time_fetched.timetuple()),
            'language': self.language,
        }

class Entry(db.Model):
    #parent(InputFeed)
    guid = db.StringProperty()
    link = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    link = db.TextProperty()
    time_published = db.DateTimeProperty()
    published = db.BooleanProperty(default=False)
    tags = db.ListProperty(db.Key)
    user = db.ReferenceProperty(reference_class=User)
    language = db.StringProperty(default='none') # set by feed

    def to_struct(self, include_tags=False):
        tags = []
        if include_tags:
            for tag in db.get(self.tags):
                tags.append(tag.to_struct())
        
        parent = self.parent()
        
        return {
            'id': self.key().id(),
            'feed_id': parent.key().id(),
            'feed_logo': parent.logo,
            'title': self.title,
    		'content': self.content,
            'link': self.link,
            'time_published': mktime(self.time_published.timetuple()),
            'time_published_rss': self.time_published.strftime("%a, %d %b %Y %H:%M:%S GMT"), #Fri, 26 Apr 2013 06:57:55 GMT
            'published': self.published,
            'tags': tags,
        }

class Tag(db.Model):
    #parent(User)
    title = db.StringProperty()
    title_lower = db.StringProperty()
    entry_count = db.IntegerProperty(default=0)
    entries = db.ListProperty(db.Key)

    def tag_entry(self, entry):
        self.entry_count += 1
        self.put()
        entry.tags.append(self.key())
        entry.save()

    def to_struct(self, include_entries=False):
        entries = []
        if include_entries:
            for entry in entries:
                entries.append(entry.to_struct())

        return {
            'title': self.title,
            'entry_count': self.entry_count,
            'entries': entries,
        }
