class UserModel:
  def __init__(self, fpath):
    self.fpath = fpath
    self.__get_all_users__()


  def __get_all_users__(self):
    users = {}
    with open(self.fpath, "r") as f:
      for line in f:
        values = line.strip().split(",")
        if len(values) == 3:
          user_id, username, age = values
          users[int(user_id)] = {"user_id": user_id, "username": username, "age": age}

    self._users = users

    self._next_user_id = max(self._users.keys()) + 1

  # 避免重複call
  def __persist_users__(self):
      with open(self.fpath, "w") as f:
        for u in self._users.values():
          f.write(f"{u['user_id']},{u['username']},{u['age']}\n")

  def get_users(self, user_id, items=None, offset=None, filter_by=None, sort_by=None):
    if user_id is None:
      items = len(self._users) if items is None else items
      offset =  0 if offset is None else offset
      users = list(self._users.values())[offset:offset+items]
      return users if filter_by is None else self.filter(users, filter_by)
    elif user_id in self._users:
      return self._users[user_id]
    else:
      return {}

  def filter(self, users, filter_by):
    result = []
    for op in [">", "=", "<"]:
        if op in filter_by:
            # filter_by => age > 10
            # age, 10 = field, val
            # user = {"age":10, "username": andy}
            field, val = filter_by.split(op)
            field = field.strip()
            val = val.strip()
            for user in users:
                if field in user:
                    user_val = user.get(field)
                    if user_val is not None:
                        if op == "=" and user_val == val:
                            result.append(user)
                        elif op == ">" and user_val > val:
                            result.append(user)
                        elif op == "<" and user_val < val:
                            result.append(user)
    return result

  def sort(self, users, sort_by):
    if sort_by is None:
      return users
    else:
      # age.desc
      # field, val =sort_by.split(".")
        field, order = sort_by.split(".")
        if field in ["user_id", "username", "age"]:
            return sorted(users, key=lambda user: user[field], reverse=order=="desc")
        else:
            return []

  def new_user(self, username="", age=""):
    with open(self.fpath, "a") as f:
      f.write(f"{self._next_user_id},{username},{age}\n")
    user = {"user_id": self._next_user_id, "username": username, "age": age}
    self._users[self._next_user_id] = user
    self._next_user_id += 1
    return user

  def delete_user(self, user_id):
    if user_id in self._users:
      user = self._users.pop(user_id)
      self.__persist_users__()
      return user
    else:
      return {}

  def update_user(self, user_id, username=None, age=None):
    if user_id in self._users:
      user = self._users[user_id]
      if username is not None:
        user["username"] = username
      if age is not None:
        user["age"] = age
      self.__persist_users__()
      return user
    else:
      return []
