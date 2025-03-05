from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json 
import threading
import traceback
import bpy

bl_info = {
    "name": "Blender_HTTP_Server",
    "author": "Igor S. Kurilov",
    "version": (1, 0),
    "blender": (2, 8, 0),
    "description": "Creates HTTP server allowing to execute python scripts in context of Blender. ",
    "category": "Object"
}

bpyHttpServerObject = None

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/version':
            result = { 'result': str(bl_info['version'][0]) + '.' + str(bl_info['version'][1]) }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found\t')


    def do_POST(self):
        handler = None
        if self.path == '/exec':
            handler = self.exec_script
        elif self.path == '/eval':
            handler = self.eval_script
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found\t')


        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode()
        try:
            result = { 'result': handler(post_body) }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except:
            import traceback
            result = { 'error': traceback.format_exc() }
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

    def eval_script(self, script):
        return eval(compile(script, 'remote_eval_script', 'eval'))


    def exec_script(self, script):
        filepath = 'remote_exec_script'
        global_namespace = {}
        global_namespace.update(globals())
        global_namespace["__file__"] = filepath
        global_namespace["__name__"] = "__main__"
        exec(compile(script, filepath, 'exec'), global_namespace)

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class BpyHttpServer:

    def start(self):
        self.server = ThreadingSimpleServer(('localhost', 8088), Handler)
        self.serverThread = threading.Thread(None, self.server.serve_forever)
        self.serverThread.start()

    def close(self):
        self.server.server_close()
        self.serverThread.join()    

def register():
    global bpyHttpServerObject
    if bpyHttpServerObject is None:
        bpyHttpServerObject = BpyHttpServer()
        bpyHttpServerObject.start()

def unregister():
    global bpyHttpServerObject
    if bpyHttpServerObject is not None:
        bpyHttpServerObject.close()
        bpyHttpServerObject = None

if __name__ == "__main__":
    register()
