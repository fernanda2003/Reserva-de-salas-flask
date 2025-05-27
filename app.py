from flask import Flask
from database import db
from reserva_controller import reserva_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
db.init_app(app)

app.register_blueprint(reserva_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    

