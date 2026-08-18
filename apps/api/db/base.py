"""Tüm ORM modellerinin (tablo tanımlarının) miras alacağı temel sınıf.

Faz 2'de Document, Chunk gibi sınıflar bu Base'den türeyecek.
Alembic, hangi tabloların olması gerektiğini bu sınıf üzerinden okuyacak.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
