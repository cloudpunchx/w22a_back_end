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
# WORKING BUT NEED TO COME BACK AND EDIT RESPONSES
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
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(result), 500)

# Clients can DELETE candy by giving an ID and Name (I wanted them to use both to confirm delete)
# circle back to fix, it completes delete and sends back the ELSE with 500 error, same with PATCH
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
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(result), 500)

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
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(result), 500)

if (production_mode == True):
    print("Running server in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Running Server in Testing Mode.")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)