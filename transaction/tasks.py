from background_task import background
import requests, json
import datetime

from django.conf import settings
from django.utils import timezone

from transaction.models import (
    InstanSale, PpobSale, Status,
    ResponseInSale, ResponsePpobSale
)


_user = settings.RB_USER
_pin = settings.RB_PIN
_link = settings.RB_LINK


@background(schedule=60)
def instansale_repeat_response(res_id):
    response_insale_objs = ResponseInSale.objects.filter(
        id = res_id, sale__closed=False
    )
    if response_insale_objs.exists():
        response_insale = response_insale_objs.get()
        if response_insale.ref2 is not None and response_insale.ref2 != '':
            h_time = timezone.localtime(response_insale.sale.timestamp) + datetime.timedelta(minutes=10)
            l_time = h_time + datetime.timedelta(days=-1)

            payload  = {
                "method"      : "rajabiller.datatransaksi",
                "uid"         : _user,
                "pin"         : _pin,
                "tgl1"        : l_time.strftime('%Y%m%d%H%M%S'),
                "tgl2"        : h_time.strftime('%Y%m%d%H%M%S'),
                "id_transaksi": response_insale.ref2,
                "id_produk"   : "",
                "idpel"       : "",
                "limit"       : ""
            }

            try :
                r = requests.post(_link, json.dumps(payload), timeout=40)
                if r.status_code == requests.codes.ok:
                    rson = r.json()

                    # {
                    #     'UID': 'SP118171', 
                    #     'KET': 'Transaksi berhasil', 
                    #     'LIMIT': '', 'IDPEL': '', 'TGL2': '20190318010101', 'PIN': '------', 
                    #     'TGL1': '20190317010101', 'STATUS': '00', 'KODE_PRODUK': '', 
                    #     'RESULT_TRANSAKSI': ['1307083649#20190317202539#S5H#TELKOMSEL SIMPATI / AS 5RB#081315667766#00#Pembelian voucher pulsa S5HX berhasil ke no 081315667766. Kode Voucher: 0041003499597509.#5575#0041003499597509#SUKSES']
                    # }

                    try :
                        data = rson['RESULT_TRANSAKSI'][0]
                        trx_ref, waktu, code, product, nopel, statcode, info, price, sn, status = data.split('#')

                        try :
                            price = int(price)
                        except:
                            price = 0

                        if statcode == '00' and sn != '':
                            response_insale_objs.update(
                                waktu = waktu,
                                no_hp = nopel,
                                sn = sn,
                                status = statcode,
                                ket = status,
                                saldo_terpotong = price
                            )
                            Status.objects.create(instansale=response_insale.sale, status='CO')
                    except:
                        pass

            except:
                pass



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
            timeout = 40
        )

        if r.status_code == requests.codes.ok:
            rson = r.json()

            Status.objects.create(instansale=insale_obj, status='IN')

            try :
                nominal = int(rson.get('NOMINAL', 0))
            except : 
                nominal = 0

            res_obj, create = ResponseInSale.objects.update_or_create(
                sale = insale_obj,
                defaults = {
                    'kode_produk' : rson.get('KODE_PRODUK', ''),
                    'waktu' : rson.get('WAKTU', ''),
                    'no_hp' : rson.get('NO_HP', ''),
                    'sn' : rson.get('SN', ''),
                    'nominal' : nominal,
                    'ref1' : rson.get('REF1', ''),
                    'ref2' : rson.get('REF2', ''),
                    'status' : rson.get('STATUS', ''),
                    'ket' : rson.get('KET', ''),
                    'saldo_terpotong' : int(rson.get('SALDO_TERPOTONG', 0))
                }
            )

            # Repeate check transakasi
            instansale_repeat_response(res_obj.id, creator=res_obj, repeat=120, repeat_until=timezone.now() + datetime.timedelta(minutes=10))

        r.raise_for_status()
    except :
        pass
        
    

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
        payload['kode_produk'] = 'PLNPRAH'

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

    try :
        r = requests.post(
            _link, data=json.dumps(payload),
            timeout = 40
        )

        if r.status_code == requests.codes.ok:
            rson = r.json()
            Status.objects.create(
                ppobsale = ppob_sale,
                status = 'IN'
            )

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
