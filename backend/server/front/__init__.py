""" Client App """

from flask import Blueprint, render_template

client_bp = Blueprint('client_app', __name__,
                        url_prefix='',
                        static_url_path='/',
                        static_folder='./',
                        template_folder='./',
                        )

@client_bp.route('/')
def index():
    return render_template('index.html')