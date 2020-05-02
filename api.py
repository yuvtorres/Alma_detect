from src.config import PORT
from src.app import app
import src.routes.usuarios
import src.routes.chats
import src.routes.mensajes
import src.routes.sentiments
import src.genera_chat.genera_chat

app.run("0.0.0.0", PORT, debug=True)
