from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import re
import json
import os

db = TinyDB('forms.json')
print("__________\n")
db.insert({
    "name": "user_form",
    "user_email": "email",
    "user_name": "text",
    "user_phone": "phone"
})
print(db.all())

app = Flask(__name__)

def determine_field_type(value):
    if re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', value) or re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        return "date"
    elif re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return "phone"
    elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        return "email"
    else:
        return "text"

@app.route('/get_form', methods=['POST'])
def get_form():
    request_data = request.form.to_dict()
    fields = request_data.keys()
    for k in request_data.keys() :
        print(k, request_data[k])
    
    for template in db:
        template_fields = template
        if all(k in request_data and determine_field_type(request_data[k]) == template_fields[k] for k in template_fields if k != 'name'):
            return jsonify(template['name'])
    
    field_types = {field: determine_field_type(value) for field, value in request_data.items()}
    return jsonify(field_types)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')