import django_filters
from ..models import Company, Production_Obstacles, Causes_Of_Obstacles

#filtering companys model
class CompanyFilter(django_filters.FilterSet):
  
  # Fitring
  Wilaya = django_filters.CharFilter(
    field_name="Wilaya",
    lookup_expr="exact",
    help_text="Filter companies by Wilaya (exact match)"
  )
  
  
  Legal_Form = django_filters.CharFilter(
    field_name="Legal_Form",
    lookup_expr="exact",
    help_text="Filter companies by Legal Form (exact match)"
  )
  
  
  Number_Direct_Jobs = django_filters.NumberFilter(
    field_name="Number_Direct_Jobs",
    lookup_expr="gte",  # "greater than"
    help_text="Filter companies with equal or more than X direct jobs"
  )
  
  
  Start_Activity_Year = django_filters.NumberFilter(
    field_name="Start_Activity_Year",
    lookup_expr="gte",  # "greater than or equal to"
    help_text="Filter companies started on or equal of after this date"
  )
  
  
  Total_Covered_Storage_Area = django_filters.NumberFilter(
    field_name="Total_Covered_Storage_Area",
    lookup_expr="gte",  # "greater than or equal to"
    help_text="Filter companies total covered storage area on or equal of after this date"
  )
  
  
  Total_Uncovered_Storage_Area = django_filters.NumberFilter(
    field_name="Total_Uncovered_Storage_Area",
    lookup_expr="gte",  # "greater than or equal to"
    help_text="Filter companies total uncovered storage area on or equal of after this date"
  )
  
  
  class Meta:
    model = Company
    fields = {
      'Wilaya': ['exact'],
      'Legal_Form': ['exact'],
      'Number_Direct_Jobs': ['gte'],  
      'Start_Activity_Year': ['gte'],  
      'Total_Covered_Storage_Area': ['gte'],
      'Total_Uncovered_Storage_Area': ['gte'],
    }


#for fitring the obstacle based on companies
""" class ProductionObstaclesFilter(django_filters.FilterSet):
  Reasons_For_Not_Achieving_Max_Capacity = django_filters.ModelMultipleChoiceFilter(
    field_name="Reasons_For_Not_Achieving_Max_Capacity",
    queryset=Causes_Of_Obstacles.objects.all(),
    lookup_expr="in",  # Filter by multiple obstacle IDs
    help_text="Filter production obstacles by reasons (comma-separated list of IDs)"
  )
    
  class Meta:
    model = Production_Obstacles
    fields = {
      'Reasons_For_Not_Achieving_Max_Capacity':['in']
    } """