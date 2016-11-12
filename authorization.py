import json;

settings_file_name = 'settings.json'
owner_field_name = 'owner_id'
admins_field_name = 'admins'


def is_admin(id):
    admins = json.loads(open(settings_file_name).read())[admins_field_name]
    return is_owner(id) or (int(id) in admins)


def is_owner(id):
    owner_id = json.loads(open(settings_file_name).read())[owner_field_name]
    return owner_id == int(id)


def add_admin(adder_id, adding_id):
    adding_id = int(adding_id)
    if not is_owner(adder_id):
        return False
    with open(settings_file_name) as f:
        data = json.load(f)
    if adding_id in data[admins_field_name]:
        return True
    data[admins_field_name].append(adding_id)

    with open(settings_file_name, 'w') as f:
        json.dump(data, f)

    return True


def delete_admin(deleter_id, deleting_id):
    deleting_id = int(deleting_id)
    if not is_owner(deleter_id):
        return False
    with open(settings_file_name) as f:
        data = json.load(f)
    if deleting_id not in data[admins_field_name]:
        return True
    data[admins_field_name].remove(deleting_id)

    with open(settings_file_name, 'w') as f:
        json.dump(data, f)

    return True


def get_admins(getter_id):
    if not is_owner(getter_id) and not is_admin(getter_id):
        return None
    admins = json.loads(open(settings_file_name).read())[admins_field_name]

    return admins
