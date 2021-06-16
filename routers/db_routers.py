class AuthRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'user_db'
        return None
   

    def allow_syncdb(self, db, model):
        if db == 'user_db':
            return model._meta.app_label == 'auth'
        elif model._meta.app_label == 'auth':
            return False
        return None

class OtherRouter(object):
    def db_for_read(self, model, **hints):
        return "default"