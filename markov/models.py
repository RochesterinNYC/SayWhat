from django.db import models

class User(models.Model):
  groupme_uid = models.CharField(max_length=100)
  access_token = models.CharField(max_length=100)
  name = models.CharField(max_length=200)
  def __str__(self):  
    return "{} {}".format(self.groupme_uid, self.name)