from .rooms import rooms_bp
from .votes import votes_bp

def register_routes(app):
    """全てのBlueprintを登録"""
    app.register_blueprint(rooms_bp)
    app.register_blueprint(votes_bp)

__all__ = ['register_routes']
