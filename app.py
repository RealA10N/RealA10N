import io
from flask import Flask, send_file
from art import GitHubBanner


def start():
    app = Flask(__name__)
    dynamicbanner = GitHubBanner('github-data.json')

    @app.route('/github-banner.png')
    def github_banner():
        arr = io.BytesIO()

        img = next(dynamicbanner)
        img.save(arr, format='png')

        arr.seek(0)
        return send_file(arr, mimetype='image/png')

    return app


if __name__ == '__main__':
    from waitress import serve
    serve(start())
