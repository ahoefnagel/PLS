import json, csv, os, zipfile, shutil

from Book import Book
from Account import Account
from StockItem import StockItem
from BorrowItem import BorrowItem
from datetime import datetime
running = True
current_account = None

books = []
authors = []
accounts = []
borrow_items = []
stock_items = []

'''
The system must feature the following functions:
-V Searching for a book. 
	This shows if there are book items in the library present for this book and if they are available. 
	The search criteria must cover various keys, such as title, author, ISBN, etc, and combinations of keys.
- Making a book loan for an available book item. 
-V Adding new customers.
-V Adding new books.
-V Making a backup of the data in the system (catalog of books and book items, data in the loan administration, list of customers, etc.)
-V Recovering the library from a backup.
'''


def load():
	if os.path.isfile('data/accounts.csv'):
		path = 'data/accounts.csv'
	else:
		path = 'data/FakeNameSet20.csv'
	with open(path, mode='r') as csv_file:
		csv_reader = csv.reader(csv_file)
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				accounts.append(
					Account(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
							row[10]))
				line_count += 1
		csv_file.close()

	if os.path.isfile('data/books.json'):
		path = 'data/books.json'
	else:
		path = 'data/booksset1.json'

	js_books = json.load(open(path, 'r'))
	for js_book in js_books:
		book = Book(js_book['author'], js_book['country'], js_book['image_link'], js_book['language'],
					js_book['link'], js_book['pages'], js_book['title'], js_book['year'])
		books.append(book)


def save():
	a = open("data/accounts.csv", "w")
	a.write('Number,Gender,NameSet,GivenName,Surname,StreetAddress,ZipCode,City,EmailAddress,Username,TelephoneNumber')
	a.close()
	open("data/books.json", "w").close()
	open("data/borrow_items.json", "w").close()
	open("data/stock_items.json", "w").close()

	for account in accounts:
		f = open("data/accounts.csv", "a")
		f.write(account.to_csv())
		f.close()
		pass

	f = open("data/books.json", "a")
	f.write(json.dumps([b.__dict__ for b in books], indent=2))
	f.close()
	pass

	f = open("data/borrow_items.json", "a")
	f.write(json.dumps([b.__dict__ for b in stock_items], indent=2))
	f.close()
	pass

	f = open("data/stock_items.json", "a")
	f.write(json.dumps([b.__dict__ for b in borrow_items], indent=2))
	f.close()
	pass


def main():
	global running, books, authors
	load()
	print("Welcome to the Python Library System v1.0 \nPlease give an input")
	print("Or use 'help' for all the commands \n---------------------------")
	while running:
		user_input = input()
		
		if "search" in user_input.lower():
			bookset = set()
			if '-t' in user_input.lower():
				for book in books:
					if user_input.split('-t')[1].lstrip() in book.title.lower():
						bookset.add(book.to_dict())
				pass
			if '-w' in user_input.lower():
				for book in books:
					if user_input.split('-w')[1].lstrip() in book.author.lower():
						bookset.add(book.to_dict())
				pass
			if '-y' in user_input.lower():
				for book in books:
					if int(user_input.split('-y')[1].lstrip()) == book.year:
						bookset.add(book.to_dict())

			for book in bookset:
				print(json.dumps(book))
			pass
		elif user_input.lower() in "search help":
			print("A list of available commands for search: ")
			print("search -t \t\t Search for a title")
			print("search -w \t\t Search for a writer")
			print("search y- \t\t Search for a year")
			print("search \t\t\t Search for anything containing the search")
			pass
		elif user_input.lower() in "customer create":
			gender = input('Please enter the gender:\n')
			name_set = input('Please enter the name set:\n')
			given_name = input('Please enter the given name:\n')
			surname = input('Please enter the surname:\n')
			street_address = input('Please enter the street address:\n')
			zipcode = input('Please enter the zipcode:\n')
			city = input('Please enter the city:\n')
			email_address = input('Please enter the email address:\n')
			telephone_number = input('Please enter the telephone number:\n')
			username = input('Please enter the username:\n')
			accounts.append(
				Account(
					accounts[len(accounts)-1].id + 1,
					gender,
					name_set,
					given_name,
					surname,
					street_address,
					zipcode,
					city,
					email_address,
					user_input,
					telephone_number,)
			)
			pass
		elif user_input.lower() in "book create":
			title = input('Please enter the title:\n')
			author = input('Please enter the author:\n')
			country = input('Please enter the country:\n')
			image_link = input('Please enter the image link:\n')
			language = input('Please enter the language:\n')
			link = input('Please enter the link:\n')
			pages = input('Please enter the pages:\n')
			year = input('Please enter the year:\n')

			books.append(
				Book(
					author,
					country,
					image_link,
					language,
					link,
					pages,
					title,
					year,
				)
			)

			pass
		elif user_input.lower() in "stock":
			i = 0
			for book in books:
				print(str(i+1) + '} ' + book.to_dict())
				i+=1

			item = int(input('for which book do you want to change the stock: \n')) - 1
			stock = int(input('new stock: \n'))

			stock_items.append(
				StockItem(
					books[item],
					stock
				)
			)

		elif user_input.lower() in "lend":
			i = 0
			for stock_item in stock_items:
				print(str(i + 1) + '} ' + stock_item.to_msv())
				i+=1

			book = int(input('which book do you want to lend: \n')) - 1

			i = 0
			for account in accounts:
				print((i + 1) + '} ' + account.to_msv())
				i+=1

			account = int(input('which user do you want to lend it to: \n')) - 1

			borrow_items.append(
				BorrowItem(
					books[book],
					accounts[account],
				)
			)
		elif user_input.lower() in "return":
			i = 0
			for borrow_item in borrow_items:
				if borrow_item.return_date is None:
					print(str(i + 1) + '} ' + borrow_item.to_msv())
				i+=1
			book = int(input('which book do you want to return: \n')) - 1

			borrow_items[i].return_date = datetime.now()

			pass
		elif user_input.lower() in "help":
			print("A list of available commands: ")
			print("switch account \t\t change the current user")
			print("backup \t\t create a backup of the users and books")
			print("quit \t\t exit the system")
			pass
		elif user_input.lower() in "backup":
			zipf = zipfile.ZipFile('backup_%s.zip' % (datetime.now().strftime("%m_%d_%Y__%H_%M_%S")), 'w', zipfile.ZIP_DEFLATED)
			for root, dirs, files in os.walk('data/'):
				for file in files:
					zipf.write(os.path.join(root, file))
			zipf.close()
			pass
		elif user_input.lower() in "backup load":
			print('available backups:')
			for root, dirs, files in os.walk('.'):
				for file in files:
					if '.zip' in file:
						print(file)
			user_input = input('Please enter the name of the backup you wish to recover:\n')
			try:
				shutil.rmtree('data/')
			except:
				pass
			with zipfile.ZipFile(user_input, 'r') as zip:
				zip.extractall()
				print('Backup has been loaded!')
				pass
		elif user_input.lower() in "quit":
			running = False
		else:
			print("Command not found, please try something else or use 'help' for a list of available commands.")
		save()

if __name__ == "__main__":
	main()
