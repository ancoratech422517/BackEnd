from routes.api_auth import login_bp
from flask import jsonify , make_response

@login_bp.route("/Logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"status": "True", "menssagem": "Deslogado"}))
    resp.delete_cookie("token_sessao", samesite="Lax")
    return resp