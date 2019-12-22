import json
from .constants import PRODUCT_CODE_TYPE_LIST
from .helper_functions import user_directory_path, ProductAPI
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100, unique=True)
    node_id = models.IntegerField()
    product_code = models.CharField(max_length=100, unique=True)
    product_code_type = models.CharField(max_length=100, choices=PRODUCT_CODE_TYPE_LIST)
    multipack_quantity = models.IntegerField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    main_image_url = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_price = self.price

    def to_json(self):
        return {
            'product_title': self.title,
            'jet_browse_node_id': self.node_id,
            'standard_product_codes': [{
                'standard_product_code': self.product_code,
                'standard_product_code_type': self.product_code_type
            }],
            'multipack_quantity': self.multipack_quantity,
            'brand': self.brand.name,
            'main_image_url': 'https://www.yeti.com/dw/image/v2/BBRN_PRD/on/demandware.static/-/Sites-masterCatalog_Yeti/default/dw8ec99c12/images/pdp-Rambler/Rambler%20Tumbler%2020oz/Brick%20Red/170781-NewSite-Brick-Red-Website-Assets-R20-BrickRed-OH-1680x1024.jpg?sw=750&sfrm=jpg'
        }

    def clean(self):
        if not self.sku or (not self.id and Product.objects.filter(product_code=self.sku).exists()):
            raise ValidationError('')

        if not self.title:
            raise ValidationError('')

        if not self.product_code or (not self.id and Product.objects.filter(product_code=self.product_code).exists()):
            raise ValidationError('')

        # Send API calls to add product, pricing
        product_api = ProductAPI(self)

        if not self.id:
            created, errors = product_api.add_product()
            if not created:
                raise ValidationError(_(f'{errors}'))

        if self.price and self.old_price != self.price:
            accepted, errors = product_api.add_price()
            if not accepted:
                raise ValidationError(_(f'{errors}'))

    def __str__(self):
        return self.title