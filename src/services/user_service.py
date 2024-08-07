from models.user import save_user, get_all_users

def add_user(user_id, name, age):
    save_user(user_id, name, age)

def list_users():
    return get_all_users()
