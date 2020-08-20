from flask import Blueprint, render_template, request, redirect
from .models import Link
from .extensions import db
from .auth import requires_auth

short = Blueprint('short', __name__)


@short.route('/<short_url>')
def redirect_to_url(short_url):
    # we redirect to the original_url in our db that matches the new, shorter url
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    # note that we had another person use a link from our db
    link.visits += 1
    db.session.commit()
    return redirect(link.original_url)


@short.route('/')
@requires_auth
def index():
    return render_template('index.html')


@short.route('/add_link', methods=['POST'])
@requires_auth
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    # adding the original and shortened url to the db
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html',
                           new_link=link.short_url,
                           original_url=link.original_url)


@short.route('/stats')
@requires_auth
def stats():
    links = Link.query.all()

    return render_template('stats.html', links=links)


@short.errorhandler(404)
def page_not_found(e):
    return '<h1> Error 404 <br /> Hey Bud, not much here rn. </h1><p>Maybe try another link?</p>', 404
