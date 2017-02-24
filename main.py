#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os, jinja2
import webapp2, cgi, re

from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

#BLOG DATABASE SKELETON
class BlogPosts(db.Model):
    """ File data skeleton for blogs  """
    title = db.StringProperty(required = True)
    body = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#DEFAULT MAIN HOME PAGE
class MainHandler(Handler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.build-a-blog.com/
    """
    def get(self):
        self.render("front.html")



#SAMPLE DEFINED BLOG PAGE
    #Header "Blog!"
    #list of the 5 most recent posts
        #includes a header size of post title **That is a permalink to posts
        #includes the text of the post below (all?)
        #single empty line between each page 'item'
class BlogHandler(Handler):
    """ Handles requests coming in to '/blog'
        e.g. www.build-a-blog.com/blog
    """
    # def get(self):
    #     self.render("blog.html")
    def render_blog(self, title="", body="", error=""):
        blogentries = db.GqlQuery("SELECT * FROM BlogPosts ORDER BY created DESC LIMIT 5")
        self.render("blog.html", title=title, body=body, error=error, blogentries=blogentries)

    def get(self):
        self.render_blog()


#SAMPLE DEFINED NEW POST PAGE
    #header "New Post"
    #Title + line text box for entry
    #Post + large text box for entry
    #Large Submit button
        #submit button takes to a created post page
            #header = previous "title"
            #body = previous post text
            #dynamically created numeric ID for page permalink
        #xxxno other items on pagexxx
class NewPostHandler(Handler):
    """ Handles requests coming in to '/newpost'
        e.g. www.build-a-blog.com/newpost
    """
    # def get(self):
    #     self.response.write('This will be new post page!')
    def render_newpost(self, title="", body="", error=""):
        self.render("newpost.html", title=title, body=body, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            ##input to database
            blogentry = BlogPosts(title=title, body=body)
            blogentry.put()
            self.redirect("/blog")
        else:
            error = "Both Title and Body need entries!"
            self.render_newpost(error = error, title = title, body = body)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler)
], debug=True)
