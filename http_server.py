#!/home/testn/testnv/bin/python 

import settings, view, static
from http.server import BaseHTTPRequestHandler, HTTPServer


def init_server(): 
    class NewsRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/reload/db' or self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(view.news_from_db().encode('utf-8'))
                self.server.path = self.path

            elif self.path == '/reload/site':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(view.news_from_site().encode('utf-8'))
                self.server.path = self.path

            elif self.path == '/css/style.css':
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(static.read_file(settings.CSS_PATH + 'style.css').encode('utf-8'))
                self.server.path = self.path

            else:
                self.send_response(404)
                self.end_headers()

    server_address = (settings.ADDRESS, settings.PORT)
    httpd = HTTPServer(server_address, NewsRequestHandler)
    httpd.serve_forever() 


if __name__ == '__main__':
    init_server()
