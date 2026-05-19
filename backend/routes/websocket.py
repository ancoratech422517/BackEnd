# routes/websocket.py
from flask_socketio import SocketIO
URL_FRONTEND_ANCORA = "https://ancoras.netlify.app"
socketio = SocketIO(
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1",
        "http://10.140.176.115:5173",
        "http://10.140.176.115",
        "http://10.140.176.115:5000",
        URL_FRONTEND_ANCORA,

    ],
    cookie='io',  # MUDOU: True -> 'io' ou remove a linha toda
    async_mode='threading',
    logger=True,
    engineio_logger=True
)
