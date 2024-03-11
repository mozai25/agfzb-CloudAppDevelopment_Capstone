from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview  


# Register your models here.

admin.site.register(CarModel)
admin.site.register(CarMake)

# CarModelInline class
#class CarModelInline(admin.StackedInline):
#    model = CarModel 
#    extra = 5

#class CarMakeInline (CarMake):
#    inlines = [CarModelInline]

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
