def solution(queries):
    in_memory_database = {}
    modification_count = {}

    def set_or_inc(key, field, value):
        if key not in in_memory_database:
            in_memory_database[key] = {field: int(value)}
        elif field not in in_memory_database[key]:
            in_memory_database[key][field] = int(value)
        else:
            in_memory_database[key][field] += int(value)

        # Update modification count
        modification_count[key] = modification_count.get(key, 0) + 1

        return str(in_memory_database[key][field])

    def get(key, field):
        if key in in_memory_database and field in in_memory_database[key]:
            return str(in_memory_database[key][field])
        else:
            return ""

    def delete(key, field):
        if key in in_memory_database and field in in_memory_database[key]:
            del in_memory_database[key][field]
            modification_count[key]+=1

            # If all fields in a record have been deleted, remove the record
            if not in_memory_database[key]:
                del in_memory_database[key]
                del modification_count[key]

            return "true"
        else:
            return "false"

    def top_n_keys(n):
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
    
    def set_or_inc_by_caller(key, field, value, caller_id):
        return set_or_inc(key, field, value, caller_id)

    def delete_by_caller(key, field, caller_id):
        return delete(key, field, caller_id)

    def lock(caller_id, key):
        if key not in in_memory_db:
            return "invalid_request"

        if key in lock_status:
            if lock_status[key] == caller_id:
                return ""

            if key not in lock_queue:
                lock_queue[key] = []

            lock_queue[key].append(caller_id)
            return "wait"

        lock_status[key] = caller_id
        return "acquired"

    def unlock(key):
        if key not in in_memory_db:
            return "invalid_request"

        if key in lock_status:
            del lock_status[key]

            if key in lock_queue:
                next_in_queue = lock_queue[key].pop(0) if lock_queue[key] else None

                if next_in_queue:
                    lock_status[key] = next_in_queue
                    return "released"

            return "released"

        return ""


    result = []

    for query in queries:
        operation, *params = query
        if operation == "SET_OR_INC":
            result.append(set_or_inc(*params))
        elif operation == "UNLOCK":
            result.append(unlock(*params))
        elif operation == "LOCK":
            result.append(lock(*params))
        elif operation == "SET_OR_INC_BY_CALLER":
            result.append(set_or_inc_by_caller(*params))
        elif operation == "DELETE_BY_CALLER":
            result.append(delete_by_caller(*params))
        elif operation == "GET":
            result.append(get(*params))

    return result


queries = [["SET_OR_INC","item1","cost","30"], 
 ["GET","item1","cost"], 
 ["DELETE","item1","cost"], 
 ["DELETE","item1","cost"], 
 ["GET","item1","cost"], 
 ["SET_OR_INC","item2","cost","50"], 
 ["SET_OR_INC","item3","cost","60"], 
 ["SET_OR_INC","item3","cost","4"], 
 ["GET","item2","cost"], 
 ["DELETE","item2","cost"], 
 ["GET","item3","cost"]]
solution(queries)
