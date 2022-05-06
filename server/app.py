from flask import Flask

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/') #type: ignore
def index():
    return "HELLO"

if __name__ == '__main__':
    app.run()
    # getGlyphSvg(Path(r'assets\fonts\MRT-まるこいあすα かなのみ.ttf'),"wind")
