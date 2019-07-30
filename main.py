from app import app
from posts.blueprint import posts

import view

app.register_blueprint(posts, url_prefix='/blog')

if __name__ == "__main__":
    app.run('127.0.0.1', '5000')
