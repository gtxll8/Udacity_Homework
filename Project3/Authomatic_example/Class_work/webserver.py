from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                restaurantid = self.path.split("/")[2]
                restaurantdata = session.query(Restaurant).filter_by(id=restaurantid).one()
                if restaurantdata != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Are You sure you want to delete: %s </h2></br>" % restaurantdata.name
                    output += "<form method='POST' enctype='multipart/form-data' " \
                              "action='/restaurants/%s/delete'><h2>" % restaurantid
                    output += "<input type='submit' value='YES'> <input type='submit' value='No'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/edit"):
                restaurantid = self.path.split("/")[2]
                restaurantdata = session.query(Restaurant).filter_by(id=restaurantid).one()
                if restaurantdata != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Edit restaurant name:</h2></br>"
                    output += "<form method='POST' enctype='multipart/form-data' " \
                              "action='/restaurants/%s/edit'><h2>" % restaurantid
                    output += "<input name='RestaurantName' type='text' "
                    output += "placeholder = '%s'>" % restaurantdata.name
                    output += "<input type='submit' value='Rename'> </form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Create a new restaurant:</h2></br>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>"
                output += "<input name='newRestaurantName' type='text' "
                output += "placeholder = 'New restaurant Name'>"
                output += "<input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Restaurants List:</h2></br>"
                output += "<a href= 'restaurants/new' > Create a new restaurant record here </a></br></br></n>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a></br>" % restaurant.id
                    output += "<a href='/restaurant/%s/delete'>Delete</a></br>" % restaurant.id
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>
                          What would you like me to say?</h2><input name="message" type="text" >
                          <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>
                          What would you like me to say?</h2><input name="message" type="text" >
                          <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:

            if self.path.endswith("/delete"):
                print "delete!"
                restaurantid = self.path.split("/")[2]
                restaurantquery = session.query(Restaurant).filter_by(id=restaurantid).one()
                if restaurantquery != []:
                    session.delete(restaurantquery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('RestaurantName')
                restaurantid = self.path.split("/")[2]
                print restaurantid
                restaurantquery = session.query(Restaurant).filter_by(id=restaurantid).one()
                if restaurantquery != []:
                    restaurantquery.name = messagecontent[0]
                    session.add(restaurantquery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                # Create new restaurant class
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()



                # self.send_response(301)
                #self.end_headers()
                #ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                #if ctype == 'multipart/form-data':
                #    fields = cgi.parse_multipart(self.rfile, pdict)
                #    messagecontent = fields.get('message')
                #output = ""
                #output += "<html><body>"
                #output += " <h2> Okay, how about this: </h2>"
                #output += "<h1> %s </h1>" % messagecontent[0]
                #output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>
                #          What would you like me to say?</h2><input name="message" type="text" >
                #          <input type="submit" value="Submit"> </form>'''
                #output += "</body></html>"
                #self.wfile.write(output)
                #print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()