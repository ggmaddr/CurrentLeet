def solution(queries):
    cloud_storage = {}
    result = []
    users = {}
    
    users["admin"]={"capacity": float("inf"), "files": cloud_storage}

    def add_file(cloud_storage, name, size):
        if name in cloud_storage:
            return "false"
        cloud_storage[name] = {"size": int(size)}
        return "true"

    def copy_file(users, name_from, name_to):
        
        for user_id, user in users.items():
            if name_from in user["files"] and "/" != name_from[:-1]:
                file_size = user["files"][name_from]
                if (
                    name_to not in user["files"]
                    and (user_id == "admin" or users[user_id]["capacity"] >= file_size)
                ):
                    user["files"][name_to] = file_size
                    if user_id != "admin":
                        users[user_id]["capacity"] -= file_size
                    return "true"
        return "false"
        
        # if name_from not in cloud_storage or "/" == name_from[:-1] or name_to in cloud_storage or "/" == name_from[:-1]:
            
        #     return "false"
        # cloud_storage[name_to] = {"size": cloud_storage[name_from]["size"]}
        # return "true"
    
    def get_file_size(cloud_storage, name):
        return str(cloud_storage.get(name, {}).get("size", ""))
    
    def find_file(cloud_storage, prefix, suffix):
        matching_files = []
        
        for name, file_info in cloud_storage.items():
            if name.startswith(prefix) and name.endswith(suffix):
                matching_files.append((name, file_info["size"]))

        if not matching_files:
            return ""

        # Sort files in descending order of size, and lexicographically in case of ties
        sorted_files = sorted(matching_files, key=lambda x: (-x[1], x[0]))
        
        # Format the result string
        result_str = ", ".join(f"{name}({size})" for name, size in sorted_files)
        return result_str
    def add_user(users, user_id, capacity):
        if user_id in users:
            return "false"
        users[user_id] = {"capacity": int(capacity), "files": {}}
        return "true"
    def add_file_by(users, user_id, name, size):
        
        if user_id not in users or name in users[user_id]["files"] or users[user_id]["capacity"] < int(size) or any(name in user["files"] for user in users.values()):
            return ""
        
        users[user_id]["files"][name] = int(size)
        users[user_id]["capacity"] -= int(size)
        
        return str(users[user_id]["capacity"])

    def update_capacity(users, user_id, new_capacity):
        if user_id not in users:
            return ""
        
        # Remove files if the new capacity is exceeded
        current_capacity = users[user_id]["capacity"]
        new_capacity = int(new_capacity)

        if current_capacity < new_capacity:
            files_to_remove = []
            remaining_capacity = new_capacity

            # Sort files lexicographically and by size
            sorted_files = sorted(users[user_id]["files"].items(), key=lambda x: (x[0], x[1]))

            for file, size in sorted_files:
                if remaining_capacity >= size:
                    remaining_capacity -= size
                else:
                    files_to_remove.append(file)
            
            # Remove files from user's storage
            for file in files_to_remove:
                current_capacity += users[user_id]["files"].pop(file)
                print(user_id, users[user_id]["files"])

            users[user_id]["capacity"] = current_capacity
            return str(len(files_to_remove))
        
        users[user_id]["capacity"] = new_capacity
        return ""

    #MAIN
    for query in queries:
        operation, *params = query
        if operation == "ADD_FILE":
            result.append(add_file(cloud_storage, *params))
        elif operation == "COPY_FILE":
            result.append(copy_file(users, *params))
        elif operation == "GET_FILE_SIZE":
            result.append(get_file_size(cloud_storage, *params))
        elif operation == "FIND_FILE":
            result.append(find_file(cloud_storage, *params))
        elif operation == "ADD_USER":
            result.append(add_user(users, *params))
        elif operation == "ADD_FILE_BY":
            result.append(add_file_by(users, *params))
        elif operation == "UPDATE_CAPACITY":
            result.append(update_capacity(users, *params))

    return result





queries = [["ADD_USER","owner","1000"], 
 ["ADD_FILE_BY","owner","/foo/bar/large_file","600"], 
 ["ADD_FILE_BY","owner","/foo/small_file","200"], 
 ["ADD_FILE_BY","owner","/foo/medium_file","400"], 
 ["UPDATE_CAPACITY","owner","1500"], 
 ["UPDATE_CAPACITY","owner","800"], 
 ["UPDATE_CAPACITY","owner","500"], 
 ["UPDATE_CAPACITY","owner","100"]]
ex = ["true", "400", "200", "", "0", "0", "1", "1"]
print(solution(queries))