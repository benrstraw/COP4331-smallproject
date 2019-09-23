from flask import Flask, request, abort, session
import sqlalchemy as db
import json

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = b'\xbd0Z\xef\xdbv\xfe|\x9e\x0b\xe4c\x08\x12&\xca'

engine = db.create_engine('mysql://smallproject:cop4331@localhost/contactmanager')
connection = engine.connect()
metadata = db.MetaData()
users = db.Table('users', metadata, autoload=True, autoload_with=engine)
contacts = db.Table('contacts', metadata, autoload=True, autoload_with=engine)

@app.route("/")
def home():
	return "Hello, me!"

@app.route("/authed")
def authed():
	userid = session.get("userid")
	if not userid:
		return { "error": "not authenticated" }, 401
	return {
		"error": "success",
		"userid": userid
	}

@app.route("/test", methods=['GET'])
def test():

	query = db.select([users])
	ResultProxy = connection.execute(query)
	result = ResultProxy.fetchall()
	allusers = [dict(r) for r in result]

	query = db.select([contacts])
	ResultProxy = connection.execute(query)
	result = ResultProxy.fetchall()
	allcontacts = [dict(r) for r in result]

	return {
		"error": "success",
		"userid": session.get('userid'),
		"users": allusers,
		"contacts": allcontacts
	}

@app.route("/logout", methods=['GET'])
def logout():
	session.pop('userid', None)
	return { "error": "success" }

@app.route("/login", methods=['POST'])
def login():
	email = request.form.get('email')
	password = request.form.get('password')

	query = db.select([users]).where(db.and_(users.columns.email == email, users.columns.password == password))
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()
	if not result:
		return { "error": "bad login" }

	session['userid'] = result['userid']

	return {
		"error": "success",
		"userid": result['userid']
	}

@app.route("/signup", methods=['POST'])
def signup():
	print(repr(request.form))

	email = request.form.get('email')
	password = request.form.get('password')

	if not email:
		return { "error": "no email" }, 400
	if not password:
		return { "error": "no password" }, 400
	if len(email) > 100:
		return { "error": "email too large (max 100)" }, 400
	if len(password) > 100:
		return { "error": "password too large (max 100)" }, 400

	query = users.insert().values(email=email, password=password)
	ResultProxy = connection.execute(query)

	session['userid'] = ResultProxy.inserted_primary_key[0]

	return {
		"error": "success",
		"userid": ResultProxy.inserted_primary_key[0]
	}

@app.route("/getall", methods=['GET'])
def getall():
	userid = session.get("userid")
	if not userid:
		return { "error": "not authenticated" }, 401

	query = db.select([contacts]).where(contacts.columns.userid == userid)
	ResultProxy = connection.execute(query)
	result = ResultProxy.fetchall()

	return {
		"error": "success",
		"results": [dict(r) for r in result]
	}

@app.route("/get", methods=['GET'])
def getone():
	userid = session.get("userid")
	if not userid:
		return { "error": "not authenticated" }, 401

	contactid = request.args.get('id')
	if not contactid:
		return { 'error': 'no contactid' }, 400

	query = db.select([contacts]).where(db.and_(contacts.columns.userid == userid, contacts.columns.contactid == contactid))
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()
	if not result:
		return { "error": "invalid contact" }

	return {
		"error": "success",
		"results": dict(result)
	}

@app.route("/add", methods=['POST'])
def add_contact():
	userid = session.get("userid")
	if not userid:
		return { "error": "not authenticated" }, 401

	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	phone = request.form.get('phone')
	email = request.form.get('email')
	address = request.form.get('address')

	if len(first_name) > 100:
		return { "error": "first_name too large (max 100)" }, 400
	if len(last_name) > 100:
		return { "error": "last_name too large (max 100)" }, 400
	if len(phone) > 15:
		return { "error": "phone too large (max 15)" }, 400
	if len(email) > 100:
		return { "error": "email too large (max 100)" }, 400
	if len(address) > 300:
		return { "error": "address too large (max 300)" }, 400

	query = contacts.insert().values(userid=userid, first_name=first_name, last_name=last_name, phone=phone, email=email, address=address).return_defaults()
	ResultProxy = connection.execute(query)

	query = db.select([contacts]).where(contacts.columns.contactid == ResultProxy.inserted_primary_key[0])
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()

	return {
		"error": "success",
		"contact": dict(result)
	}

@app.route("/edit", methods=['POST'])
def edit_contact():
	userid = session.get("userid")
	if not userid:
		return { "error": "not authenticated" }, 401

	contactid = request.form.get('contactid')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	phone = request.form.get('phone')
	email = request.form.get('email')
	address = request.form.get('address')

	if len(first_name) > 100:
		return { "error": "first_name too large (max 100)" }, 400
	if len(last_name) > 100:
		return { "error": "last_name too large (max 100)" }, 400
	if len(phone) > 15:
		return { "error": "phone too large (max 15)" }, 400
	if len(email) > 100:
		return { "error": "email too large (max 100)" }, 400
	if len(address) > 300:
		return { "error": "address too large (max 300)" }, 400

	query = contacts.update().values(userid=userid, first_name=first_name, last_name=last_name, phone=phone, email=email, address=address).where(contacts.columns.contactid == contactid)
	ResultProxy = connection.execute(query)

	query = db.select([contacts]).where(contacts.columns.contactid == contactid)
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()

	return {
		"error": "success",
		"contact": dict(result)
	}

@app.route("/delete", methods=['POST'])
def delete_contact():
	userid = session.get("userid")
	if not userid:
		return { "error": "not authenticated" }, 401

	contactid = request.form.get('contactid')
	if not contactid:
		return { "error": "no contactid" }, 400

	query = contacts.delete().where(db.and_(contacts.columns.contactid == contactid, contacts.columns.userid == userid))
	ResultProxy = connection.execute(query)

	return {
		"error": "success"
	}

@app.route("/search", methods=['GET'])
def search():
	userid = session.get("userid")
	if not userid:
		return { "error": "not authenticated" }, 401

	searchq = request.args.get('query')
	if not searchq:
		return { 'error': 'no query' }, 400

	#query = db.select([contacts]).where(contacts.columns.userid == userid)
	query = db.text("SELECT * FROM contacts WHERE userid = :userid AND MATCH (first_name,last_name,phone,email,address) AGAINST (:squery)")
	ResultProxy = connection.execute(query, userid=userid, squery=searchq)
	result = ResultProxy.fetchall()
	if not result:
		return { "error": "no results" }

	return {
		"error": "success",
		"results": [dict(r) for r in result]
	}

app.run()
