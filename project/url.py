import os

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from hashids import Hashids
from app import app
from . import db
from .models import Urls

url = Blueprint('url', __name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
hashids = Hashids(min_length=4, salt='34j23k4jhk324h324')

@url.route('/shorten')
@login_required
def shorten():
    return render_template('shortenurl.html')

@url.route('/shorten', methods=['POST'])
@login_required
def shorten_post():

    url = request.form.get('url')

    if not url:
        flash('A URL is required')
        return redirect(url_for('url.shorten'))

    url_data = Urls(
        original_url=url,
        generated_user=current_user.id
    )

    db.session.add(url_data)
    db.session.commit()

    short_url = url_data.id
    hashid = hashids.encode(short_url)
    short_url = request.host_url + hashid

    return render_template('index.html', short_url=short_url)


@url.route('/stats')
def stats():

    db_urls = Urls.query.all()

    fucking_urls = []

    for u in db_urls:
        u = dict(u)
        u['short_url'] = 1
        fucking_urls.append(u)


    return render_template('stats.html', urls=fucking_urls)
