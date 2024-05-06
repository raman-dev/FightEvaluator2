from django.apps import AppConfig


class FightevaluatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fightEvaluator'

    def ready(self):
        print('------------------------------')
        print('| READY METHOD EXECUTING !!! |')
        print('------------------------------')
