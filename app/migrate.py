from app import app, init_db
from app.db_models.example import Example

Example()

if __name__ == 'app.migrate':
    init_db(app)
