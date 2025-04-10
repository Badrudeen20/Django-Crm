class MoviePlanetRouter:
    def db_for_read(self, model, **hints):
        """Read operations for movieplanet models."""
        if model._meta.app_label == 'movieplanet':
            return 'movieplanet'
        return 'default'

    def db_for_write(self, model, **hints):
        """Write operations for movieplanet models."""
        if model._meta.app_label == 'movieplanet':
            return 'movieplanet'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations only within the same database."""
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Only migrate movieplanet models to the movieplanet database."""
        if app_label == 'movieplanet':
            return db == 'movieplanet'
        # Prevent default Django tables from being created in movieplanet
        return db == 'default'
