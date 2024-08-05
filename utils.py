import bcrypt
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker

# Configuração da Conexão com o BD
DATABASE_URL = "postgresql://mygamehub:XnDyt3Xa8O66bmE7Jbc3ly6zZ3f4eiGH@dpg-cqlnivdumphs7397s8k0-a.oregon-postgres.render.com/loginbd_6tj3"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Tabela users
users = Table('users', metadata, 
              Column('id', Integer, primary_key=True),
              Column('username', String, unique=True),
              Column('password', String),

# Tabela profiles
profiles = Table('profiles', metadata, 
                 Column('id', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey('users.id')),
                 Column('full_name', String),
                 Column('bio', String),
                 Column('profile_picture', String))  # Armazena o caminho da imagem de perfil

# Tabela posts (simula postagens do usuário)
posts = Table('posts', metadata,
              Column('id', Integer, primary_key=True),
              Column('user_id', Integer, ForeignKey('users.id')),
              Column('image_path', String))  # Caminho para a imagem do post

metadata.create_all(engine)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))