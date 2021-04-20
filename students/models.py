from django.db import models
import calendar, time

# Create your models here.
class StudentInfo(models.Model):
    id = models.CharField(primary_key=True,editable=False,max_length=200)
    GENDER_CHOICES=(
        ('male', 'Male'),
        ('female', 'Female'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    registeration_num = models.CharField(max_length=100)
    admission_date = models.DateTimeField()
    gender = models.CharField(choices=GENDER_CHOICES,max_length=10)
    created_dt = models.DateTimeField(verbose_name="created date", auto_now_add=True)
    modify_dt = models.DateTimeField(verbose_name="modified date", auto_now=True)


    def save(self, **kwargs):
        gmt = time.gmtime()
        dt = calendar.timegm(gmt)
        if not self.id:
            self.id = "{}{}{}".format(self.first_name[0],self.last_name[0],str(dt))
        super().save(**kwargs)

    def __str__(self):
        return self.id +" "+self.first_name +" "+self.last_name
    
