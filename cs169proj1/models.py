from django.db import models

# Create your models here.

SUCCESS = 1 
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS = -2
ERR_BAD_USERNAME = -3
ERR_BAD_PASSWORD = -4

MAX_PASSWORD_LENGTH = 128
MAX_USERNAME_LENGTH = 128

class UsersModel(models.Model):
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH)
    user = models.CharField(max_length=MAX_USERNAME_LENGTH)
    count = models.IntegerField()
    
    def __unicode__(self):
        return "user: %s, password: %s" % (self.user, self.password)
    
    @classmethod
    def login(cls, user, password):
        User = cls.objects.filter(user=user, password=password)[0]
        if not User:
            return ERR_BAD_CREDENTIALS
        else:
            User.count = User.count + 1
            User.save()
            return User.count
        
    @classmethod
    def add(cls, user, password):
        if not user:
            return ERR_BAD_USERNAME
        if len(password) > MAX_PASSWORD_LENGTH:
            return ERR_BAD_PASSWORD
        if cls.objects.filter(user=user):
            return ERR_USER_EXISTS
        else:
            newUser = cls(user=user, password=password)
            newUser.count = 1
            newUser.save()
            return newUser.count
        
    @classmethod
    def TESTAPI_resetFixture(cls):
        for user in cls.objects.all():
            user.delete()
        return SUCCESS
        