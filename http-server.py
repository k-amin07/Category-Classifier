from http.server import BaseHTTPRequestHandler, HTTPServer
from ml_for_server import ml
import time
from urllib.parse import parse_qs
import json

hostName = "localhost"
serverPort = 4000

mlObj = None


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global mlObj
        if(self.path=='/init'):
            mlObj = ml()
            mlObj.read_data('') #to be replaced with db later
            mlObj.train()
            resp = '{"message": "OK", "staus":200}'
            resp = json.loads(resp)
            valid = True
        elif(self.path=='/train'):
            mlObj.train()
            resp = '{"message": "OK", "status":200}'
            resp = json.loads(resp)
            valid = True
        else:
            #A valid query is of the form /classify?q="I want you to mow my lawn"
            query = parse_qs(self.path)
            if(query):
                if(list(query.keys())[0].split('?')[0]=='/classify'):
                    resp = mlObj.classify(query[list(query.keys())[0]][0])
                    resp = resp.strip()
                    if(resp == 'ERROR ALERT!'):
                        resp = '{"category": "None", "status":500}'
                        resp = json.loads(resp)
                    else:
                        resp = '{"category": "' + resp + '", "status":200}'
                        resp = json.loads(resp)
                    print(resp)
                    valid=True
                else:
                    valid=False
                    resp='error'
            else:
                valid=False
        
        if(valid):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(resp), "utf-8"))
        else:
            self.send_response(404,message=None)
            self.end_headers()
            # self.wfile.write(bytes("Not found", "utf-8"))



        # self.send_response(200)
        # self.send_header("Content-type", "text/html")
        # self.end_headers()
        # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
