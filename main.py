from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from sqlalchemy.exc import NoResultFound

from models import db, ShortLink
from utils import set_cache, id_generator, check_key

shortlink_app = Blueprint('shortlink', __name__,
                          template_folder='templates')


@shortlink_app.route('/')
def index():
    user_links = None
    if current_user.is_authenticated:
        user_links = db.session.query(ShortLink).filter(ShortLink.user == current_user).all()

    return render_template('index.html', user_links=user_links)


@shortlink_app.route('/make', methods=['POST'])
def make_short_link():
    data = request.form
    custom_code = data.get('custom_code', None)
    expire = data.get('expire', 5 * 60)
    otp = data.get('otp', None)
    private = data.get('private', False)

    if not expire:
        expire = 5 * 60

    # if custom_code and len(custom_code) < 8:
    #     return render_template("index.html", error='Custom code must be 8')

    if custom_code and check_key(custom_code):
        return render_template("index.html", error='Custom code exist!')
    if custom_code:
        generated_id = custom_code
    else:
        generated_id = id_generator()
        while True:
            if not check_key(generated_id):
                break
            generated_id = id_generator()

    short_link = ShortLink(main_url=data.get('main_url'), short_url=generated_id, private=bool(private), expire=expire)
    set_cache(generated_id, data.get('main_url'), expire)
    if current_user.is_authenticated:
        short_link.user = current_user
        if otp:
            short_link.otp_code = otp

    db.session.add(short_link)
    db.session.commit()
    return render_template("index.html", result=request.host_url + generated_id, main_url=data.get('main_url'))


@shortlink_app.route('/<short_text>', methods=['GET'])
def handle_request(short_text):
    if check_key(short_text):
        try:
            short_link = db.session.query(ShortLink).filter(ShortLink.short_url == short_text).one()
            if short_link.private and current_user != short_link.user:
                return render_template("errors.html", error='Only created user allow to access to short link.')
            if short_link.otp_code:
                return render_template("otp.html", short_key=short_link.short_url)
            short_link.redirection_count += 1
            db.session.commit()
            return redirect(short_link.main_url, code=302)
        except NoResultFound:
            pass
    return render_template("errors.html", error='Requested short link  expired or does not exist.')


@shortlink_app.route('/process_otp', methods=['POST'])
def process_otp():
    otp = request.form.get('otp', None)
    short_key = request.form.get('short_key', None)

    if otp:
        try:
            short_link = db.session.query(ShortLink).filter(ShortLink.short_url == short_key).one()
            print(otp, flush=True)
            if short_link.otp_code == otp:
                short_link.redirection_count += 1
                db.session.commit()
                return redirect(short_link.main_url, code=302)
        except NoResultFound:
            pass
    return render_template("errors.html", error='Wrong Password', short_key=short_key)
