import sqlite3
import sys

DB_FILE = 'db.sqlite'

def get_db():
	try:
		conn = sqlite3.connect(DB_FILE)
		c = conn.cursor()
		return conn, c
	except sqlite3.Error as e:
		print("SQLite Error: {}".format(e))
		sys.exit(0)

def create_db():
	conn, c = get_db()

	# ingredients
	try:
		c.execute("""CREATE TABLE IF NOT EXISTS ingredients (
			id integer primary key autoincrement,
			name varchar(200)
			)""")
		conn.commit()
	except sqlite3.Error as e:
		print("Error while creating ingredients table:\n{}".format(e))
		sys.exit(0)
	# print("[+] TABLE ingredients created !")

	# meals
	try:
		c.execute("""CREATE TABLE IF NOT EXISTS meals (
			id integer primary key autoincrement,
			name varchar(200),
			ingredients text
			)""")
		conn.commit()
	except sqlite3.Error as e:
		print("Error while creating meals table:\n{}".format(e))
		sys.exit(0)
	# print("[+] TABLE meals created !")

	conn.close()

def insert_meals():
	conn, c = get_db()

	meals = {'crepes':'milk,sugar,flour', 'hamburger':'beef,tomato,salad,bread', 'chilly con carne':'chilly,beef,bean',\
	'curry chicken':'chicken,curry,fresh cream', 'coco chicken':'coconut milk,chiken', 'beuf bourgigon':'beef,wine,carrot'}

	try:
		for k,i in meals.items():
			c.execute("insert into meals(name, ingredients) select ?,? where not exists(select 1 from meals where name = ?);", (k, i, k))
	except sqlite3.Error:
		print("Error insert meals\n{}".format(e))
		return
	

	conn.commit()
	conn.close()

	# print("[+] Meals added !")

def insert_ingredients():
	conn, c = get_db()

	ingredients = ['chicken', 'milk', 'sugar', 'flour', 'beef', 'bean', 'curry', 'chilly', 'coconut milk', 'wine', 'carrot',\
	'fresh cream', 'bread', 'tomato', 'salad']
	for ingredient in ingredients:
		c.execute("insert into ingredients(name) select ? where not exists(select 1 from ingredients where name = ?);", (ingredient, ingredient))

	conn.commit()
	conn.close()

	# print("[+] Ingredients added !")

def get_meals_by_ingredients(ingredients):
	ingredients = ingredients.split(',')
	conn, c = get_db()
	meals = []
	for ingredient in ingredients:
		c.execute("select * from meals where ingredients LIKE ?", ('%{0}%'.format(ingredient), ))
		res = c.fetchall()
		for meal in res:
			meals.append(meal[1])
	conn.close()
	return set(meals)

def print_meals():
	conn, c = get_db()
	c.execute("select name, ingredients from meals")
	meals = c.fetchall()
	for meal in meals:
		print(meal[0])
		for ingre in meal[1].split(','):
			print("\t{}".format(ingre))

	conn.close()

def count_all_ingredients():
	conn, c = get_db()
	c.execute("select ingredients from meals")
	res = c.fetchall()
	count = 0
	for ingredients in res:
		count += ingredients[0].count(',') + 1
	conn.close()
	return count

def count_meals():
	conn, c = get_db()

	c.execute("select count(*) from meals")

	# conn.close()
	return c.fetchall()[0][0]

def support(ingredients):
	conn, c = get_db()

	lmeals = count_meals()
	arg = '%{}%'.format('%'.join([z for z in ingredients.split(',')])) # boom
	c.execute("select count(*) from meals where ingredients like ?", (arg, ))
	count = c.fetchall()[0][0]

	conn.close()
	return '{}/{}'.format(count, lmeals)







if __name__ == '__main__':
	create_db()
	insert_meals()
	insert_ingredients()
	print("Meals available :")
	print_meals()
	print("----------------------------")
	if len(sys.argv) < 3:
		print("Usage: python {} operation[support only] ingredients".format(sys.argv[0]))
		print("Examp: python {} support \"beef,wine\"".format(sys.argv[0]))
		sys.exit(0)

	if sys.argv[1] == "support":
		support_ = support(sys.argv[2])
		print("supp({{{}}}) = {}".format(sys.argv[2], support_))

