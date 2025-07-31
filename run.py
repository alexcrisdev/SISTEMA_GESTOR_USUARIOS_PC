from flask import Flask
from app.controllers.controller_usuario import usuario_bp
from app.controllers.controller_area import area_bp
from app.controllers.controller_computadora import computadora_bp

app = Flask(__name__)
app.register_blueprint(usuario_bp)
app.register_blueprint(area_bp)
app.register_blueprint(computadora_bp)

if __name__=='__main__':
    app.run(debug=True)