"""
This file initializes a Python MongoDB client that can be shared across files.
Since the only other code file is `app.py`, the code below could be moved to
`app.py`, but with larger codebases where multiple files interact with the
MongoDB client, this file will come in handy.
"""

import os

from dotenv import load_dotenv
from pymongo import MongoClient

# This is only a sample, so the `.env.sample` is used. For your project, you should
# use `.env`. BE SURE TO INCLUDE THIS FILE IN YOUR `.gitignore` FILE OR ELSE YOUR
# MONGODB CREDENTIALS WILL BE PUBLISHED TO GITHUB!
load_dotenv('.env.sample')

client = MongoClient(os.getenv("MONGO_URI_MASTER"))
