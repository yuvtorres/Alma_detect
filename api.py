from src.config import PORT
from src.app import app
import src.routes.usuarios
import src.routes.chats
import src.routes.mensajes

app.run("0.0.0.0", PORT, debug=True)
