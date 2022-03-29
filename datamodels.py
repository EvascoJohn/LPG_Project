import sqlite3


def writer(connection, command):
	c = sqlite3.connect(connection)
	c.cursor().execute(command)
	c.commit()
	c.close()



def retrieve(connection, command):
	c = sqlite3.connect(connection)
	result = c.cursor().execute(command).fetchone();
	c.commit()
	c.close()
	return result



def retrieve_all(connection, command):
	c = sqlite3.connect(connection)
	result = c.cursor().execute(command).fetchall();
	c.commit()
	c.close()
	return result



class DatabaseHandler(object):

	select = "select"
	create = "create"
	insert = "insert"
	update = "update"
	delete = "delete"

	def __init__(self, database, table_attributes, table_name):
		self.database_file = database
		self.table_attributes = table_attributes
		self.table_name = table_name


	def insert_data(self, data):
		values = f'values{data}'
		command = f'{self.insert} into {self.table_name}{self.table_attributes} {values}'
		writer(self.database_file, command)


	def update_data(self, column, newdata, row, rowdata):
		command = f'{self.update} {self.table_name} set {column} = {newdata} where {row} == {rowdata}'
		writer(self.database_file, command)


	def delete_data(self, column, keyname):
		command = f'{self.delete} from {self.table_name} where {column} = {keyname}'
		writer(self.database_file, command)


	def select_string_data(self, column, keyname):
		command = f'{self.select} * from {self.table_name} where {column} = "{keyname}" '
		return retrieve(self.database_file, command)


	def select_integer_data(self, column, keyname):
		command = f'{self.select} * from {self.table_name} where {column} = {keyname} '
		return retrieve(self.database_file, command)


	def select_data_all(self):
		command = f"{self.select} * from {self.table_name}"
		return retrieve_all(self.database_file, command)



class LPGDataObject(object):

	def __init__(self,*, name=None, weight=None, price=None):
		self.name = f'"{name}"'
		self.weight = weight
		self.price = price


	def set_weight_only(self, weight):
		self.weight = weight


	def set_price_only(self, price):
		self.price = price


	def get_weight(self):
		return self.weight


	def set_name_only(self, name):
		self.name = name


	def __setattr__(self, key, value):
		self.__dict__[key] = value


class CustomerDataObject(object):


	def __init__(self,*, firstname, lastname):
		self.firstname = f'"{firstname}"'
		self.lastname = f'"{lastname}"'


	def __setattr__(self, key, value):
		self.__dict__[key.title()] = value



class OrderDataObject(object):


	def __init__(self,*, datelog, lpg, customer, paidamount, fullypaid, delivered):
		self.datelog = f'"{datelog}"'
		self.lpg = f'"{lpg}"'
		self.customer = f'"{customer}"'
		self.paidamount = paidamount
		self.fullypaid = fullypaid
		self.delivered = delivered


	def __setattr__(self, key, value):
		self.__dict__[key.title()] = value



class LPG(DatabaseHandler):


	def __init__(self, database, table_name):
		self.table_name = table_name
		self.table_attributes = "(Name, Weight, Price)"
		self.lpg_connection = database
		super().__init__(database, self.table_attributes, self.table_name)
		print("Connected succesfully to "+database+" table name "+self.table_name)


	def select_lpg_by_name(self, name):
		return self.select_string_data("Name", name)


	def select_lpg_by_weight(self, Weight):
		return self.select_integer_data("Weight", weight)


	def select_lpg_by_price(self, Price):
		return self.select_integer_data("Price", price)


	def select_lpg_by_id(self, id):
		return self.select_integer_data("ID", id)

		
	def insert_lpg(self, name, weight, price):
		self.insert_data(f'("{name}",{weight},{price})')


	def delete_lpg(self, ID):
		self.delete_data("ID", ID)


	def change_price(self, ID, new_price):
		self.update_data("Price", new_price, "ID", ID)


	def change_price_by_name(self, Name, new_price):
		self.update_data("Price", new_price, "ID", ID)


	def get_all(self):
		return self.select_data_all()



class Customer(DatabaseHandler):


	def __init__(self, database, table_name):
		self.table_name = table_name
		self.table_attributes = "(Firstname, Lastname)"
		self.customer_connection = database
		super().__init__(self.customer_connection, self.table_attributes, self.table_name)
		print("Connected succesfully to "+database+" table name "+self.table_name)


	def select_customer_by_firstname(self, firstname):
		return self.select_string_data("Firstname", firstname)


	def select_customer_by_lastname(self, lastname):
		return self.select_string_data("Lastname", lastname)


	def select_customer_by_id(self, id):
		return self.select_integer_data("ID", id)

		
	def insert_customer(self, firstname, lastname):
		return self.insert_data(f'{firstname},{lastname}')


	def delete_customer(self, ID):
		return self.delete_data("ID", ID)


	def change_customer_firstname(self, ID, firstname):
		self.update_data("Firstname", firstname, "ID", ID)


	def change_customer_lastname(self, ID, lastname):
		self.update_data("Lastname", lastname, "ID", ID)


	def get_all(self):
		return self.select_data_all()


class Orders(DatabaseHandler):


	def __init__(self, database, table_name):
		self.table_name = table_name
		self.table_attributes = "(DateLog, LPG, Customer, PaidAmount, Fullypaid, Delivered)"
		self.order_connection = database
		super().__init__(self.order_connection, self.table_attributes, self.table_name)
		print("Connected succesfully to "+database+" table name "+self.table_name)


	def select_order_by_date(self, date):
		return self.select_string_data("DateLog", date)

	def select_order_by_id(self, id):
		return self.select_string_data("ID", id)


	def select_order_by_paidamount(self, price):
		return self.select_string_data("PaidAmount", price)


	def select_order_by_fullypaid_is_true(self, boolean):
		return self.select_integer_data("Fullypaid", boolean)

		
	def insert_order(self, date, lpg, customer, paidamount, fullypaid, delivered):
		self.insert_data(f' "{date}", "{lpg}" , "{customer}" ,{paidamount},{fullypaid}, {delivered}')


	def delete_order(self, ID):
		self.delete_data("ID", ID)


	def get_all(self):
		return self.select_data_all()


def x(**kwargs):
	print(kwargs)

if __name__ == "__main__":
	LPG_TABLE_NAME = "LPG"
	CUSTOMER_TABLE_NAME = "Customer"
	ORDER_TABLE_NAME = "Orders"
	lpg = LPG("lpg_database.db", LPG_TABLE_NAME)
	cust = Customer("lpg_database.db", CUSTOMER_TABLE_NAME)
	ors = Orders("lpg_database.db", ORDER_TABLE_NAME)
	#print(ors.get_all())
	#print(cust.get_all())
	#print(lpg.get_all())

	l = LPGDataObject()
	l.set_weight_only(12)
	print(l.__dict__)
	print(l.get_weight())
	#lpg.select_lpg_by_name(l.get_weight())