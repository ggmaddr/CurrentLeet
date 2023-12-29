def solution(queries):
    in_memory_db = {}
    modification_count = {}
    lock_queue = {}
    lock_status = {}
    def set_or_inc(key, field, value):
        #debug
        if get_key_locked_status(key):
            print("setorinc ignored", key)
        if not get_key_locked_status(key):
            if key not in in_memory_db:
                in_memory_db[key] = {field: int(value)}
            elif field not in in_memory_db[key]:
                in_memory_db[key][field] = int(value)
            else:
                in_memory_db[key][field] += int(value)

            # Update modification count
            modification_count[key] = modification_count.get(key, 0) + 1

        return str(in_memory_db[key][field])

    def get(key, field):
        if key in in_memory_db and field in in_memory_db[key]:
            return str(in_memory_db[key][field])
        else:
            return ""

    def delete(key, field):
        if key in in_memory_db and field in in_memory_db[key] and not get_key_locked_status(key):
            del in_memory_db[key][field]
            modification_count[key]+=1

            # If all fields in a record have been deleted, remove the record
            if not in_memory_db[key]:
                del in_memory_db[key]
                del modification_count[key]

            return "true"
        else:
            return "false"

    def top_n_keys(n):
        n = int(n)
        sorted_keys = sorted(
            modification_count.keys(),
            #if tie, sort by k (key names)lexicographical 
            key=lambda k: (-modification_count[k], k),
            reverse=False,
        )

        result = []

        for key in sorted_keys[:n]:
            result.append(f"{key}({modification_count[key]})")

        return ", ".join(result)
    def get_key_locked_status(key) -> bool:
        return key in lock_status
    def set_or_inc_by_caller(key, field, value, caller_id):
        if key not in in_memory_db or not get_key_locked_status(key) or lock_status[key]["user"] == caller_id:
            if key in lock_status:
                if lock_status[key]["user"] == caller_id:
                    print(key, field, value, caller_id)
            return set_or_inc(key, field, value)
        else:
            return str(in_memory_db[key].get(field, ""))if field in in_memory_db[key] else ""

    def delete_by_caller(key, field, caller_id):
        if key in in_memory_db and (not get_key_locked_status(key) or lock_status[key]["user"] == caller_id):
            return delete(key, field)
        else:
            return "false"

    def lock(caller_id, key):
        if key not in in_memory_db:
            return "invalid_request"
        #  if the record is already locked by another user
        if get_key_locked_status(key):
            if lock_status[key]["user"] == caller_id or caller_id in lock_queue[key]:
                return ""
            elif caller_id not in lock_queue[key]:
                lock_queue[key].append(caller_id)
                return "wait"
            else:
                return ""
        else:
            lock_queue[key] = []
            lock_status[key] = {"user": caller_id, "queue": lock_queue[key]}
            return "acquired"

    def unlock(key):
        if key in lock_status:
            released_user = lock_status[key]["user"]
            lock_queue[key] = lock_status[key]["queue"]
            del lock_status[key]
            return "released" if released_user else ""
        else:
            return "invalid_request"


    result = []

    for query in queries:
        operation, *params = query
        if operation == "SET_OR_INC":
            result.append(set_or_inc(*params))
        elif operation == "UNLOCK":
            result.append(unlock(*params))
        elif operation == "LOCK":
            result.append(lock(*params))
        elif operation == "DELETE":
            result.append(delete(*params))
        elif operation == "TOP_N_KEYS":
            result.append(top_n_keys(*params))
        elif operation == "SET_OR_INC_BY_CALLER":
            result.append(set_or_inc_by_caller(*params))
        elif operation == "DELETE_BY_CALLER":
            result.append(delete_by_caller(*params))
        elif operation == "GET":
            result.append(get(*params))

    return result


# # Example Usage
# queries = [
#     ["SET_OR_INC", "C", "field1", "10"],
#     ["TOP_N_KEYS", "5"],
#     ["SET_OR_INC", "A", "
