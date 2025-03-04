from rest_framework.views import APIView
from ..models import Company
from .serializers import CompanySerializer, ProductSerializer, RawMaterialSerializer, PublicAgenciesAndServicesSerializer, ProductionObstaclesSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .filters import CompanyFilter #ProductionObstaclesFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuserActiveStaff
import csv
from django.http import HttpResponse


#Just for testing

class Test(APIView):
  
  def get(self, request):
    
    data = {
      "message": "This is a test API response!",
      "status": "success",
      "data": {
          "example_key": "example_value"
      }
    }
    return Response(data)



# for form submission
class CompanyCreateView(generics.CreateAPIView):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  
  def perform_create(self, serializer):
    serializer.save()
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



#Get the data for all the companys we have
class CompanyListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated, IsSuperuserActiveStaff]
  queryset = Company.objects.all().prefetch_related(
    'products',
    'raw_materials',
    'public_agencies_services',
    'production_obstacles'
  )
  serializer_class = CompanySerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_class = CompanyFilter  # Apply the filter class
  #search_fields = ['^Wilaya',]  # Optional: Add search fields
  ordering_fields = ['Start_Activity_Year', 'Number_Direct_Jobs', 'Number_Indirect_Jobs', 'Legal_Form', 'Target_Audience', 'Source', 'Total_Covered_Storage_Area', 'Total_Uncovered_Storage_Area']



#Get the company detail by ID
class CompanyDetailView(generics.RetrieveAPIView):
  permission_classes = [IsAuthenticated, IsSuperuserActiveStaff]
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.serializer_class(instance)
    
    # Include nested data explicitly if needed
    data = serializer.data
    data['products'] = ProductSerializer(instance.products.all(), many=True).data
    data['raw_materials'] = RawMaterialSerializer(instance.raw_materials.all(), many=True).data
    data['public_agencies_services'] = PublicAgenciesAndServicesSerializer(instance.public_agencies_services.all(), many=True).data
    data['production_obstacles'] = ProductionObstaclesSerializer(instance.production_obstacles.all(), many=True).data
    
    return Response(data)






#export all data as CSV with French field names
class ExportAllDataCSV(APIView):
  
  permission_classes = [IsAuthenticated, IsSuperuserActiveStaff]
  
  def get(self, request, format=None):
    # Create HTTP response with CSV content type and UTF-8 encoding
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="all_data.csv"'
    # Write BOM for UTF-8 (helpful for Excel to display Arabic/French characters properly)
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    
    # Write header row with French field names.
    writer.writerow([
      "ID de la Société",
      "Nom de l'Institution",
      "Type de Secteur",
      "Origine de Propriété",
      "Spécialisation",
      "Type d'Industrie",
      "Activité",
      "Wilaya",
      "Commune",
      "Prénom",
      "Nom",
      "E-mail",
      "Téléphone",
      "Année d'établissement de l'Institution",
      "Année de Début d'Activité",
      "Numéro d'Enregistrement Commercial",
      "Numéro d'Identification Fiscale",
      "Forme Juridique",
      "Statut Juridique",
      "Nombre d'Emplois Directs",
      "Nombre d'Emplois Indirects",
      "Surface Totale Couvert en mètre carré",
      "Surface Totale Non Couvert en mètre carré",
      "Pénurie en Matières Premières",
      "Bénéficie du Soutien des Agences Publiques",
      "Produits",
      "Matières Premières",
      "Agences Publiques",
      "Obstacles de Production",
    ])
    
    # Use prefetch_related to optimize related queries.
    companies = Company.objects.all().prefetch_related(
      'products', 
      'raw_materials', 
      'public_agencies_services', 
      'production_obstacles__Reasons_For_Not_Achieving_Max_Capacity'
    )
    
    for company in companies:
      # Company basic fields.
      company_id = company.id
      industry_type = company.Industry_Type
      sector_type = company.Sector_Type
      specialization = company.Specialization
      first_name = company.First_Name
      last_name = company.Last_Name
      wilaya = company.get_Wilaya_display() if hasattr(company, 'get_Wilaya_display') else company.Wilaya
      commune = company.Commune
      email = company.Email
      phone = company.Phone
      name_institution = company.Name_Institution
      activity = company.Activity
      institution_year = company.Institution_Establishment_Year
      start_year = company.Start_Activity_Year
      commercial_reg = company.Commercial_Registration_Number
      tax_id = company.Tax_Identification_Number
      legal_form = company.get_Legal_Form_display() if hasattr(company, 'get_Legal_Form_display') else company.Legal_Form
      legal_status = company.get_Legal_Status_display() if hasattr(company, 'get_Legal_Status_display') else company.Legal_Status
      direct_jobs = company.Number_Direct_Jobs
      indirect_jobs = company.Number_Indirect_Jobs
      covered_area = company.Total_Covered_Storage_Area
      uncovered_area = company.Total_Uncovered_Storage_Area
      origin_ownership = company.get_Origin_Ownership_display() if hasattr(company, 'get_Origin_Ownership_display') else company.Origin_Ownership
      shortage = company.Shortage_In_Raw_Material
      benefit = company.Benefit_From_Public_Agencies_Support
      
      # Aggregate Products: join all product fields.
      products_data = []
      for product in company.products.all():
        products_data.append(
          f"Nom: {product.Product_Name}, "
          f"Capacité: {product.Production_Capacity_Monthly}, "
          f"Volume Réel: {product.Actual_Production_Volume}, "
          f"Volume Unit: {product.Actual_Production_Unit}, "
          f"Marché Cible: {product.Target_Market}, "
          f"Public Cible: {product.Target_Audience}"
        )
      products_str = " | ".join(products_data)
        
      # Aggregate Raw Materials.
      raw_materials_data = []
      for raw in company.raw_materials.all():
        raw_materials_data.append(
          f"Matière Première: {raw.Raw_Material}, "
          f"Consommation Mensuelle: {raw.Monthly_Consumption}, "
          f"Source: {raw.get_Source_display() if hasattr(raw, 'get_Source_display') else raw.Source}, "
          f"Pays Source: {raw.Source_Country}, "
          f"Est Rare: {raw.Is_Scarce}, "
          f"Quantités Requises: {raw.Quantities_Required_To_Reach_Maximum_Production_Capacity_Monthly}"
        )
      raw_materials_str = " | ".join(raw_materials_data)
        
      # Aggregate Public Agencies.
      public_agencies_data = []
      for pa in company.public_agencies_services.all():
        public_agencies_data.append(pa.List_Agencies_And_Services)
      public_agencies_str = " | ".join(public_agencies_data)
        
      # Aggregate Production Obstacles.
      production_obstacles_data = []
      for po in company.production_obstacles.all():
        reasons = ", ".join([reason.Obstacle for reason in po.Reasons_For_Not_Achieving_Max_Capacity.all()])
        production_obstacles_data.append(
          f"Obstacles Supplémentaires: {po.More_Obstacles}, Raisons: {reasons}"
        )
      production_obstacles_str = " | ".join(production_obstacles_data)
        
      writer.writerow([
        company_id,                
        name_institution,          
        sector_type,               
        origin_ownership,          
        specialization,           
        industry_type,             
        activity,                  
        wilaya,                    
        commune,                   
        first_name,               
        last_name,                 
        email,                   
        phone,                     
        institution_year,          
        start_year,                
        commercial_reg,            
        tax_id,                    
        legal_form,                
        legal_status,              
        direct_jobs,               
        indirect_jobs,            
        covered_area,              
        uncovered_area,            
        shortage,                  
        benefit,                   
        products_str,              
        raw_materials_str,         
        public_agencies_str,       
        production_obstacles_str  
      ])
    
    return response


