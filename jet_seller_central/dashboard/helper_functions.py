import os
import requests
from .decorators import refresh_token
from .constants import HOST

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{instance.product.title}/{filename}'

@refresh_token
def product_api(product, method='add'):
    token = os.environ.get('JET_TOKEN')
    product_json = product.to_json()
    response = requests.put(
            f'{HOST}api/merchant-skus/{product.sku}',
            json=product_json,
            headers={'Authorization': f'bearer {token}'}
    )
    return response

class ProductAPI():

    def __init__(self, product):
        self.product = product

    def error_handleding(self, response):
        try:
            response.raise_for_status()
            return (True, '')
        except Exception as err:
            errors = response.json().get('errors')
            if not errors:
                errors = response.json().get('Message')
            else:
                errors = ', '.join(errors)
            return (False, errors)

    @refresh_token
    def add_product(self):
        token = os.environ.get('JET_TOKEN')
        response = requests.put(
            f'{HOST}api/merchant-skus/{self.product.sku}',
            json=self.product.to_json(),
            headers={'Authorization': f'bearer {token}'}
        )
        return self.error_handleding(response)

    @refresh_token
    def add_price(self):
        token = os.environ.get('JET_TOKEN')
        response = requests.put(
            f'{HOST}api/merchant-skus/{self.product.sku}/price',
            json={'price': self.product.price},
            headers={'Authorization': f'bearer {token}'}
        )
        return self.error_handleding(response)

    @refresh_token
    def archive(self):
        token = os.environ.get('JET_TOKEN')
        response = requests.put(
            f'{HOST}api/merchant-skus/{self.product.sku}/status/archive',
            json={'is_archived': True},
            headers={'Authorization': f'bearer {token}'}
        )
        return self.error_handleding(response)

    @refresh_token
    def unarchive(self):
        token = os.environ.get('JET_TOKEN')
        response = requests.put(
            f'{HOST}api/merchant-skus/{self.product.sku}/status/archive',
            json={'is_archived': False},
            headers={'Authorization': f'bearer {token}'}
        )

        return self.error_handleding(response)
