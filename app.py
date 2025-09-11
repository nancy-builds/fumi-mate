# Web Server Gateway Interface: in application platform, not dev
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
