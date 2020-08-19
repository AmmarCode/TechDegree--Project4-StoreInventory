STORE INVENTORY
---------------
Python Web Development

Tech degree Project 4

Created by AmmarCode
 
 
INTRODUCTION
------------
Store inventory management program. Create or get products lists from a csv file, Save it in a SQLite3 database.

User can view inventory by product id.

User can Add new products to the database.

User can create a back up csv file for the database

Program will prevent creating duplicate products and will allow updates to existing products by adding them using the same stored name with updated details.


REQUIREMENTS
------------
Python

import datetime

import csv

import os

from collections import OrderedDict

from peewee import *
