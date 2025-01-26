
#!/usr/bin/env python3
"""
This module contains the blueprint for the API views.

It defines the `app_views` blueprint object, which is used
to group related API endpoints. The blueprint is registered
with the Flask application and has a URL prefix of '/api/v1'.

The module also imports the necessary views for the API
endpoints and loads user data from a file.
"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *
User.load_from_file()
