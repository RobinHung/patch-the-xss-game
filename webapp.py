import webapp2
import os
from google.appengine.ext.webapp import template
import jinja2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(open("mainpage.html").read())


class LevelOne(webapp2.RequestHandler):
    page_header = """
    <!doctype html>
    <html>
    <head>
        <!-- Internal game scripts/styles, mostly boring stuff -->
        <script src="/static/js/game-frame.js"></script>
        <link rel="stylesheet" href="/static/css/game-frame-styles.css" />
    </head>

    <body id="level1">
        <div>
    """

    page_footer = """
        </div>
    </body>
    </html>
    """

    main_page_markup = """
    <form action="" method="GET">
    <input id="query" name="query" value="Enter query here..."
        onfocus="this.value=''">
    <input id="button" type="submit" value="Search">
    </form>
    """

    def render_string(self, s):
        self.response.out.write(s)

    def get(self):
        # Disable the reflected XSS filter for demonstration purposes
        self.response.headers.add_header("X-XSS-Protection", "0")

        # @csp
        self.response.headers.add_header(
            "Content-Security-Policy", "script-src 'self' style-src 'self'")

        if not self.request.get('query'):
            # Show main search page
            self.render_string(LevelOne.page_header +
                               LevelOne.main_page_markup + LevelOne.page_footer)
        else:
            query = self.request.get('query', '[empty]')

            # Our search engine broke, we found no results :-(
            message = "Sorry, no results were found for <b>" + query + "</b>."
            message += " <a href='?'>Try again</a>."

            # Display the results page
            self.render_string(LevelOne.page_header +
                               message + LevelOne.page_footer)

        return


class LevelTwo(webapp2.RequestHandler):
    # def render_template(self, filename, context={}):
    #     path = os.path.join(os.path.dirname(__file__), filename)
    #     self.response.out.write(template.render(path, context))

    # def get(self):
    #     self.render_template('/level-2/index.html')

    def get(self):
        self.response.write(open("level2-index.html").read())


class LevelThree(webapp2.RequestHandler):
    # def get(self):
    #     self.response.write(open("level3-index.html").read())

    def render_template(self, filename, context={}):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, context))

    def get(self):
        self.render_template('level3-index.html')


class LevelFour(webapp2.RequestHandler):
    # def get(self):
    #     self.response.write(open("level4-index.html").read())
    def render_template(self, filename, context={}):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, context))

    def get(self):
        # Disable the reflected XSS filter for demonstration purposes
        # self.response.headers.add_header("X-XSS-Protection", "0")

        if not self.request.get('timer'):
            # Show main timer page
            self.render_template('level4-index.html')
        else:
            try:
                # @xss
                int(self.request.get('timer', 0))
                timer = str(int(self.request.get('timer', 0)))
                self.render_template('timer.html', {'timer': timer})

            except ValueError:
                self.response.write("Error input!")

        return


class LevelFive(webapp2.RequestHandler):
    def render_template(self, filename, context={}):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, context))

    def get(self):
        # Disable the reflected XSS filter for demonstration purposes
        self.response.headers.add_header("X-XSS-Protection", "0")

        # # Route the request to the appropriate template
        # if "signup" in self.request.path:
        #     self.render_template('signup.html',
        #                          {'next': self.request.get('next')})
        # elif "confirm" in self.request.path:
        #     self.render_template('confirm.html',
        #                          {'next': self.request.get('next', 'welcome')})
        # else:
        #     self.render_template('welcome.html', {})

        self.render_template('welcome.html', {})

        return


class LevelFiveSignUp(webapp2.RequestHandler):
    def render_template(self, filename, context={}):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, context))

    def get(self):
        if "signup" in self.request.path:
            self.render_template('signup.html',
                                 {'next': self.request.get('next', 'welcome').replace(':', '')})
        else:
            self.response.write("Error...")

        return


class LevelFiveConfirm(webapp2.RequestHandler):
    def render_template(self, filename, context={}):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, context))

    def get(self):
        if "confirm" in self.request.path:
            # self.render_template('confirm.html',
            #                      {'next': self.request.get('next')})
            self.render_template('confirm.html',
                                 {'next': self.request.get('next', 'welcome')})
        else:
            self.response.write("Error...")

        return


class LevelSix(webapp2.RequestHandler):
    def render_template(self, filename, context={}):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, context))

    def get(self):
        self.render_template('level6-index.html')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/level-1', LevelOne),
    ('/level-2', LevelTwo),
    ('/level-3', LevelThree),
    ('/level-4', LevelFour),
    ('/level-5', LevelFive),
    ('/level-5/welcome', LevelFive),
    ('/level-5/signup', LevelFiveSignUp),
    ('/level-5/confirm', LevelFiveConfirm),
    ('/level-6', LevelSix)
], debug=True)
