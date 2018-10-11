from app import app, init_db
from app.db_models.call import Call

Call()

if __name__ == 'app.migrate':
    init_db(app)
