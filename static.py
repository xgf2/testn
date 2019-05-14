import http.client as client
import os, re, settings

def save_image(href):
    host_url = re.search(settings.HOST_URL, href).group()
    host_path = re.search('(' + settings.HOST_PATH + ')/([a-z,0-9,/,.]*)', href).group()

    connection = client.HTTPSConnection(host_url)
    connection.request('GET', host_path)
    response = connection.getresponse()

    if response.status == 200:
        image_data = response.read()
        connection.close()
