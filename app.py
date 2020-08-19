import datetime
import csv
import os
from collections import OrderedDict

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = CharField(max_length=100, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and tables if they don't exist."""
    db.connect()
    db.create_tables([Product], safe=True)
    clean_data()


def clear():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def clean_data():
    """Clean data"""
    with open('inventory.csv', newline='') as csvfile:
        inventory_reader = csv.DictReader(csvfile, delimiter=',')
        rows = list(inventory_reader)
        for row in rows:
            row['product_name'] = row['product_name']
            row['product_price'] = (row['product_price']
                                    .strip('$').replace('.', ''))
            row['product_price'] = int(row['product_price'])
            row['product_quantity'] = int(row['product_quantity'])
            row['date_updated'] = datetime.datetime.strptime(
                row['date_updated'], "%m/%d/%Y").date()

            try:
                Product.create(product_name=row['product_name'],
                               product_price=row['product_price'],
                               product_quantity=row['product_quantity'],
                               date_updated=row['date_updated'])
            except IntegrityError:
                product_record = Product.get(product_name=row['product_name'])
                product_record.product_price = (row['product_price'])
                product_record.product_quantity = row['product_quantity']
                product_record.date_updated = datetime.datetime.now().date()
                product_record.save()


def menu_loop():
    """Show menu"""
    choice = None
    clear()
    while True:
        print('='*6 + ' Menu ' + '='*6 + '\n\n')
        print("Enter 'q' to quit.\n")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        try:
            choice = input('Action: ').lower().strip()
            if choice not in menu and choice != 'q':
                raise ValueError('Enter an option from menu')
        except ValueError as err:
            print(f'Invalid input {err}')
        else:
            if choice in menu:
                clear()
                menu[choice]()

        if choice == 'q':
            print('\n\n'+'='*14+"\nSee you later!\n"+'='*14)
            break


def add_product():
    """Add a product"""
    while True:
        try:
            prod_name = input("Enter product name: ")
            clear()
            prod_price = input("Enter product price in the form of"
                            "(example: $1:50):  ").strip('$').replace('.', '')
            prod_price = int(prod_price)
            clear()
            prod_quantity = int(input("Etner product quantity in digits(example: 123): "))
            date_added = datetime.datetime.now().date()
            clear()
        except ValueError:
            print("You must enter required details as shown in example.")
        else:
            if prod_name and prod_price and prod_quantity:
                confirm = input("Save product? [Y/N]: ").lower().strip()
                clear()
                if confirm == 'y':
                    try:
                        added_prod = Product.create(product_name=prod_name,
                                                    product_price=prod_price,
                                                    product_quantity=prod_quantity,
                                                    date_updated=date_added)
                        if added_prod.get(Product.product_name) in Product.get(Product.product_name):
                            if added_prod.date_updated > Product.date_updated:
                                continue
                    except IntegrityError:
                        product_record = Product.get(product_name=prod_name)
                        product_record.product_price = prod_price
                        product_record.product_quantity = prod_quantity
                        product_record.date_updated = datetime.datetime.now().date()
                        product_record.save()
                    else:
                        break
            break


def view_product():
    """View a product"""
    while True:
        try:
            product = Product.get(Product.product_id)
            len_inv = product.select().count()
            Product.select()
            search_id = int(
                input(f"Enter Product id between 1 & {len_inv}:> "))
            product = Product.get(Product.product_id == search_id)
            if search_id not in Product.product_id:
                raise DoesNotExist
        except DoesNotExist:
            print(f'{search_id} Product id not in inventory list, Try again')
        except ValueError:
            print(f'{search_id} Product id not in inventory list, Try again')
        else:
            clear()
            print(f'Product id: {product.product_id}')
            print(f'Product: {product.product_name}')
            print(f'Price: ${"{:.2f}".format(product.product_price/100)}')
            print(f'Quantity: {product.product_quantity}')
            print(f'Date updated: {product.date_updated}')
            print('\n\nEnter) To pick another product')
            print('Q) Return to main menu')

            next_action = input('Action: [Enter/Q]').lower().strip()
            clear()
            if next_action == 'q':
                break


def backup_inventory():
    """Backup inventory"""
    with open('backup.csv', 'a') as csvfile:
        fieldnames = ['product_id', 'product_name', 'product_price',
                      'product_quantity', 'date_updated']
        productwiter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        productwiter.writeheader()
        prod_lst = Product.select().order_by(Product.product_id.asc())
        for produ in prod_lst:
            productwiter.writerow({
                'product_id': produ.product_id,
                'product_name': produ.product_name,
                'product_price': produ.product_price,
                'product_quantity': produ.product_quantity,
                'date_updated': produ.date_updated,
            })
        print("backup.csv was created successfully!")


menu = OrderedDict([
    ('v', view_product),
    ('a', add_product),
    ('b', backup_inventory),
])

if __name__ == '__main__':
    initialize()
    menu_loop()
