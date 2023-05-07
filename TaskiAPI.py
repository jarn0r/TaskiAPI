from flask import Flask, request, jsonify, abort
import uuid

app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]


@app.route('/todolist/<list_id>', methods=['GET', 'DELETE']) #/<list_id>
def handle_list(list_id):
    if request.method == 'GET':
        print(list_id)
        return jsonify([i for i in todos if i['list'] == list_id])

    elif request.method == 'DELETE':
        print(list_id)
        for i in todo_lists:
            if i['id'] == list_id:
                print("Wird entfernt: {}".format(i['id']))
                todo_lists.remove(i)
        return "Wurde entfernt",200
    
@app.route('/todo-list', methods=['POST'])
def createList():
    new_list = request.get_json()
    print('Got new list to be added: {}'.format(new_list))
    new_list['id'] = uuid.uuid4()
    #new_list['name'] = 
    print(new_list)
    todo_lists.append(new_list)
    return jsonify(new_list), 200


@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['POST', 'PUT', 'DELETE'])
def createEntry(list_id, entry_id):
    if request.method == 'POST':
        new_entry = request.get_json()
        new_entry['list'] = list_id
        new_entry['id'] = uuid.uuid4()
        todos.append(new_entry)
        return jsonify([i for i in todos if i['list'] == list_id]), 200
        
    elif request.method == 'PUT':
        updated_entry = request.get_json()
        return jsonify(updated_entry)
        
    elif request.method == 'DELETE':
        for i in todos:
            if i['list'] == list_id:
                if i['id'] == entry_id:
                    todos.remove(entry_id)
                    return "success", 200
                    
    elif request.method == 'GET' :
        abort("Nicht zugelassen",405)
        
    pass

app.run(host='0.0.0.0', port=5000)

    