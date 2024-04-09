from sqlalchemy import create_engine, MetaData

database_path = r'C:\Users\Minh Long\Documents\Freelancing\WebGiaDinh\myproject\db.sqlite3'
sqlite_engine =create_engine(f'sqlite:///{database_path}')

# drop all tables
meta = MetaData()
meta.reflect(bind=sqlite_engine)

# Drop all tables
meta.drop_all(bind=sqlite_engine)