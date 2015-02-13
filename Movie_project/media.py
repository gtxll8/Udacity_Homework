__author__ = 'gcalinescu'
import webbrowser

class Movie():

    """ This is the documentation for media class
    class Movies contains information about a movie
    and can be extended to as many attributes as you want.
    """

    VALID_RATINGS = ["G", "PG", "PG-13", "R"]
    def __init__ (self, movie_title, movie_storyline, poster_image, trailer_youtube):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
    #this is an implementation of __name__ when
    #to find out if it's called as a program or imported
    if __name__ == '__main__':
        print "Used by itself and not imported"