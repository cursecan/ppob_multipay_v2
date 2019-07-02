from background_task import background
from .models import Product
from django.conf import settings

import requests, json

_user = settings.RB_USER
_pin = settings.RB_PIN
_link = settings.RB_LINK

@background(schedule=1)
def scheduling_prod_status(prod_id):
    prod_obj = Product.objects.get(pk=prod_id)
    data = {
        'method': 'rajabiller.info_produk',
        'uid': _user,
        'pin': _pin,
        'kode_produk': prod_obj.code
    }

    try : 
        r = requests.post(_link, data=json.dumps(data), timeout=10)
        if r.status_code == requests.codes.ok:
            rson = r.json()

            produk_code = rson.get('KODE_PRODUK', '00')
            status = rson.get('STATUS_PRODUK', '')
            harga = int(rson.get('HARGA', 0))

            sta = False
            if status == 'AKTIF':
                sta = True

            Product.objects.filter(code=produk_code).update(
                is_active = sta
            )
        
    except:
        pass



@background(schedule=1)
def product_operator_status(op_id):
    prod_objs = Product.objects.filter(
        type_product='IN', operator__id=op_id
    )

    for i in prod_objs:
        payload = {
            'method': 'rajabiller.info_produk',
            'uid': _user,
            'pin': _pin,
            'kode_produk': i.code
        }

        try : 
            r = requests.post(_link, data=json.dumps(payload), timeout=10)
            if r.status_code == requests.codes.ok:
                rson = r.json()

                produk_code = rson.get('KODE_PRODUK', '00')
                status = rson.get('STATUS_PRODUK', '')
                harga = int(rson.get('HARGA', 0))

                sta = False
                if status == 'AKTIF':
                    sta = True

                Product.objects.filter(code=produk_code).update(
                    is_active = sta
                )
            
        except:
            pass