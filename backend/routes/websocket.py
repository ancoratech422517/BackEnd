# routes/websocket.py
from flask_socketio import SocketIO

socketio = SocketIO(
    logger=True,
    engineio_logger=True,
    async_mode='gevent',
    cors_allowed_origins=[          # CORRIGIDO: lista explícita em vez de "*"
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.11.1:5173",
        "http://10.140.176.115:5173",
        "https://loja-penelaka.netlify.app"
    ]
)
