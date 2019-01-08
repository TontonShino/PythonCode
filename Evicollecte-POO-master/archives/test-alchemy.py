from sqlalchemy import MetaData

from sqlalchemy.schema import Table
bddUrl="shinobize.com"#Url/adresse bdd
bddUser="evidensee"#User BDD
bddPswd="house732"#Mot de passe BDD
bddName="dolibarr"#nom de la base de donnee
conn = {

        'type': 'mysql',

        'adap': 'oursql',

        'host': bddUrl,

        'port': '3306',

        'user': bddUser,

        'pass': bddPswd,

        'name': bddName,

}

url = '%(type)s+%(adap)s://%(user)s:%(pass)s@%(host)s:%(port)s/%(name)s' % conn



metadata = MetaData(url)

table = Table('table_name', metadata, autoload=True)from sqlalchemy.schema import Table

print(table.c)