import cherrypy


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"


if __name__ == '__main__':
    server_config = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8000,
    }

    cherrypy.config.update(server_config)
    cherrypy.quickstart(HelloWorld())
