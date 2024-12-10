from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import re
import json
import os

db = TinyDB(os.getenv("DB_PATH"))
app = Flask(__name__)

date_regex = re.compile(r"^(?:\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{2}-\d{2})$")
phone_regex = re.compile(r"^\+7 \d{3} \d{3} \d{2} \d{2}$")
email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
def determine_field_type(value):
    if date_regex.match(value):
        return "date"
    elif phone_regex.match(value):
        return "phone"
    elif email_regex.match(value):
        return "email"
    else:
        return "text"


@app.route("/get_form", methods=["POST"])
def get_form():
    request_data = request.form.to_dict()
    for template in db:
        if all(
            k in request_data
            and determine_field_type(request_data[k]) == template[k]
            for k in template
            if k != "name"
        ):
            return jsonify(template["name"])

    field_types = {
        field: determine_field_type(value) for field, value in request_data.items()
    }
    return jsonify(field_types)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
