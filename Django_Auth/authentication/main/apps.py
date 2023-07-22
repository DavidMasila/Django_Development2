from django.apps import AppConfig
from django.conf import settings

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    #making the new sign ups to be automatically assigned to default group
    #when the app is ready make imports
    def ready(self):
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_save

        def add_to_default_group(sender, **kwargs):
            user = kwargs["instance"]
            if kwargs['created']:
                #create or get the default group
                group, ok = Group.objects.get_or_create(name='default')
                #add the user to the group >> group.user_set.add(user)
                group.user_set.add(user)

        post_save.connect(add_to_default_group, 
                          sender=settings.AUTH_USER_MODEL)