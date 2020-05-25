__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "GPL v3"
__version__ = "0.0.2"
__status__ = "Prototype"

import QmlReader
import Questionnaire
import os
import os.path
import string
import secrets
import getpass
import configparser


import cherrypy
from cherrypy.lib import auth_digest
from cherrypy.lib import static

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

config = configparser.ConfigParser()

CONFIGFILE = 'settings.ini'

config.read(CONFIGFILE)

class LoginIndex(object):
    @cherrypy.expose
    def index(self):
        return """
          <html><body>
              <h2>Login</h2>
            <a href='secure'>here</a>
          </body></html>
          """


class FileDemo(object):
    def __init__(self):
        self.png_filename = None

    @cherrypy.expose
    def index(self):
        return """
        <html><body>
            Hello """ \
               + str(cherrypy.request.login) + \
               """
               <h2>Upload a file</h2>
               <form action="upload" method="post" enctype="multipart/form-data">
               filename: <input type="file" name="myFile" /><br />
               <input type="submit" />
               </form>
           </body></html>
           """

    @cherrypy.expose
    def upload(self, myFile):
        out = """
        <html>
        <body>
            file length: %s<br />
            filename: %s<br />
            mime-type: %s

            <h2>Download flowchart</h2>
            <a href='download'>here</a>

            <br /><br />

            <h2>CherryPy Qml Reader Tools """ + str(__version__) + """</h2>
            Questionnaire.py """ + str(Questionnaire.__version__) + """<br>
            QmlReader.py """ + str(QmlReader.__version__) + """<br><br>

            <form action="download" method="post" enctype="multipart/form-data">
            <input type="button" value="download flowchart" />
            </form>


        </body>
        </html>"""

        error = """
        <html>
        <body>
            Error! File is either too large or not of type 'text/xml' <br><br>
            file length: %s<br />
            filename: %s<br />
            mime-type: %s  
        </body>
        </html>"""

        # Although this just counts the file length, it demonstrates
        # how to read large files in chunks instead of all at once.
        # CherryPy reads the uploaded file into a temporary file;
        # myFile.file.read reads from that.
        # size = len(myFile.file.read())

        size = 0
        permitted_size = 20971520
        #        data = myFile.file.read()
        #        print(help(data))
        #        print(dir(data))
        data = b''

        while True:
            tmp_data = myFile.file.read(8129)
            data += tmp_data
            if not tmp_data:
                break
            size += len(tmp_data)
            if size > permitted_size:
                break

        print(type(myFile.content_type))
        print(myFile.content_type)

        if size <= permitted_size and str(myFile.content_type) == 'text/xml':
            self.png_filename = QmlReader.QmlReader(filename=myFile.filename, file=data).png_filename
            return out % (size, myFile.filename, myFile.content_type)
        else:
            return error % (size, myFile.filename, myFile.content_type)

    @cherrypy.expose
    def qmlreadertools(self):
        out = """
            <html><body>

                <form action="upload" method="post" enctype="multipart/form-data">
                filename: <input type="file" name="myFile" /><br />
                <input type="submit" />
                </form>

                <form action="upload" method="post" enctype="multipart/form-data">
                filename: <input type="file" name="myFile" /><br />
                <input type="submit" />
                </form>

            <a href='secure'>here</a>
        </body></html>
        """
        return out

    @cherrypy.expose
    def download(self):
        path = os.path.join(absDir, 'flowcharts/' + self.png_filename)
        return static.serve_file(path, 'application/x-download',
                                 'attachment', os.path.basename(path))


if __name__ == '__main__':
    USERS = {}
    for key in config['users'].keys():
        USERS[key] = config['users'][key]

    alphabet = string.ascii_letters + string.digits
    digest_key = ''.join(secrets.choice(alphabet) for i in range(16))

    server_config = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080
    }
#        'server.ssl_module': 'pyOpenSSL',
#        'server.ssl_certificate': config['ssl']['certificate'],
#        'server.ssl_private_key': config['ssl']['key']

    conf = {
        '/secure': {
            'tools.auth_digest.on': True,
            'tools.auth_digest.realm': 'localhost',
            'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS),
            'tools.auth_digest.key': digest_key,
            'tools.auth_digest.accept_charset': 'UTF-8',
        }
    }

    # CherryPy accepting always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().

    root = LoginIndex()
    root.secure = FileDemo()
    cherrypy.config.update(server_config)
    cherrypy.quickstart(root, '/', conf)



