from django.db import models


# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=20)
    reputation=models.IntegerField()
    id=models.IntegerField(primary_key=True)

    def __str__(self):
        return "id: " + str(self.id)+" name: "+self.name +" reputation: "+str(self.reputation)

    class Meta:
        db_table='users'

class Questions(models.Model):
    question=models.CharField(max_length=150)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reputation = models.IntegerField()

    def __str__(self):
        return "question: "+self.question+" репутация: "+str(self.reputation)

    class Meta:
        db_table='questions'


class Respondent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)

    class Meta:
        db_table='respondents'