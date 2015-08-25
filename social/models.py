from django.db import models

class Profile(models.Model):
    text = models.CharField(max_length=4096)

    def __str__(self):
        if self.member:
            return self.member.username + ": " + self.text
        return self.text

class Member(models.Model):
    username = models.CharField(max_length=16,primary_key=True)
    password = models.CharField(max_length=16)
    profile = models.OneToOneField(Profile, null=True)
    following = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.username

class Message(models.Model):
    author = models.ForeignKey(Member, related_name="author") # References a user in model Member
    recip = models.ForeignKey(Member, related_name="recip") # References a user in model Member
    private = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=4096)
	
    def __str__(self):
        return self.message