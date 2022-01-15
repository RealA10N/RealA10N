import io
from flask import Flask, send_file, make_response
from art import GitHubBanner

app = Flask(__name__)
dynamicbanner = GitHubBanner('github-data.json')


@app.route('/github-banner.png')
def github_banner():
    arr = io.BytesIO()

    img = next(dynamicbanner)
    img.save(arr, format='png')

    arr.seek(0)

    re = make_response(send_file(arr, mimetype='image/png'))
    re.headers['Cache-Control'] = ', '.join((
        'max-age=0',
        'no-cache',
        'no-store',
        'must-revalidate',
    ))
    return re