########################################################################################################################################
#comment sections




#Get the data for all the companys we have
#old one
""" 
class CompanyListView(generics.ListAPIView):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  
  def list(self, request, *args, **kwargs):
    companies = self.get_queryset()
    serializer = self.serializer_class(companies, many=True)
    
    # Include additional related data (optional)
    products = Product.objects.all()
    raw_materials = RawMaterial.objects.all()
    public_agencies = PublicAgenciesAndServices.objects.all()
    production_obstacles = Production_Obstacles.objects.all()
    
    return Response({
      'companies': serializer.data,
      #for extra data like get all the Product and then can filter them by companyID
      #'products': ProductSerializer(products, many=True).data,
      #'raw_materials': RawMaterialSerializer(raw_materials, many=True).data,
      #'public_agencies': PublicAgenciesAndServicesSerializer(public_agencies, many=True).data,
      #'production_obstacles': ProductionObstaclesSerializer(production_obstacles, many=True).data
    })
"""



#Get the data for all the companys we have
#old one
""" 
class CompanyListView(generics.ListAPIView):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  
  def list(self, request, *args, **kwargs):
    companies = self.get_queryset()
    serializer = self.serializer_class(companies, many=True)
    
    # Include additional related data (optional)
    products = Product.objects.all()
    raw_materials = RawMaterial.objects.all()
    public_agencies = PublicAgenciesAndServices.objects.all()
    production_obstacles = Production_Obstacles.objects.all()
    
    return Response({
      'companies': serializer.data,
      #for extra data like get all the Product and then can filter them by companyID
      #'products': ProductSerializer(products, many=True).data,
      #'raw_materials': RawMaterialSerializer(raw_materials, many=True).data,
      #'public_agencies': PublicAgenciesAndServicesSerializer(public_agencies, many=True).data,
      #'production_obstacles': ProductionObstaclesSerializer(production_obstacles, many=True).data
    })
"""


"""
#this class is for fitring the products obstacles by the companys
class ProductionObstaclesListView(generics.ListAPIView):
  queryset = Production_Obstacles.objects.all().select_related('Company').prefetch_related('Reasons_For_Not_Achieving_Max_Capacity')
  serializer_class = ProductionObstaclesSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_class = ProductionObstaclesFilter  # Apply the filter class
"""