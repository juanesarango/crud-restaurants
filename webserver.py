from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import crud


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = crud.query_all_restaurants()

                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants:</h1>"
                output += "<ul>"
                for restaurant in restaurants:
                    output += "<li>"
                    output += "<span>%s</span><br>" % restaurant.name
                    output += "<a href=/restaurants/%s/edit>Edit</a><br>" % restaurant.id
                    output += "<a href=/restaurants/%s/delete>Delete</a><br>" % restaurant.id
                    output += "</li>"
                    
                output += "</ul>"
                output += "<h2><a href='/restaurants/new'>Create New Restaurant</a></h2>"
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Create New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'> \
                    <h2>What is the name of the new restaurant?</h2> \
                    <input name="restaurant_name" type="text" placeholder="New restaurant name"> \
                    <input type="submit" value="Create"></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return
            
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = self.path[
                    self.path.find('/restaurants/') + 13:
                    self.path.rfind('/')]
                restaurant = crud.query_restaurant_by_id(
                    restaurant_id=restaurant_id)
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'> \
                    <h2>What is the new name of the restaurant?</h2> \
                    <input name="restaurant_name" type="text" value='%s'> \
                    <input type="submit" value="Change Name"></form>''' % (restaurant.id, restaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                return
            
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = self.path[
                    self.path.find('/restaurants/') + 13:
                    self.path.rfind('/')]
                restaurant = crud.query_restaurant_by_id(
                    restaurant_id=restaurant_id)
                output = ""
                output += "<html><body>"
                output += "<h1>Delete Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><h2>Are you sure you want to delete %s?</h2><input type="submit" value="Sure. Delete it!"></form>''' % (restaurant.id, restaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()
            
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant_name')[0]
                    crud.create_restaurant(restaurant_name=restaurant_name)
                    new_restaurant = crud.query_restaurant_by_name(
                        restaurant_name)
                    if new_restaurant:
                        output = ""
                        output += "<html><body>"
                        output += "<h1>Restaurant %s has been created successfully</h1>" % new_restaurant.name
                        output += "<a href='/restaurants'>Show all restaurants</a>"
                        output += "</body></html>"
                        self.wfile.write(output)
                        return
                else:
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Restaurant could not be created</h1>" % new_restaurant.name
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant_name')[0]
                    restaurant_id = self.path[
                        self.path.find('/restaurants/') + 13:
                        self.path.rfind('/')]
                    crud.edit_restaurant(
                        restaurant_id=restaurant_id, 
                        restaurant_name=restaurant_name)
                    restaurant = crud.query_restaurant_by_id(
                        restaurant_id=restaurant_id)                  
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Restaurant %s has been edited successfully</h1>" % restaurant.name
                    output += "<a href='/restaurants'>Show all restaurants</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return
                else:
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Restaurant could not be edited</h1>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_id = self.path[
                        self.path.find('/restaurants/') + 13:
                        self.path.rfind('/')]
                    crud.delete_restaurant(
                        restaurant_id=restaurant_id)
                    return
                else:
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Restaurant could not be deleted</h1>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

        except IOError:
            pass


def main():
    try:
        port = 4000
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()