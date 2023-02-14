from flask import Flask, request, make_response, jsonify
from dbhelpers import run_statement
from dbcreds import production_mode
from helpers import check_data

app = Flask(__name__)

# Clients can GET/read all candy posts
@app.get('/api/candy')
def get_candy():
    result = run_statement("CALL get_all_candy()")
    keys = ["candyName", "variety"]
    response = []
    if (type(result) == list):
        for candy in result:
            response.append(dict(zip(keys, candy)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 500)

# Clients can PATCH/edit candy name for existing candy
@app.patch('/api/candy')
def patch_candy_name():
    """
    Expects 2 Arguments:
    candyId, candyName
    """
    required_data = ['candyId', 'candyName']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    candy_id = request.json.get('candyId')
    candy_name = request.json.get('candyName')
    result = run_statement("CALL patch_candy(?,?)", [candy_id, candy_name])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify(f"Successfully edited Candy: {candy_name}"), 200)
        elif result[0][0] == 0:
            return make_response(jsonify(f"Edit unsuccessful for Candy, please verify candy ID and name."), 400)
    else:
        "There has been an unexpected error."

# Clients can DELETE candy by giving an ID and Name (I wanted them to use both to confirm delete)
@app.delete('/api/candy')
def delete_candy():
    """
    Expects 2 Arguments:
    candyId, candyName
    """
    required_data = ['candyId', 'candyName']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    candy_id = request.json.get('candyId')
    candy_name = request.json.get('candyName')
    result = run_statement("CALL delete_candy(?,?)", [candy_id, candy_name])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify(f"Successfully deleted candy {candy_name}."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify(f"Delete unsuccessful for candy {candy_name}, check candy ID and name."), 400)
    else:
        "There has been an unexpected error."


# Clients can POST/create candy by giving a name and category
@app.post('/api/candy')
def post_candy():
    """
    Expects 2 Arguments:
    candyName, category
    """
    required_data = ['candyName', 'category']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    candy_name = request.json.get('candyName')
    category = request.json.get('category')
    result = run_statement("CALL post_candy(?,?)", [candy_name, category])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify(f"Successfully posted Candy: {candy_name}."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify(f"Post unsuccessful for candy {candy_name}, check candy ID and name."), 500)
    elif "candy_UN_name" in result:
        return make_response(jsonify(f"{candy_name} is a duplicate entry, please enter a unique candy name."), 400)
    else:
        return "There has been an unexpected error."

if (production_mode == True):
    print("Running server in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Running Server in Testing Mode.")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)