from django.contrib import admin
from .models import Company, Product, RawMaterial, PublicAgenciesAndServices, Causes_Of_Obstacles, Production_Obstacles


class CompanyAdmin(admin.ModelAdmin):
  list_display = ('Name_Institution', 'Activity', 'Legal_Form', 'Wilaya')
  list_filter = ('Activity', 'Legal_Form', 'Wilaya')

class ProductAdmin(admin.ModelAdmin):
  list_display = ('Product_Name', 'Company', 'Target_Audience')
  list_filter = ('Company', 'Target_Audience')


class RawMaterialAdmin(admin.ModelAdmin):
  list_display = ('Raw_Material', 'Source', 'Source_Country', 'Company')
  list_filter = ('Company', 'Source', 'Source_Country')


class PublicAgenciesAndServicesAdmin(admin.ModelAdmin):
  list_display = ('List_Agencies_And_Services', 'Company')
  list_filter = ('Company',)


class Causes_Of_ObstaclesAdmin(admin.ModelAdmin):
  list_display = ('Obstacle',)
  list_filter = ('Obstacle',)


class Production_ObstaclesAdmin(admin.ModelAdmin):
  list_display = ('Company', 'More_Obstacles')
  list_filter = ('Company',)
  filter_horizontal = ('Reasons_For_Not_Achieving_Max_Capacity',)



# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RawMaterial, RawMaterialAdmin)
admin.site.register(PublicAgenciesAndServices, PublicAgenciesAndServicesAdmin)
admin.site.register(Causes_Of_Obstacles, Causes_Of_ObstaclesAdmin)
admin.site.register(Production_Obstacles, Production_ObstaclesAdmin)