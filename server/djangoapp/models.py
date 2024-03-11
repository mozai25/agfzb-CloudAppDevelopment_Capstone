from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50, default='BMW')
    description = models.CharField(null=False, max_length=250, default='BMW - luxury car')
    
#   power = models.CharField(null=False, max_length=10, default='300hp')

    def __str__(self):
        return self.name + " " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    name = models.CharField(null=False, max_length=50, default='BMW 525')
    year = models.DateField(null=False, max_length=50, default='2022')
    make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    SEDAN = 'audit'
    SUV = 'honor'
    WAGON = 'wagon'
    CARS_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon'),
    ]
    car_type = models.CharField(null=False, choices=CARS_TYPES, max_length=50, default='Sedan')

    def __str__(self):
        return self.name + " " + self.year + " " + self.make + " " + self.dealerId + " " + self.car_type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(): 
    
    def __init__(self, id, city, state, st, address, zip, lat, long,short_name, full_name):
       self.id = id
       self.city = city
       self.state = state
       self.st = st
       self.address = address
       self.zip = zip
       self.lat = lat
       self.long = long
       self.short_name = short_name
       self.full_name = full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(): 
    
    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year):
        self.id = id
        self.name = name
        self.dealer = dealer
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        