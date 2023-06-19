from flask import Flask, request, jsonify, abort, render_template
import uuid
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "https://editor.swagger.io/"}})

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = '17983c31-2098-46e4-85d2-2934681fd8f6'
todo_2_id = '8a9f7b25-afdf-4b7f-9102-63b74d1ee662'
todo_3_id = '8a9f7b25-a000-4000-9002-63b74d1ee333'
todo_4_id = '10000000-2000-4000-8000-200000000000'

todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

@app.route('/')
def banner():
    return render_template('index.html'),200

@app.route('/overview')
def overview():
    return render_template('overview.html', todo_lists=todo_lists),200

@app.route('/todolist/<list_id>', methods=['GET', 'DELETE']) #/<list_id>
def handle_list(list_id):
    if request.method == 'GET':
        myTodo =[]
        print(list_id)
        for i in todos:
            if str(i['list']) == str(list_id):
                myTodo.append(i)
        for i in todo_lists:
            if str(i['id']) == list_id:
                list_name = i['name']
        #return jsonify([i for i in todos if i['list'] == list_id])
        return render_template('todolist.html', todos=myTodo, todolist=list_name)

    elif request.method == 'DELETE':
        print(list_id)
        for i in todo_lists:
            if i['id'] == list_id:
                print("Wird entfernt: {}".format(i['id']))
                todo_lists.remove(i)
            else:
                print(i['id'])
        return "Wurde entfernt",200
    
@app.route('/todolist', methods=['POST'])
def createList():
    new_list = request.get_json()
    print('Got new list to be added: {}'.format(new_list))
    new_list['id'] = uuid.uuid4()
    #new_list['name'] = 
    print(new_list)
    todo_lists.append(new_list)
    return jsonify(new_list), 200

@app.route('/todolist/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def editEntry(list_id, entry_id):    
    if request.method == 'PUT':
        updated_entry = request.get_json()
        for i in todo_lists:
            if str(i['id']) == str(list_id):
                for j in todos:
                    if str(j['id']) == str(entry_id):
                        print("Hier")
                        j['name'] = updated_entry.get('name', j['name'])
                        j['description'] = updated_entry.get('description', j['description'])
                        j['list'] = updated_entry.get('list', j['list'])
                        print(j)
        return jsonify(updated_entry),200
        
    elif request.method == 'DELETE':
        for i in todo_lists:
            if str(i['id']) == str(list_id):
                for j in todos:
                    if str(j['id']) == str(entry_id):
                        todos.remove(j)
                        return "success", 200

    elif request.method == 'GET' :
        abort("Nicht zugelassen",405)

@app.route('/todolist/<list_id>/entry', methods=['POST'])
def createEntry(list_id):
    newEntry = request.get_json(force=True)
    entry = {'id': uuid.uuid4()}
    entry['name'] = newEntry['name']
    entry['description'] = newEntry['description']
    entry['list'] = list_id
    todos.append(entry)
    print("New Entry: {}".format(entry))
    return jsonify(entry), 200

app.run(host='0.0.0.0', port=5000)

    