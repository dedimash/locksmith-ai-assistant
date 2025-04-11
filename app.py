from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Locksmith AI Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }
            h1 { color: #2c3e50; }
            .container { max-width: 800px; margin: 0 auto; }
            .success { color: green; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Locksmith AI Assistant</h1>
            <p>The AI assistant is running successfully!</p>
            <p class="success">✓ Server is operational</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
