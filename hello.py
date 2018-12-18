import json

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
	with open('db.txt', 'r') as f:
		items = json.load(f)
	if request.method == 'POST':
		item = request.form.get('item')
		quantity = request.form.get('quantity')
		update = request.form.get('update')
		delete = request.form.get('delete')
#		for item, quantity in items.items():
		if update: 
			items.update({item: quantity})
			with open('db.txt', 'w') as f2:
				json.dump(items, f2)
		elif delete:
			items.pop(item)
			with open('db.txt', 'w') as f2:
				json.dump(items, f2)
	return render_template('hello.html', items=items)


