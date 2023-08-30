from django.db import models

# Create your models here.

Gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
Courses = (
    ('Python kick start', 'Python kick start'),
    ('Python Champ', 'Python Champ'),
    ('Python Advance', 'Python Advance'),
    ('Python Professional', 'Python Professional'),
)


# Create your models here.
class StudentModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10, default="Male", choices=Gender)
    mobile_no = models.BigIntegerField()
    email = models.EmailField(max_length=100)
    courses = models.CharField(max_length=100, choices=Courses)
    date = models.DateField(auto_now=True)
    city = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='images', blank=True, null=True)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.first_name


class ContactModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    interested = models.BooleanField(default=False, choices=((True, 'True'), (False, 'False')))
    called = models.BooleanField(default=False, choices=((True, 'True'), (False, 'False')))

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return self.first_name


class SubscribeModel(models.Model):
    email = models.EmailField(max_length=100, unique=True)

    class Meta:
        db_table = 'subscribe'

    def __str__(self):
        return self.email



