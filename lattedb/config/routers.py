# pylint: disable=W0212, W0613, C0103
"""Router maps for different database entries.
"""


class DBRouter:
    """A router to control all database operations on models in the `app` application.
    """

    app = None

    def db_for_read(self, model, **hints):
        """Attempts to read models go to `app` database.
        """
        print("read:", self, model, model._meta.app_label, self.app)
        if model._meta.app_label == self.app:
            print("success")
            return self.app
        return None

    def db_for_write(self, model, **hints):
        """Attempts to write models go to `app` database.
        """
        print("write:", self, model, model._meta.app_label, self.app)
        if model._meta.app_label == self.app:
            print("success")
            return self.app
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the app is involved.
        """
        if obj1._meta.app_label == self.app or obj2._meta.app_label == self.app:
            return True
        return None

    # def allow_migrate(self, db, app_label, model_name=None, **hints):
    #     """
    #     Make sure the auth app only appears in the 'auth_db'
    #     database.
    #     """
    #     if app_label == self.app:
    #         return db == self.app
    #     return None


class BaseRouter(DBRouter):
    """Router for `base` models"""

    app = "base"


class GaugeConfigRouter(DBRouter):
    """Router for `ensemble` models"""

    app = "ensemble"


class PropagatorRouter(DBRouter):
    """Router for `propagator` models"""

    app = "propagator"
