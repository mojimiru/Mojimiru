from io import BytesIO
import json
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.subset import Options,load_font,Subsetter,save_font
from pathlib import Path
from flask import Flask, request, abort, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True
)

fontmap = json.loads(Path('./assets/fontmap.json').read_text(encoding="utf-8"))

def getGlyphSvg(fontpath:Path,text:str) -> BytesIO:
    io = BytesIO()
    options = Options()
    options.name_IDs = []
    options.obfuscate_names = True
    options.flavor = 'woff'

    font = load_font(fontpath, options)
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    save_font(font, io, options)
    font.close()
    return io

@app.route('/') #type: ignore
def getfont():
    try:
      if request.method == 'GET':
        fontname = request.args.get('font', '')
        texts = request.args.get('text', 'sample text')
        print(f'fontname:{fontname},texts:{texts}')
        if fontname in fontmap:
          fontpath = Path(fontmap[fontname])
          subset = getGlyphSvg(fontpath,texts)
          subset.seek(0)
          return send_file(subset,download_name='font.woff',mimetype='application/font-woff')
          # return "aaaaaa"
        return abort(400)
      else:
        return abort(400)
    except Exception as e:
        return str(e)
