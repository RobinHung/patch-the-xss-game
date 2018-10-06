import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(open("mainpage.html").read())


class LevelOne(webapp2.RequestHandler):
    page_header = """
    <!doctype html>
    <html>
    <head>
        <!-- Internal game scripts/styles, mostly boring stuff -->
        <script src="/static/game-frame.js"></script>
        <link rel="stylesheet" href="/static/game-frame-styles.css" />
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


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/level-1', LevelOne)
], debug=True)