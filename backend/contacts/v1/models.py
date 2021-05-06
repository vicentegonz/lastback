from django.db import models

class AdminUserManager(models.UserManager):
    def get_queryset(self):
        return super(AdminUserManager, self).get_queryset().filter(role=0)

class ZoneLeaderUserManager(models.UserManager):
    def get_queryset(self):
        return super(ZoneLeaderuserManager, self).get_queryset().filter(role=1)

class AdminUser(models.User):
    objects = AdminUserManager()
    class Meta:
        proxy = True
    
class ZoneLeaderUser(models.User):
    objects = ZoneLeaderUserManager()
    class Meta:
        proxy = True
