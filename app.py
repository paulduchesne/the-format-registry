import json
import pathlib
import rdflib
from flask import Flask, render_template

# load rdf data.

g = rdflib.Graph().parse(pathlib.Path.cwd() / 'public' / 'tfr' / 'tfr-triples' / 'tfr-format-triples.ttl')

# flask app.

app = Flask(__name__)

# render homepage.

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# render page.

@app.route('/fileformat/<path>', methods=['GET', 'POST'])
def page(path):
    page_data = g.serialize(format='json-ld')
    page_data = json.loads(page_data)
    page_data = [x for x in page_data if pathlib.Path(x['@id']).stem == path]
    if not len(page_data):
        return render_template('404.html')
    else:
        return render_template('fileformat.html', data=page_data[0])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
