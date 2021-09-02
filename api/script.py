#escalar a quantidade de container desejado
#executar esse script


import requests
import random
import uuid


url = 'https://integrator.lwmail.com.br/migration'
payload_quantity = 100
payload_test = {
        "person_type": "PF",
        "alias_email_address": "",
        "password": "Passwordtotest@2021",
        "name": "globo teste",
        "company_name": "globo",
        "cpf": "03374110509",
        "cnpj": "00002375149902",
        "rg": "",
        "phones": [
            {
                "number": "71992035822"
            }
        ],
        "emails": [
            {
                "address": "teste@globo.com",
                "main": True,
                "confirmed": True
            }
        ],
        "address": {
            "city": "Blumenau",
            "state": "SC",
            "postal_code": "89025969",
            "country": "BR",
            "number": "23",
            "street": "rua dois"
        }
    }

emails = ["migrar_SQHRRLwMzq@globomail.correio.biz",
"migrar_uPdiXmUIsW@globomail.correio.biz",
"migrar_twAJfcofSJ@globomail.correio.biz",
"migrar_yShOrUxGsf@globomail.correio.biz",
"migrar_tNJLLTPGey@globomail.correio.biz",
"migrar_pNEKhkMuMX@globomail.correio.biz",
"migrar_FzcYnJFsRC@globomail.correio.biz",
"migrar_JHJitythBn@globomail.correio.biz",
"migrar_pgHUCnkuje@globomail.correio.biz",
"migrar_zkHDEkcQjE@globomail.correio.biz",
"migrar_qyXMRLNXdf@globomail.correio.biz",
"migrar_TJRbDNcjNn@globomail.correio.biz",
"migrar_bbhSPflpdq@globomail.correio.biz",
"migrar_hOqRiPHqOY@globomail.correio.biz",
"migrar_ZjrzeIcKvC@globomail.correio.biz",
"migrar_BplvkcjfzO@globomail.correio.biz",
"migrar_prQBiYyqHk@globomail.correio.biz",
"migrar_ODXwCgfVnm@globomail.correio.biz",
"migrar_CsnZbvMhxf@globomail.correio.biz",
"migrar_DPvsSXGhiU@globomail.correio.biz",
"migrar_ROSwDUIEmm@globomail.correio.biz",
"migrar_qNGXkZJcul@globomail.correio.biz",
"migrar_zLNdyZUIlh@globomail.correio.biz",
"migrar_zjtqkXdcEk@globomail.correio.biz",
"migrar_IurvvLtZbN@globomail.correio.biz",
"migrar_gQcHkjMeBt@globomail.correio.biz",
"migrar_yBHeLqtSSw@globomail.correio.biz",
"migrar_dgpNmitAFf@globomail.correio.biz",
"migrar_hhyfpTweGQ@globomail.correio.biz",
"migrar_uQKDPwetls@globomail.correio.biz",
"migrar_UAQaVtOdoF@globomail.correio.biz",
"migrar_KCDAYPiajc@globomail.correio.biz",
"migrar_VAnKLnHJXN@globomail.correio.biz",
"migrar_AOFlGTrQac@globomail.correio.biz",
"migrar_jcIbIoTBQC@globomail.correio.biz",
"migrar_uAaorskYNV@globomail.correio.biz",
"migrar_zLRCvVWlXh@globomail.correio.biz",
"migrar_prnbEeUvgF@globomail.correio.biz",
"migrar_AJsFmwcJmE@globomail.correio.biz",
"migrar_jVSZUPIaLB@globomail.correio.biz",
"migrar_iILHPihndF@globomail.correio.biz",
"migrar_mljmYpTyQB@globomail.correio.biz",
"migrar_AgJXVrRZQz@globomail.correio.biz",
"migrar_OZtgIFioah@globomail.correio.biz",
"migrar_qOmppscRuP@globomail.correio.biz",
"migrar_WcngiGhmpd@globomail.correio.biz",
"migrar_gpMgAzcljD@globomail.correio.biz",
"migrar_dzthMIjuwf@globomail.correio.biz",
"migrar_acZGsNehAZ@globomail.correio.biz",
"migrar_SCcCGdkJFf@globomail.correio.biz",
"migrar_DcpkZBHefv@globomail.correio.biz",
"migrar_gXOMhCWvXS@globomail.correio.biz",
"migrar_ZXoVOWNCBc@globomail.correio.biz",
"migrar_VskdNJylrU@globomail.correio.biz",
"migrar_oOMtyQdIau@globomail.correio.biz",
"migrar_nOJdsXhLrZ@globomail.correio.biz",
"migrar_eFuFlMYcqy@globomail.correio.biz",
"migrar_DtpTMuVsLF@globomail.correio.biz",
"migrar_rrGbhOKBiM@globomail.correio.biz",
"migrar_XkpptoALHX@globomail.correio.biz",
"migrar_bMivkZsMWF@globomail.correio.biz",
"migrar_oANEDxJGQh@globomail.correio.biz",
"migrar_uUlJCvbvsD@globomail.correio.biz",
"migrar_koppDbJutt@globomail.correio.biz",
"migrar_wDAwHNABAL@globomail.correio.biz",
"migrar_zWuYuOqdcl@globomail.correio.biz",
"migrar_PhLZfSsogg@globomail.correio.biz",
"migrar_xthqrBoSSN@globomail.correio.biz",
"migrar_hWxjBLpnql@globomail.correio.biz",
"migrar_XLyUoXGMeC@globomail.correio.biz",
"migrar_KGAmNLIMYq@globomail.correio.biz",
"migrar_pBLsfflhsU@globomail.correio.biz",
"migrar_iWLzRmBXpU@globomail.correio.biz",
"migrar_HvEXkpcPTx@globomail.correio.biz",
"migrar_bXGHApKMeU@globomail.correio.biz",
"migrar_EojRCGQjUK@globomail.correio.biz",
"migrar_XVCdVCzkga@globomail.correio.biz",
"migrar_BRcBArmtqB@globomail.correio.biz",
"migrar_eqgmBIwfSx@globomail.correio.biz",
"migrar_mhiqlOhEWk@globomail.correio.biz",
"migrar_UgApCPwSpF@globomail.correio.biz",
"migrar_rFXydyOQJs@globomail.correio.biz",
"migrar_sVVZvgDoSH@globomail.correio.biz",
"migrar_UHCKuwNfhf@globomail.correio.biz",
"migrar_RRjZnWUobo@globomail.correio.biz",
"migrar_TxpFqohHid@globomail.correio.biz",
"migrar_IJWazuXsLi@globomail.correio.biz",
"migrar_lgajbrlivf@globomail.correio.biz",
"migrar_bMwAYHeolF@globomail.correio.biz",
"migrar_iXLqckLZlX@globomail.correio.biz",
"migrar_fLqmbChtsW@globomail.correio.biz",
"migrar_IRiKSvvaLB@globomail.correio.biz",
"migrar_qsTCBMAAAf@globomail.correio.biz",
"migrar_jJXGvelETS@globomail.correio.biz",
"migrar_RKoACdgvlZ@globomail.correio.biz",
"migrar_IMAlAmSQdI@globomail.correio.biz",
"migrar_PMkblwPkLc@globomail.correio.biz",
"migrar_OOxgqrdbds@globomail.correio.biz",
"migrar_ZtGZAmvIDY@globomail.correio.biz",
"migrar_wUPfNspcSE@globomail.correio.biz"]

payload_list = []
for i in range(0, payload_quantity):
    payload = {}
    id_globo = f'{str(uuid.uuid4())}/{random.randint(0,99999)}'
    payload.update({'id_globo': id_globo})
    payload.update({'current_email_address': emails[i]})
    payload_list.append(payload)

migration_list = []
for item in payload_list:
    payload = {}
    payload.update(payload_test)
    payload.update({'id_globo': item['id_globo']})
    payload.update({'current_email_address': item['current_email_address']})
    migration_list.append(payload)


response = requests.post(url, json=migration_list)
response.raise_for_status()


    




