from peewee import *
import datetime

db = SqliteDatabase('./database/aplicacao.db')

class BaseModel(Model):
    class Meta:
        database = db

class Usuario(BaseModel):
    usuario = CharField(max_length=50)
    senha   = CharField(max_length=100)
    perfil  = CharField(max_length=20)
    criacao = DateTimeField(default=datetime.datetime.now)

class Produto(BaseModel):
    desc = CharField(max_length=255)
    medida = CharField(max_length=50)
    categoria = CharField(max_length=50)
    valor = DoubleField()
    quantidade = DoubleField()

class Vendas(BaseModel):
    nome_cliente = CharField(max_length=100)
    cpf_cliente = CharField(max_length=15)
    valorTotal = DecimalField(max_digits=10, decimal_places=2)
    desconto = DecimalField(max_digits=10, decimal_places=2)

# Usuario.create_table()
