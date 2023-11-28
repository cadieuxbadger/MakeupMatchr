from django import forms
from makeupApp.models import Product

class imgForm(forms.Form):
	name = forms.CharField()
	img_field = forms.ImageField()
  
brandChoices = Product.getBrands()

# creating a form
class InputForm(forms.Form):

	# Form Creation for the lower price limit
	priceL = forms.IntegerField(widget = forms.NumberInput
                    (attrs = {'class':'form-control',
			                'placeholder':'Ex. 14',
			                'aria-label':'Minimum price point'}),
			     label = "Min Price",
			     required = False)
	
	# Form Creation for the upper price limit
	priceM = forms.IntegerField(widget = forms.NumberInput
                    (attrs = {'class':'form-control',
			                'placeholder':'Ex. 50',
			                'aria-label':'Maximum price point'}),
			     label = "Max Price",
			     required = False)
	
	# brandName = forms.CharField(max_length = 200,
	# 		     widget = forms.TextInput
    #                 (attrs = {'class':'form-control',
	# 		                'placeholder':'Brand',
	# 		                'aria-label':'Enter Brand Name'}),
	# 		    label = "Brand",
	# 		    required = False)

	# Form Creation for the brandname drop down
	# TODO: MAKE THIS COMPONENT PRETTY
	brandName = forms.TypedChoiceField(
					coerce = str,
					choices = zip(range(len(brandChoices)), brandChoices),
				    label = "Brand",
				    required=False
				   )