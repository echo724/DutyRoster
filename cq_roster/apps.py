from django.apps import AppConfig


class CqRosterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cq_roster'
    
    def ready(self):
        import cq_roster.signals