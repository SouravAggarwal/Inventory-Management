from django.db import models
class Purchased(models.Model):
	stock=models.ForeignKey('stocks.Stock',on_delete=models.PROTECT)
	Purchase_ID=models.CharField(max_length=100,null=True)
	Purchase_Date=models.CharField(max_length=100,null=True)
	Remarks=models.CharField(max_length=200,null=True)
	ItemCode=models.CharField(max_length=100,null=True)
	Base_Price=models.DecimalField(max_digits=8,decimal_places=3,null=True)
	ProductName=models.CharField(max_length=100,null=True)
	Capacity=models.CharField(max_length=100,null=True)
	Old_Quantity=models.IntegerField(null=True)
	Quantity=models.IntegerField(null=True)
	Total_Quantity=models.IntegerField(null=True)
	def __str__(self):
		return self.Purchase_ID+"^^"+self.Purchase_Date+"^^"+self.Remarks+"^^"+self.ItemCode+"^^"+str(self.Base_Price)+"^^"+self.ProductName+"^^"+str(self.Capacity)+"^^"+str(self.Old_Quantity)+"^^"+str(self.Quantity)+"^^"+str(self.Total_Quantity)
	
	