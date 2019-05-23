import uuid as uid
from datetime import timedelta

from musichub import redis


class EmailVerificationUUIDStorage:
    key_prefix = 'user-uuid-'

    @classmethod
    def save(cls, email: str) -> tuple:
        uuid = uid.uuid4()
        uuid_key = cls.build_key(uuid)
        expire_time = timedelta(minutes=1).seconds
        redis.set(uuid_key, email, ex=expire_time)
        return uuid, email

    @classmethod
    def delete(cls, uuid):
        uuid_key = cls.build_key(uuid)
        redis.delete(uuid_key)

    @classmethod
    def get_email_by_uuid(cls, uuid: str) -> str:
        uuid_key = cls.build_key(uuid)
        email = redis.get(uuid_key)
        if not email:
            raise KeyError(f'Email with uuid {uuid} not found')
        return str(email, encoding='utf-8')

    @classmethod
    def build_key(cls, uuid):
        return f'{cls.key_prefix}{uuid}'
