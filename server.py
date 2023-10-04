import http.server
import socketserver
import mysql.connector
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

# Specify the port you want to use
port = 8000

# Database connection details
db_config = {
    "host": "sql.freedb.tech",
    "user": "",
    "password": "",
    "database": "",
}

# Create a MySQL connection
try:
    db_connection = mysql.connector.connect(**db_config)
    if db_connection.is_connected():
        print("Connected to MySQL database")
    else:
        print("Failed to connect to MySQL database")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    db_connection = None

# Create a function to execute a query and return the result
def execute_query(query):
    if db_connection:
        cursor = db_connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
        finally:
            cursor.close()

# Create a Jinja2 environment for rendering HTML templates
env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html"])
)

# Define a custom request handler
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(".css") or self.path.endswith(".js") or self.path.endswith(".png"):
            # Serve static files directly
            super().do_GET()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if self.path == "/index":
                template_name = "index.html"
            elif self.path == "/about":
                template_name = "about.html"
            elif self.path == "/contact":
                template_name = "contact.html"
            elif self.path == "/template":
                template_name = "template.html"
            else:
                self.send_error(404, "Page not found")
                return

            template = env.get_template(template_name)
            data = execute_query("SELECT id, content, author FROM content")
            rendered_html = template.render(data=data)

            self.wfile.write(rendered_html.encode())

# Create a simple HTTP server with the custom handler
with socketserver.TCPServer(("", port), CustomHandler) as httpd:
    print(f"Serving at port {port}")
    httpd.serve_forever()
