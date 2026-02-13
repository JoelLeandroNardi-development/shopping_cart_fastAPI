import importlib

def import_user_model_without_relationship():
    import sqlalchemy.orm as _orm

    original_relationship = _orm.relationship

    def _noop_relationship(*args, **kwargs):
        return None

    _orm.relationship = _noop_relationship
    try:
        mod = importlib.import_module("app.users.model")
        importlib.reload(mod)
    finally:
        _orm.relationship = original_relationship

    return mod.User