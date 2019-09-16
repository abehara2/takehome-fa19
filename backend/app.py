from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/contacts", methods=['GET'])
def get_all_contacts():
    param = request.args.get('hobby')
    contacts = db.get('contacts')
    if (param is None):
        return create_response({"contacts": contacts})
    hobbies = []
    for contact in contacts:
        if (contact.get("hobby") == param):
            hobbies.append(contact)
    if (len(hobbies) == 0):
        return create_response(status=404, message="No contact with this hobby exists")
    return create_response({"content": hobbies})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="No contact with this id exists")
    db.deleteById('contacts', int(id))
    return create_response(message="Contact deleted")


# TODO: Implement the rest of the API here!

@app.route("/contacts/<id>", methods=['GET'])
def getById(id):
    contact = db.getById('contacts', int(id))
    if contact is None:
        return create_response(status=404, message="No contact with this id exists")
    return create_response(contact)

@app.route("/contacts", methods=['POST'])
def createContact():
    input = request.json
    if input is None:
         return create_response(status = 422, message = "You are missing: input")
    error = ""
    name = input.get("name")
    flag = 0
    if name is None:
        flag = 1
        error = error + " name "
    nickname = input.get("nickname")
    if nickname is None:
        flag = 1
        error = error + " name "
    hobby = input.get("hobby")
    if hobby is None:
        flag = 1
        error = error + " hobby "
    if flag == 1:
        return create_response(status = 422, message = "You are missing:" + error)
    new_contact = db.create("contacts", input)
    return create_response(new_contact, status = 201)

@app.route("/contacts/<id>", methods=['PUT'])
def updateContact(id):
    input = request.json
    contact = db.getById('contacts', int(id))
    if contact is None:
        return create_response(status=404, message="No contact with this id exists")
    if input is None:
        return create_response(status = 422, message = "You are missing: input")
    namep = input.get("name")
    hobbyp = input.get("hobby")
    if not (namep is None):
        contact.update(name = namep)
    if not (hobbyp is None):
        contact.update(hobby = hobbyp)
    newContact = (db.updateById("contacts", id, contact))
    return create_response(contact, status = 201)
"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
