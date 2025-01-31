from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib

BOLD_SECRET_KEY = "RtAdKZJgfYPf1y_JY1E5Sw"

def generate_bold_signature(order_id, amount):
    # Concatenar exactamente como dice la documentación, sin espacios ni caracteres adicionales
    message = f"{order_id}{amount}COP{BOLD_SECRET_KEY}"
    print("\n=== DEBUG INFO ===")
    print(f"Order ID: {order_id}")
    print(f"Amount: {amount}")
    print(f"Message to hash: {message}")
    
    # Generar hash SHA256
    hash_object = hashlib.sha256(message.encode('utf-8'))
    signature = hash_object.hexdigest()
    print(f"Generated signature: {signature}")
    print("================\n")
    return signature

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path.startswith('/generate-hash/'):
            # Extraer los parámetros de la URL
            params = self.path.split('/')[-1].split(',')
            order_id = params[0]
            amount = params[1]
            
            signature = generate_bold_signature(order_id, amount)
            
            response = {
                'signature': signature,
                'order_id': order_id,
                'amount': amount
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            response = {'message': 'Server is working!'}
            self.wfile.write(json.dumps(response).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        run(port=5000)
    except OSError:
        print("Port 5000 is in use, trying port 5001...")
        run(port=5001) 