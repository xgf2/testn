import settings
from http.server import BaseHTTPRequestHandler, HTTPServer


def init_server(): 
    class NewsRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/getnews' or self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                page_news = '<html> <p> Hello ! </p></html>' 
                self.wfile.write(page_news.encode('utf-8'))
                self.server.path = self.path
            else:
                self.send_response(404)
                self.end_headers()

    server_address = (settings.ADDRESS, settings.PORT)
    httpd = HTTPServer(server_address, NewsRequestHandler)
    httpd.handle_request()
    httpd.server_close()
    #httpd.serve_forever() 


if __name__ == '__main__':
    init_server()
