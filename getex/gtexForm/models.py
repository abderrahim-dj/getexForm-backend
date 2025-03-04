from django.db import models

# Create your models here.


#For table 1 Company

Wilaya_Choices = [
  ('1', "Adrar"),
  ('2', "Chlef"),
  ('3', "Laghouat"),
  ('4', "Oum El Bouaghi"),
  ('5', "Batna"),
  ('6', "Béjaïa"),
  ('7', "Biskra"),
  ('8', "Béchar"),
  ('9', "Blida"),
  ('10', "Bouira"),
  ('11', "Tamanrasset"),
  ('12', "Tébessa"),
  ('13', "Tlemcen"),
  ('14', "Tiaret"),
  ('15', "Tizi Ouzou"),
  ('16', "Alger"),
  ('17', "Djelfa"),
  ('18', "Jijel"),
  ('19', "Sétif"),
  ('20', "Saïda"),
  ('21', "Skikda"),
  ('22', "Sidi Bel Abbès"),
  ('23', "Annaba"),
  ('24', "Guelma"),
  ('25', "Constantine"),
  ('26', "Médéa"),
  ('27', "Mostaganem"),
  ('28', "M'Sila"),
  ('29', "Mascara"),
  ('30', "Ouargla"),
  ('31', "Oran"),
  ('32', "El Bayadh"),
  ('33', "Illizi"),
  ('34', "Bordj Bou Arréridj"),
  ('35', "Boumerdès"),
  ('36', "El Tarf"),
  ('37', "Tindouf"),
  ('38', "Tissemsilt"),
  ('39', "El Oued"),
  ('40', "Khenchela"),
  ('41', "Souk Ahras"),
  ('42', "Tipaza"),
  ('43', "Mila"),
  ('44', "Aïn Defla"),
  ('45', "Naâma"),
  ('46', "Aïn Témouchent"),
  ('47', "Ghardaïa"),
  ('48', "Relizane"),
  ('49', "Timimoun"),
  ('50', "Bordj Badji Mokhtar"),
  ('51', "Ouled Djellal"),
  ('52', "Béni Abbès"),
  ('53', "In Salah"),
  ('54', "In Guezzam"),
  ('55', "Touggourt"),
  ('56', "Djanet"),
  ('57', "El M'Ghair"),
  ('58', "El Meniaa"),
]


Legal_Form_Choices = [
  ('1', 'SPA'),
  ('2', 'SARL'),
  ('3', 'EURL'),
  ('4', 'SNC'),
  ('5', 'SCS'),
  ('6', 'ARTISANT'),
  ('7', 'AUTRES'),
]


Legal_Status_Choices = [
  ('1', 'Publique'),
  ('2', 'Privé'),
  ('3', 'Mixte(nationale/étrangère)')
]

Origin_Ownership_Choices = [
  ('1', 'عقد امتياز '),
  ('2', 'كراء'),
  ('3', 'خاصة')
]

#For table 2 Product

#was choice in Target_Audience
Target_Audience_Choices = [
  ('1', 'آخر'),
  ('2', 'أطفال'),
  ('3', 'نساء'),
  ('4', 'رجال')
  ]




#For table 3 Product
Source_Choices = [
  ('1', 'مستورد'),
  ('2', 'محلي')
]

class Company(models.Model):
  #the first 3 questions
  Industry_Type = models.CharField(max_length=20)
  Sector_Type = models.CharField(max_length=50)
  Specialization = models.CharField(max_length=50)
  
  #The rest of form
  
  First_Name =  models.CharField(max_length=100)
  Last_Name = models.CharField(max_length=100)
  Wilaya = models.CharField(max_length=100, choices=Wilaya_Choices)
  Commune = models.CharField(max_length=100)
  Email = models.EmailField()
  Phone = models.CharField(max_length=20)
  Name_Institution = models.CharField(max_length=250)
  Activity = models.CharField(max_length=250)
  Institution_Establishment_Year = models.IntegerField()
  Start_Activity_Year = models.IntegerField()
  Commercial_Registration_Number = models.CharField(max_length=30)
  Tax_Identification_Number = models.CharField(max_length=30)
  Legal_Form = models.CharField(max_length=20, choices=Legal_Form_Choices)
  Legal_Status = models.CharField(max_length=30, choices=Legal_Status_Choices)
  Number_Direct_Jobs = models.IntegerField()
  Number_Indirect_Jobs = models.IntegerField()
  Total_Covered_Storage_Area = models.IntegerField()
  Total_Uncovered_Storage_Area = models.IntegerField()
  Origin_Ownership = models.CharField(max_length=20, choices=Origin_Ownership_Choices)
  
  Shortage_In_Raw_Material = models.BooleanField(default=False)#related to the 3 table RawMaterial
  Benefit_From_Public_Agencies_Support = models.BooleanField(default=False)#related with the last table
  
  def __str__(self):
    return self.Name_Institution 




class Product(models.Model):
  Product_Name = models.CharField(max_length=150)
  Production_Capacity_Monthly = models.CharField(max_length=30)
  Actual_Production_Volume = models.CharField(max_length=50)
  Actual_Production_Unit = models.CharField(max_length=50)
  Target_Market = models.CharField(max_length=150)
  Target_Audience = models.CharField(max_length=50)
  Company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
  
  def __str__(self):
    return self.Product_Name 
  
  
class RawMaterial(models.Model):
  Raw_Material = models.CharField(max_length=150)
  Monthly_Consumption = models.CharField(max_length=30)#is it charfield or int or what ???
  Source = models.CharField(max_length=20, choices=Source_Choices)
  Source_Country = models.CharField(max_length=100, default='Algeria') 
  Is_Scarce = models.BooleanField(default=False)
  Company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='raw_materials')
  
  Quantities_Required_To_Reach_Maximum_Production_Capacity_Monthly = models.CharField(max_length=100)#is it charfield or int or what ???
  
  def __str__(self):
    return self.Raw_Material


class PublicAgenciesAndServices(models.Model):
  List_Agencies_And_Services = models.CharField(max_length=150, blank=True)
  Company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='public_agencies_services')
  
  def __str__(self):
    return self.List_Agencies_And_Services


class Causes_Of_Obstacles(models.Model):
  Obstacle = models.CharField(max_length=100)
  
  def __str__(self):
    return self.Obstacle

class Production_Obstacles(models.Model):
  Reasons_For_Not_Achieving_Max_Capacity = models.ManyToManyField(Causes_Of_Obstacles, blank=True)
  More_Obstacles = models.TextField(blank=True)
  Company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='production_obstacles')
  
  def __str__(self):
    return self.Company.Name_Institution