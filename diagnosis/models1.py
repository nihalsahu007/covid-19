from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

profile_choice = (
    ('STUDENT', 'STUDENT'),
    ('WORKING', 'WORKING'),
    ('RETIRED', 'RETIRED'),
)
state_choices = (("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), ("Assam", "Assam"), ("Bihar", "Bihar"), ("Chhattisgarh", "Chhattisgarh"), ("Goa", "Goa"), ("Gujarat", "Gujarat"), ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"), ("Jammu and Kashmir ", "Jammu and Kashmir "), ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"), ("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"), ("Maharashtra", "Maharashtra"), ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"), ("Nagaland", "Nagaland"), ("Odisha", "Odisha"),
                 ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"), ("Sikkim", "Sikkim"), ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), ("Tripura", "Tripura"), ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), ("West Bengal", "West Bengal"), ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), ("Chandigarh", "Chandigarh"), ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), ("Daman and Diu", "Daman and Diu"), ("Lakshadweep", "Lakshadweep"), ("National Capital Territory of Delhi", "National Capital Territory of Delhi"), ("Puducherry", "Puducherry"))


class data_base(models.Model):

	name = models.CharField(max_length=128, blank=False)
	phone = models.IntegerField(
	    validators=[MaxValueValidator(9999999999), MinValueValidator(6000000000)])
	email = models.EmailField(max_length=70, blank=False)
	age = models.IntegerField(
	    validators=[MaxValueValidator(100), MinValueValidator(1)])
    street=models.CharField(max_length=128,blank=False)
	city=models.CharField(max_length=100,blank=False)
	state=models.CharField(max_length=128,choices=state_choices,blank=False)
	profile=models.CharField(max_length=20,choices=profile_choice,blank=False)
	organisation=models.CharField(max_length=150,blank=False)
    travelHistory=models.CharField(max_length=50)
	fever=models.IntegerField(default=0)
	bodyPain=models.IntegerField(default=0)
	runningNose=models.IntegerField(default=0)
	diffBreath=models.IntegerField(default=0)
    soreThroat=models.IntegerField(default=0)
	infectionProb=models.FloatField(default=0)
    
    	
	def __str__(self):
		return self.name+' '+self.city
# civid_Result=models.IntegerField(choices=bool_choice,default=0)
