from random import randrange

from flask import flash, Flask, redirect, render_template, url_for

from .models import URLMap
from . import app, db