'''
SQLAlchemy is a library that facilitates the communication between Python programs 
and databases. Most of the times, this library is used as an Object Relational Mapper (ORM) tool 
that translates Python classes to tables on relational databases and automatically 
converts function calls to SQL statements.
'''

from flask_sqlalchemy import SQLAlchemy

#sql alchemy obj
db = SQLAlchemy()