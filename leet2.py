def solution(queries):
    cloud_storage = {}
    result = []
    users = {}

    users["admin"]={"capacity": float("inf"), "files": cloud_storage}

    def add_file(cloud_storage, name, size):
        if name in cloud_storage:
            return "false"
        cloud_storage[name] = int(size)
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
        for user_id, user in users.items():
            file_size = user["files"].get(name)
            if file_size:
                if user_id == "admin":
                    return str(cloud_storage.get(name, {}))
                else:
                    return str(file_size)
        return ""
    
    def find_file(prefix, suffix):
        matching_files = []

        for user_id, user in users.items():
            for name, file_info in user["files"].items():
                if name.startswith(prefix) and name.endswith(suffix):
                    matching_files.append((name, file_info))

        if not matching_files:
            return ""

        # Sort files in descending order of size, and lexicographically in case of ties
        sorted_files = sorted(matching_files, key=lambda x: (-x[1], x[0]), reverse=False)
        

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
            
            total_size = sum(users[user_id]["files"].values())

            if total_size > new_capacity:
                files_to_remove = 0
                remaining_capacity = new_capacity
                files_list = list(users[user_id]["files"].items())

                # Sort files lexicographically and by size
                sorted_files = sorted(users[user_id]["files"].items(), key=lambda x: (-x[1], x[0]), reverse=False)
                sorted_files.reverse()
                print("sorted files",sorted_files)
                while total_size > new_capacity:
                    popfile = sorted_files.pop()
                    removedfile = users[user_id]["files"].pop(popfile[0])
                    # print("ATTENTION 888",removedfile,users[user_id]["files"])

                    total_size -= removedfile
                    files_to_remove+=1
                    # print("removed file", popfile, removedfile)
                    # current_capacity += removedfile
                    # print("removing file",user_id, users[user_id]["files"], current_capacity)
                    
                # for file, size in sorted_files:
                #     if remaining_capacity >= size:
                #         remaining_capacity -= size
                #     else:
                #         print("FILES TO REMOVE", file, size)
                #         files_to_remove.append(file )

                # Remove files from user's storage
                
                # for file in files_to_remove:
                #     removedfile = users[user_id]["files"].pop(file)
                #     print("removed file", removedfile)
                #     current_capacity += removedfile
                #     print("removing file",user_id, users[user_id]["files"], current_capacity)
                
                users[user_id]["capacity"] = new_capacity - total_size
                return str(files_to_remove)
            
            users[user_id]["capacity"] = new_capacity - total_size
            return "0"
    def compress_file(users, user_id, name):
        if not name.endswith(".COMPRESSED") and name in users[user_id]["files"]:
            original_size = users[user_id]["files"][name]
            compressed_size = original_size // 2

            if users[user_id]["capacity"] >= compressed_size:
                compressed_name = name + ".COMPRESSED"
                users[user_id]["files"][compressed_name] = compressed_size
                users[user_id]["capacity"] += compressed_size
                del users[user_id]["files"][name]
                return str(users[user_id]["capacity"])

        return ""

    def decompress_file(users, user_id, name):
        if name.endswith(".COMPRESSED") and name in users[user_id]["files"]:
            decompressed_name = name.replace(".COMPRESSED", "")
            decompressed_size = users[user_id]["files"][name] * 2
            if decompressed_name not in users[user_id]["files"] and users[user_id]["capacity"] >= decompressed_size:
                users[user_id]["files"][decompressed_name] = decompressed_size
                users[user_id]["capacity"] -= decompressed_size
                #FIX HERE, delete the file[name] in users[user_id]["files"]

                return str(users[user_id]["capacity"])
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
            result.append(find_file(*params))
        elif operation == "ADD_USER":
            result.append(add_user(users, *params))
        elif operation == "ADD_FILE_BY":
            result.append(add_file_by(users, *params))
        elif operation == "UPDATE_CAPACITY":
            result.append(update_capacity(users, *params))
        elif operation == "COMPRESS_FILE":
            result.append(compress_file(users, *params))
        elif operation == "DECOMPRESS_FILE":
            result.append(decompress_file(users, *params))
    return result




# queries = [["ADD_USER","owner","1000"], 
#  ["ADD_FILE_BY","owner","/foo/bar/large_file","600"], 
#  ["ADD_FILE_BY","owner","/foo/small_file","200"], 
#  ["ADD_FILE_BY","owner","/foo/medium_file","400"], 
#  ["UPDATE_CAPACITY","owner","1500"], 
#  ["UPDATE_CAPACITY","owner","800"], 
#  ["UPDATE_CAPACITY","owner","500"], 
#  ["UPDATE_CAPACITY","owner","100"]]
# ex = ["true", "400", "200", "", "0", "0", "1", "1"]
# print(solution(queries))