#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
import hashlib
from faker import Faker

f = Faker()

class GeneratorEvents:
    def __init__(self, root):
        self.fields = 'all'
        self.root = root
        self.allowed_channels = self.__generate().keys()

    def __generate(self):
        return {
            'global'               : self.create_global(),
            'session'              : self.create_session(),
            'payment'              : self.create_payment(),
            'acquiring'            : self.create_acquiring(),
            'card2card'            : self.create_card2card(),
            'p2p_money_transfer'   : self.create_p2p(),
            'invoice'              : self.create_invoice(),
            'login'                : self.create_login(),
            'access_control_change': self.create_access(),
            'email'                : self.create_email()
        }

    def __get_random_cart(self):
        length = random.randint(1, 20)
        cart = []
        for i in range(0, length):
            cart.append({
                "name"  : str(f.pystr(min_chars=1, max_chars=20)),
                "qty"   : random.randint(1, 5),
                "price" : random.randint(10, 1000)
            })
        return cart

    # <----------------------------------------------------------------
    def pull_create_event(self, channel, sub_channel, fields):
        if fields == 'requiered':
            self.fields = fields
            r = self.__generate()[channel]
        else:
            self.fields = 'all'
            r = self.__generate()[channel]
            if isinstance(fields, list):
                r = {key: val for key, val in r.items() if key in fields}
        if self.root.af_version == 'v2.1':
            r['channel']     = channel
            r['sub_channel'] = sub_channel
        return r

    def pull_update_event(self, extid = None, tx_id = None):
        r = {
            "comment":"generator comment",
            "code":"generator code"
        }
        if self.root.af_version == 'v2.2':
            r["status"] = random.choice(['OK', 'FAILED', 'FRAUD', 'CHARGEBACK', 'REFUND', 'SETTLED'])
            r["t"] = int(f.date_time_between(start_date='now', end_date='now').timestamp() / 10)
        else:
            assert extid or tx_id, 'extid or tx_id must be present for v2.1'
            r["status"] = random.choice(['OK', 'FAILED', 'FRAUD'])
            r["is_authed"] = random.choice([0, 1])
            r['extid'] = extid if extid else ""
            r['tx_id'] = tx_id if tx_id else ""
        return r

    def create_global(self):
        requiered_fields = {}  # there is not special reqiered fields excepts 'channel'/'subchannel'
        if self.fields == 'all':
            additional_fields = {
                "t": int(f.date_time_between(start_date='-1y', end_date='now').timestamp() / 10),
                "timezone": random.randint(-720, 840),  # from -12 to +14 GMT
                "extid": str(f.pystr(min_chars=1, max_chars=20)),
                "tid": str(f.pystr(min_chars=1, max_chars=20)),
                "ip": str(random.choice([f.ipv4(network=False, address_class=None, private=None),
                                         f.ipv6(network=False)])),
                "ext_fraud_score": random.randint(0, 1000),
                "query": ["fraud_score"]
            }
            requiered_fields = {**requiered_fields, **additional_fields}
        return requiered_fields

    def create_session(self):
        return {
            **self.create_global(),
            "tid": str(f.pystr(min_chars=1, max_chars=20))
        }

    def create_payment(self):
        requiered_fields = {
            **self.create_global(),
            "src_id"     : str(f.iban()),
            "src_parent" : "test_%s" % str(f.pystr(min_chars=1, max_chars=20)),
            "dst_id"     : str(f.iban()),
            "dst_parent" : "test_%s" % str(f.pystr(min_chars=1, max_chars=20)),
            "amount"     : int(random.randint(1000, 21000)),
            "exp"        : 2,  # EUR and USD
            "currency"   : str(random.choice(["840", "978"]))
        }
        if self.fields == 'all':
            additional_fields = {
                "src_partner"   : "test_%s" % str(f.pystr(min_chars=1, max_chars=20)),
                "src_client_id" : str(f.iban()),
                "dst_partner"   : "test_%s" % str(f.pystr(min_chars=1, max_chars=20)),
                "dst_client_id" : str(f.iban())
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields

    def create_acquiring(self):
        requiered_fields = {
            **self.create_payment(),
            "exp_date": str(f.credit_card_expire(start="now", end="+10y", date_format="%m.%y"))
        }
        src_id = hashlib.sha256(f.credit_card_number(card_type=None).encode('utf-8')).hexdigest()
        requiered_fields["src_id"]     = str(src_id)
        requiered_fields["src_parent"] = str(f.credit_card_full(card_type=None)).split(' ')[0]
        requiered_fields["dst_parent"] = "test_%s" % str(f.credit_card_full(card_type=None)).split(' ')[0]

        if self.fields == 'all':
            additional_fields = {
                "mcc"              : random.choice(["5309", "5310", "5311"]),
                "shipping_address" : f.address(),
                "zipcode"          : f.postcode(),
                "is_3ds_enabled"   : random.choice([0, 1]),
                "is_recurrent"     : random.choice([0, 1]),
                "cart"             : self.__get_random_cart(),
                "email"            : f.email(),
                "phonenumber"      : f.phone_number()
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields

    def create_card2card(self):
        requiered_fields = self.create_payment()  # there is not special reqiered fields excepts fields from payment

        src_id = hashlib.sha256(f.credit_card_number(card_type=None).encode('utf-8')).hexdigest()
        dst_id = hashlib.sha256(f.credit_card_number(card_type=None).encode('utf-8')).hexdigest()

        requiered_fields["src_id"] = str(src_id)
        requiered_fields["dst_id"] = str(dst_id)
        requiered_fields["src_parent"] = "test_" + str(f.credit_card_full(card_type=None)).split(' ')[0]
        requiered_fields["dst_parent"] = "test_" + str(f.credit_card_full(card_type=None)).split(' ')[0]

        if self.fields == 'all':
            src_profile = f.simple_profile()
            dst_profile = f.simple_profile()

            additional_fields = {
                "is_3ds_enabled"      : random.choice([0, 1]),
                "src_exp_date"        : str(f.credit_card_expire(start="now",
                                            end="+10y", date_format="%m.%y")),
                "src_billing_address" : src_profile['address'],
                "src_zipcode"         : f.postcode(),
                "src_email"           : src_profile['mail'],
                "src_phonenumber"     : f.phone_number(),
                "src_fullname"        : src_profile['name'],
                "src_birthdate"       : src_profile['birthdate'].strftime("%a%B%Y"),
                "dst_exp_date"        : str(f.credit_card_expire(start="now",
                                            end="+10y", date_format="%m.%y")),
                "dst_billing_address" : dst_profile['address'],
                "dst_zipcode"         : f.postcode(),
                "dst_email"           : dst_profile['mail'],
                "dst_phonenumber"     : f.phone_number(),
                "dst_fullname"        : dst_profile['name'],
                "dst_birthdate"       : dst_profile['birthdate'].strftime("%a%B%Y")
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields

    def create_p2p(self):
        requiered_fields = {
            **self.create_payment(),
            "operation_type": random.choice(["input", "output"])
        }
        src_id = hashlib.sha256(f.credit_card_number(card_type=None).encode('utf-8')).hexdigest()
        dst_id = hashlib.sha256(f.credit_card_number(card_type=None).encode('utf-8')).hexdigest()

        requiered_fields["src_id"]      = str(src_id)
        requiered_fields["dst_id"]      = str(dst_id)
        requiered_fields["src_parent"]  = f.iban()
        requiered_fields["dst_parent"]  = f.iban()
        requiered_fields["src_partner"] = "test_%s" % str(f.pystr(min_chars=1, max_chars=20))
        requiered_fields["dst_partner"] = "test_%s" % str(f.pystr(min_chars=1, max_chars=20))

        if self.fields == 'all':
            additional_fields = {
                "system_name"          : random.choice(["transferto", "transferwise", "contact"]),
                "sender_phonenumber"   : f.phone_number(),
                "src_pos_city"         : f.location_on_land(coords_only=False)[2],
                "src_pos_id"           : f.location_on_land(coords_only=False)[3],
                "src_pos_country"      : f.location_on_land(coords_only=False)[4].split('/')[1],
                "receiver_phonenumber" : f.phone_number(),
                "dst_pos_city"         : f.location_on_land(coords_only=False)[2],
                "dst_pos_id"           : f.location_on_land(coords_only=False)[3],
                "dst_pos_country"      : f.location_on_land(coords_only=False)[4].split('/')[1]
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields

    def create_invoice(self):
        requiered_fields = self.create_payment()

        customer_bank_id = hashlib.sha256(f.iban().encode('utf-8')).hexdigest()
        requiered_fields["src_id"] = customer_bank_id
        requiered_fields["src_parent"] = "test_%s" % str(f.pystr(min_chars=1, max_chars=20))

        if self.fields == 'all':
            additional_fields = {
                "shipping_address": f.address(),
                "zipcode"         : f.postcode(),
                "cart"            : self.__get_random_cart()
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields

    def create_login(self):
        requiered_fields = {
            **self.create_global(),
            "login" : f.user_name()
        }

        if self.fields == 'all':
            additional_fields = {
                "email"        : f.email(),
                "phonenumber"  : f.phone_number(),
                "imsi_number"  : f.msisdn(),
                "oauth_system" : random.choice(['google', 'facebook', 'twitter']),
                "2FAused"      : random.choice([0, 1])
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields

    def create_access(self):
        requiered_fields = {
            **self.create_global(),
            "dst_id"      : f.user_name(),
            "dst_parent"  : str(f.pystr(min_chars=1, max_chars=20)),
        }

        if self.fields == 'all':
            additional_fields = {
                "email"       : f.email(),
                "phonenumber" : f.phone_number(),
                "imsi_number" : f.msisdn(),
                "2FA_used"    : random.choice([0, 1])
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields

    def create_email(self):
        requiered_fields = {
            **self.create_global(),
            "src_id"   : str(f.pystr(min_chars=1, max_chars=20)),
            "dst_id"   : str(f.pystr(min_chars=1, max_chars=20)),
            "subject"  : str(f.pystr(min_chars=1, max_chars=20))
        }

        if self.fields == 'all':
            additional_fields = {
                "contentType"  : f.phone_number(),
                "body"         : f.msisdn(),
                "is_encrypted" : random.choice([0, 1]),
            }
            requiered_fields = {**requiered_fields, **additional_fields}

        return requiered_fields


if __name__ == '__main__':
    pass
