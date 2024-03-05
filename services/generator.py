import string
import random

chars = string.digits + string.ascii_letters

numbers = string.digits

class Generator:
    @staticmethod
    def key_generator(size, chars=chars):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_key(cls, size, model_):
        new_key = cls.key_generator(size=size)
        key_exists = model_.objects.filter(token_key=new_key).exists()
        return cls.create_key(size, model_) if key_exists else new_key

    @staticmethod
    def id_generator(size, number=numbers):
        return "".join(random.choice(number) for _ in range(size))


    @classmethod
    def create_id(cls, size, model_name):
        new_id = cls.id_generator(size=size)
        id_exists = model_name.objects.filter(invoice_id=new_id).exists()
        return cls.create_id(size, model_name) if id_exists else new_id


    @staticmethod
    def order_key_generator(size, chars=chars):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def order_key(cls, size, model_):
        new_order_key = cls.order_key_generator(size=size)
        order_key_exists = model_.objects.filter(verification_key=new_order_key).exists()
        return cls.order_key(size, model_) if order_key_exists else new_order_key
