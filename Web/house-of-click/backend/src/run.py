import clickhouse_connect
import ipaddress
import web
import os

with open('.token', 'r') as f:
    TOKEN = f.read()

urls = (
    '/', 'Index',
    '/query', 'Query',
    '/api/ping', 'Ping',
    '/api/token', 'Token',
    '/api/upload', 'Upload',
)

render = web.template.render('templates/')


def check_ip(ip, ip_range):
    return ipaddress.ip_address(ip) in ipaddress.ip_network(ip_range)


class Index:
    def GET(self):
        return render.index()

    def POST(self):
        data = web.input(name='index')
        return render.__getattr__(data.name)()


class Query:
    def POST(self):
        data = web.input(id='1')

        client = clickhouse_connect.get_client(host='db', port=8123, username='default', password='default')
        sql = 'SELECT * FROM web.users WHERE id = ' + data.id
        client.command(sql)
        client.close()
        
        return 'ok'


class Ping:
    def GET(self):
        return 'pong'


class Token:
    def GET(self):
        ip = web.ctx.env.get('REMOTE_ADDR')
        if not check_ip(ip, '172.28.0.0/16'):
            return 'forbidden'
        return TOKEN


class Upload:
    def POST(self):
        ip = web.ctx.env.get('REMOTE_ADDR')
        token = web.ctx.env.get('HTTP_X_ACCESS_TOKEN')

        if not check_ip(ip, '172.28.0.0/16'):
            return 'forbidden'
        if token != TOKEN:
            return 'unauthorized'
    
        files = web.input(myfile={})
        if 'myfile' in files:
            filepath = os.path.join('upload/', files.myfile.filename)
            if (os.path.isfile(filepath)):
                return 'error'
            with open(filepath, 'wb') as f:
                f.write(files.myfile.file.read())
        return 'ok'    


app = web.application(urls, globals())
application = app.wsgifunc(web.httpserver.StaticMiddleware)