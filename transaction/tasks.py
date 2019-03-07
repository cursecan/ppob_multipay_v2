from background_task import background
import requests, json

from django.conf import settings

from transaction.models import (
    InstanSale, PpobSale, Status,
    ResponseInSale, ResponsePpobSale
)

_user = settings.RB_USER
_pin = settings.RB_PIN
_link = settings.RB_LINK

@background(schedule=1)
def instansale_tasks(sale_id):
    insale_obj = InstanSale.objects.get(id=sale_id)

    # DEFAULT OF PULSA DATA
    payload = {
        "method"      : "rajabiller.pulsa",
        "uid"         : _user,
        "pin"         : _pin,
        "no_hp"       : insale_obj.customer,
        "kode_produk" : insale_obj.product_code,
        "ref1"        : insale_obj.code
    }

    # GAME GROUP
    if not insale_obj.product.group.code in ['PULSA', 'DATA']:
        payload['method'] = "rajabiller.game"


    try :
        r = requests.post(
            _link, data=json.dumps(payload),
            timeout = 20
        )

        if r.status_code == requests.codes.ok:
            rson = r.json()

            Status.objects.create(instansale=insale_obj, status='IN')

        r.raise_for_status()
    except :
        pass
        
    ResponseInSale.objects.filter(sale=insale_obj).update(
        kode_produk = rson.get('KODE_PRODUK', ''),
        waktu = rson.get('WAKTU', ''),
        no_hp = rson.get('NO_HP', ''),
        sn = rson.get('SN', ''),
        nominal = int(rson.get('NOMINAL', 0)),
        ref1 = rson.get('REF1', ''),
        ref2 = rson.get('REF2', ''),
        status = rson.get('STATUS', ''),
        ket = rson.get('KET', ''),
        saldo_terpotong = int(rson.get('SALDO_TERPOTONG', 0))
    )


@background(schedule=1)
def ppobsale_tasks(sale_id):
    ppob_sale = PpobSale.objects.get(pk=sale_id)

    payload = {
        "method"      : "rajabiller.inq",
        "uid"         : _user,
        "pin"         : _pin,
        "idpel1"      : "",
        "idpel2"      : "",
        "idpel3"      : "",
        "kode_produk" : "",
        "ref1"        : ppob_sale.code
    }

    customer = ppob_sale.customer

    # TOKEN LISTRIK GROUP
    if ppob_sale.product.group.code == 'TOPLN':
        payload['kode_produk'] = 'PLNPRAB'

        if len(customer) == 11:
            payload['idpel1'] = customer
        else :
            payload['idpel2'] = customer

    # PLN PASCABAYAR GROUP
    elif ppob_sale.product.group.code == 'PLN':
        payload['kode_produk'] = ppob_sale.product.code
        payload['idpel1'] = customer
            
    # TELEPON GROUP
    elif ppob_sale.product.group.code in ['TLP', 'SPEEDY']:
        payload['kode_produk'] = ppob_sale.product.code
        payload['idpel1'] = customer[:3]
        payload['idpel2'] = customer[3:]

    # PDAM GROUP
    elif ppob_sale.product.group.code == 'PDAM':
        payload['kode_produk'] = ppob_sale.product.code
        if ppob_sale.product.code in ['WABGK', 'WAMJK', 'WATAPIN']:
            payload['idpel2'] = customer
        else :
            payload['idpel1'] = customer


    # PAYMENT REQUEST
    if ppob_sale.sale_type == 'PY':
        payload['method'] = "rajabiller.paydetail"
        payload['ref2'] = ppob_sale.inquery.responseppobsale.ref2
        payload['nominal'] = ppob_sale.nominal
        payload['ref3'] = ''

        Status.objects.create(
            ppobsale = ppob_sale,
            status = 'IN'
        )
        


    try :
        r = requests.post(
            _link, data=json.dumps(payload),
            timeout = 20
        )

        if r.status_code == requests.codes.ok:
            rson = r.json()

        r.raise_for_status()
    except :
        pass

    ResponsePpobSale.objects.filter(sale=ppob_sale).update(
        kode_produk = rson.get('KODE_PRODUK', ''),
        waktu = rson.get('WAKTU', ''),
        idpel1 = rson.get('IDPEL1', ''),
        idpel2 = rson.get('IDPEL2', ''),
        idpel3 = rson.get('IDPEL3', ''),
        nama_pelanggan = rson.get('NAMA_PELANGGAN', ''),
        periode = rson.get('PERIODE', ''),
        nominal = int(rson.get('NOMINAL', 0)),
        admin = int(rson.get('ADMIN', 0)),
        ref1 = rson.get('REF1', ''),
        ref2 = rson.get('REF2', ''),
        ref3 = rson.get('REF3', ''),
        status = rson.get('STATUS', ''),
        ket = rson.get('KET', ''),
        saldo_terpotong = int(rson.get('SALDO_TERPOTONG', 0)),
        url_struk = rson.get('URL_STRUK', '')
    )
