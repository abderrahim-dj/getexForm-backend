from rest_framework import serializers
from ..models import (
  Company, Product, RawMaterial, PublicAgenciesAndServices,
  Causes_Of_Obstacles, Production_Obstacles
)

class ProductNestedSerializer(serializers.ModelSerializer):
  #Target_Audience_display = serializers.SerializerMethodField()
  
  class Meta:
    model = Product
    exclude = ['Company']


class RawMaterialSerializer(serializers.ModelSerializer):
  Source_display = serializers.SerializerMethodField()
  
  class Meta:
    model = RawMaterial
    exclude = ['Company']
  
  def get_Source_display(self, obj):
    return obj.get_Source_display()

class PublicAgenciesAndServicesSerializer(serializers.ModelSerializer):
  class Meta:
    model = PublicAgenciesAndServices
    exclude = ['Company']

class CausesOfObstaclesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Causes_Of_Obstacles
    fields = ['Obstacle']

class ProductionObstaclesSerializer(serializers.ModelSerializer):
  Reasons_For_Not_Achieving_Max_Capacity = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=Causes_Of_Obstacles.objects.all()
  )
  
  class Meta:
    model = Production_Obstacles
    fields = [
      'Reasons_For_Not_Achieving_Max_Capacity',
      'More_Obstacles'
    ]

class CompanySerializer(serializers.ModelSerializer):
  products = ProductNestedSerializer(many=True, required=False)
  raw_materials = RawMaterialSerializer(many=True, required=False)
  public_agencies_services = PublicAgenciesAndServicesSerializer(many=True, required=False)
  production_obstacles = ProductionObstaclesSerializer(many=True, required=False)
  Wilaya_display = serializers.SerializerMethodField()
  Legal_Form_display = serializers.SerializerMethodField()
  Legal_Status_display = serializers.SerializerMethodField()
  Origin_Ownership_display = serializers.SerializerMethodField()
  
  class Meta:
    model = Company
    
    fields = [
      'id',
      'Industry_Type',
      'Sector_Type',
      'Specialization',
      'First_Name',
      'Last_Name',
      'Wilaya',
      'Wilaya_display',
      'Commune',
      'Email',
      'Phone',
      'Name_Institution',
      'Activity',
      'Institution_Establishment_Year',
      'Start_Activity_Year',
      'Commercial_Registration_Number',
      'Tax_Identification_Number',
      'Legal_Form',
      'Legal_Form_display',
      'Legal_Status',
      'Legal_Status_display',
      'Number_Direct_Jobs',
      'Number_Indirect_Jobs',
      'Total_Covered_Storage_Area',
      'Total_Uncovered_Storage_Area',
      'Origin_Ownership',
      'Origin_Ownership_display',
      'Shortage_In_Raw_Material',
      'Benefit_From_Public_Agencies_Support',
      'products',
      'raw_materials',
      'public_agencies_services',
      'production_obstacles',
    ]
  
  def get_Wilaya_display(self, obj):
    return obj.get_Wilaya_display()
  
  def get_Legal_Form_display(self, obj):
    return obj.get_Legal_Form_display()
  
  def get_Legal_Status_display(self, obj):
    return obj.get_Legal_Status_display()
  
  def get_Origin_Ownership_display(self, obj):
    return obj.get_Origin_Ownership_display()
  
  def create(self, validated_data):
    products_data = validated_data.pop('products', [])
    raw_materials_data = validated_data.pop('raw_materials', [])
    public_agencies_services_data = validated_data.pop('public_agencies_services', [])
    production_obstacles_data = validated_data.pop('production_obstacles', [])
    
    company = Company.objects.create(**validated_data)
    
    for product_data in products_data:
      Product.objects.create(Company=company, **product_data)
    
    for raw_material_data in raw_materials_data:
      RawMaterial.objects.create(Company=company, **raw_material_data)
    
    for public_agency_service_data in public_agencies_services_data:
      PublicAgenciesAndServices.objects.create(
        Company=company,
        **public_agency_service_data
      )
    
    for production_obstacle_data in production_obstacles_data:
      reasons = production_obstacle_data.pop('Reasons_For_Not_Achieving_Max_Capacity', [])
      production_obstacle = Production_Obstacles.objects.create(
        Company=company,
        **production_obstacle_data
      )
      production_obstacle.Reasons_For_Not_Achieving_Max_Capacity.set(reasons)
    
    return company


class ProductSerializer(serializers.ModelSerializer):
  #Target_Audience_display = serializers.SerializerMethodField()
  
  class Meta:
    model = Product
    fields = '__all__'
  

""" 
class RawMaterialSerializer(serializers.ModelSerializer):
  Source_display = serializers.SerializerMethodField()
  
  class Meta:
    model = RawMaterial
    fields = '__all__'
  
  def get_Source_display(self, obj):
    return obj.get_Source_display()

class PublicAgenciesAndServicesSerializer(serializers.ModelSerializer):
  class Meta:
    model = PublicAgenciesAndServices
    fields = '__all__'

class CausesOfObstaclesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Causes_Of_Obstacles
    fields = ['Obstacle']

class ProductionObstaclesSerializer(serializers.ModelSerializer):
  Reasons_For_Not_Achieving_Max_Capacity = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=Causes_Of_Obstacles.objects.all()
  )
  
  class Meta:
    model = Production_Obstacles
    fields = [
      'Reasons_For_Not_Achieving_Max_Capacity',
      'More_Obstacles'
    ] """