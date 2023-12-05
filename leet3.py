def solution(queries):
    accounts = {}
    transfers = {}
    transfer_counter = 0
    MILLISECONDS_IN_1_DAY = 86400000


    def create_account(timestamp, account_id):
        if account_id not in accounts:
            accounts[account_id] = {"balance": 0, "transactions": [], "transfers": {}}
            return "true"
        else:
            return "false"

    def deposit(timestamp, account_id, amount):
        if account_id in accounts:
            amount = int(amount)
            
            # if accounts[account_id]: 
            #     if accounts[account_id]["balance"]:
            #         print( accounts[account_id]["balance"] )

            accounts[account_id]["balance"] += amount
            accounts[account_id]["transactions"].append({"type": "DEPOSIT", "amount": amount, "timestamp": int(timestamp)})
            
            
            return str(accounts[account_id]["balance"])
        else:
            return ""

    def pay(timestamp, account_id, amount):
        if account_id in accounts:
            amount = int(amount)
            if accounts[account_id]["balance"] >= amount:
                accounts[account_id]["balance"] -= amount
                accounts[account_id]["transactions"].append({"type": "PAY", "amount": amount, "timestamp": int(timestamp)})
                return str(accounts[account_id]["balance"])
            else:
                return ""
        else:
            return ""
    
    def top_activity(timestamp, n):
            sorted_accounts = sorted(accounts.items(), key=lambda x: (-sum(t['amount'] for t in x[1]['transactions']), x[0]), reverse=False)
            
            top_n_accounts = sorted_accounts[:n]
            result = ", ".join(f"{account_id}({sum(t['amount'] for t in account_data['transactions'])})" for account_id, account_data in top_n_accounts)
            return result

    def transfer(timestamp, source_account_id, target_account_id, amount):
        nonlocal transfer_counter
        if source_account_id == target_account_id or source_account_id not in accounts or target_account_id not in accounts:
            return ""

        amount = int(amount)
        if accounts[source_account_id]["balance"] < amount:
            return ""

        transfer_id = f"transfer{transfer_counter + 1}"
        transfer_counter += 1

        transfers[transfer_id] = {
            "source_account": source_account_id,
            "target_account": target_account_id,
            "amount": amount,
            "timestamp": int(timestamp),
            "accepted": False
        }

        accounts[source_account_id]["balance"] -= amount
        accounts[source_account_id]["transfers"][transfer_id] = {"type": "TRANSFER_OUT", "amount": amount, "timestamp": int(timestamp)}

        accounts[target_account_id]["transfers"][transfer_id] = {"type": "TRANSFER_IN", "amount": amount, "timestamp": int(timestamp)}

        return transfer_id
    
    def accept_transfer(timestamp, account_id, transfer_id):
      
        if (transfer_id not in transfers 
        or transfers[transfer_id]["accepted"] 
        #expired
        or int(timestamp) > transfers[transfer_id]["timestamp"] + MILLISECONDS_IN_1_DAY  
        
        or account_id != transfers[transfer_id]["target_account"]):
            if transfer_id in transfers:
                if int(timestamp) > transfers[transfer_id]["timestamp"] + MILLISECONDS_IN_1_DAY:
                    
                    source_account_id = transfers[transfer_id]["source_account"]
                    amount = transfers[transfer_id]["amount"]
                    accounts[source_account_id]["balance"] += amount

            
            return "false"
        else:
            source_account_id = transfers[transfer_id]["source_account"]
            
            
            
            
            amount = transfers[transfer_id]["amount"]

            transfers[transfer_id]["accepted"] = True
            
            accounts[account_id]["balance"] += amount
            
            accounts[account_id]["transactions"].append({"type": "TRANSFER_IN", "amount": amount, "timestamp": int(timestamp)})
            #? not sure + or - for out amount
            accounts[source_account_id]["transactions"].append({"type": "TRANSFER_OUT", "amount": amount, "timestamp": int(timestamp)})

            return "true"
    
    
    #MAIN
    output = []
    
    for query in queries:
        operation, timestamp, account_id, *args = query
        if operation == "CREATE_ACCOUNT":
            output.append(create_account(timestamp, account_id))
        elif operation == "DEPOSIT":
            output.append(deposit(timestamp, account_id, *args))
        elif operation == "PAY":
            output.append(pay(timestamp, account_id, *args))
        elif operation == "TOP_ACTIVITY":
            output.append(top_activity(timestamp, int(account_id)))
        elif operation == "TRANSFER":
            output.append(transfer(timestamp, account_id, *args))
        elif operation == "ACCEPT_TRANSFER":
            output.append(accept_transfer(timestamp, account_id, *args))
    return output


queries = [
      [
        "CREATE_ACCOUNT",
        "1",
        "acc0"
      ],
      [
        "CREATE_ACCOUNT",
        "2",
        "acc1"
      ],
      [
        "CREATE_ACCOUNT",
        "3",
        "acc2"
      ],
      [
        "CREATE_ACCOUNT",
        "4",
        "acc3"
      ],
      [
        "CREATE_ACCOUNT",
        "5",
        "acc4"
      ],
      [
        "CREATE_ACCOUNT",
        "6",
        "acc5"
      ],
      [
        "CREATE_ACCOUNT",
        "7",
        "acc6"
      ],
      [
        "CREATE_ACCOUNT",
        "8",
        "acc7"
      ],
      [
        "CREATE_ACCOUNT",
        "9",
        "acc8"
      ],
      [
        "CREATE_ACCOUNT",
        "10",
        "acc9"
      ],
      [
        "DEPOSIT",
        "11",
        "acc0",
        "7757"
      ],
      [
        "DEPOSIT",
        "12",
        "acc1",
        "8114"
      ],
      [
        "DEPOSIT",
        "13",
        "acc2",
        "6692"
      ],
      [
        "DEPOSIT",
        "14",
        "acc3",
        "5429"
      ],
      [
        "DEPOSIT",
        "15",
        "acc4",
        "7852"
      ],
      [
        "DEPOSIT",
        "16",
        "acc5",
        "6105"
      ],
      [
        "DEPOSIT",
        "17",
        "acc6",
        "5747"
      ],
      [
        "DEPOSIT",
        "18",
        "acc7",
        "8009"
      ],
      [
        "DEPOSIT",
        "19",
        "acc8",
        "5165"
      ],
      [
        "DEPOSIT",
        "20",
        "acc9",
        "5966"
      ],
      [
        "PAY",
        "21",
        "acc0",
        "344"
      ],
      [
        "PAY",
        "22",
        "acc1",
        "222"
      ],
      [
        "PAY",
        "23",
        "acc2",
        "377"
      ],
      [
        "PAY",
        "24",
        "acc3",
        "172"
      ],
      [
        "PAY",
        "25",
        "acc4",
        "251"
      ],
      [
        "PAY",
        "26",
        "acc5",
        "497"
      ],
      [
        "PAY",
        "27",
        "acc6",
        "472"
      ],
      [
        "PAY",
        "28",
        "acc7",
        "103"
      ],
      [
        "PAY",
        "29",
        "acc8",
        "171"
      ],
      [
        "PAY",
        "30",
        "acc9",
        "448"
      ],
      [
        "TRANSFER",
        "31",
        "acc6",
        "acc0",
        "1358"
      ],
      [
        "TRANSFER",
        "32",
        "acc0",
        "acc1",
        "1150"
      ],
      [
        "TRANSFER",
        "33",
        "acc3",
        "acc2",
        "1235"
      ],
      [
        "TRANSFER",
        "34",
        "acc0",
        "acc3",
        "1539"
      ],
      [
        "TRANSFER",
        "35",
        "acc2",
        "acc4",
        "1253"
      ],
      [
        "TRANSFER",
        "36",
        "acc2",
        "acc5",
        "1397"
      ],
      [
        "TRANSFER",
        "37",
        "acc5",
        "acc6",
        "1861"
      ],
      [
        "TRANSFER",
        "38",
        "acc2",
        "acc7",
        "1518"
      ],
      [
        "TRANSFER",
        "39",
        "acc3",
        "acc8",
        "1635"
      ],
      [
        "TRANSFER",
        "40",
        "acc1",
        "acc9",
        "1669"
      ],
      [
        "TOP_ACTIVITY",
        "41",
        "10"
      ],
      [
        "DEPOSIT",
        "86400041",
        "acc0",
        "506"
      ],
      [
        "DEPOSIT",
        "86400042",
        "acc1",
        "276"
      ],
      [
        "DEPOSIT",
        "86400043",
        "acc2",
        "361"
      ],
      [
        "DEPOSIT",
        "86400044",
        "acc3",
        "757"
      ],
      [
        "DEPOSIT",
        "86400045",
        "acc4",
        "129"
      ],
      [
        "DEPOSIT",
        "86400046",
        "acc5",
        "477"
      ],
      [
        "DEPOSIT",
        "86400047",
        "acc6",
        "676"
      ],
      [
        "DEPOSIT",
        "86400048",
        "acc7",
        "754"
      ],
      [
        "DEPOSIT",
        "86400049",
        "acc8",
        "873"
      ],
      [
        "DEPOSIT",
        "86400050",
        "acc9",
        "242"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400051",
        "acc0",
        "transfer1"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400052",
        "acc1",
        "transfer2"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400053",
        "acc2",
        "transfer3"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400054",
        "acc3",
        "transfer4"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400055",
        "acc4",
        "transfer5"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400056",
        "acc5",
        "transfer6"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400057",
        "acc6",
        "transfer7"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400058",
        "acc7",
        "transfer8"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400059",
        "acc8",
        "transfer9"
      ],
      [
        "ACCEPT_TRANSFER",
        "86400060",
        "acc9",
        "transfer10"
      ],
      [
        "TOP_ACTIVITY",
        "86400061",
        "10"
      ],
      [
        "PAY",
        "86400062",
        "acc0",
        "348"
      ],
      [
        "PAY",
        "86400063",
        "acc1",
        "166"
      ],
      [
        "PAY",
        "86400064",
        "acc2",
        "281"
      ],
      [
        "PAY",
        "86400065",
        "acc3",
        "267"
      ],
      [
        "PAY",
        "86400066",
        "acc4",
        "421"
      ],
      [
        "PAY",
        "86400067",
        "acc5",
        "387"
      ],
      [
        "PAY",
        "86400068",
        "acc6",
        "172"
      ],
      [
        "PAY",
        "86400069",
        "acc7",
        "427"
      ],
      [
        "PAY",
        "86400070",
        "acc8",
        "481"
      ],
      [
        "PAY",
        "86400071",
        "acc9",
        "459"
      ],
      [
        "TRANSFER",
        "86400073",
        "acc9",
        "acc0",
        "1938"
      ],
      [
        "TRANSFER",
        "86400074",
        "acc3",
        "acc1",
        "1764"
      ],
      [
        "TRANSFER",
        "86400075",
        "acc7",
        "acc2",
        "1660"
      ],
      [
        "TRANSFER",
        "86400076",
        "acc4",
        "acc3",
        "1541"
      ],
      [
        "TRANSFER",
        "86400077",
        "acc8",
        "acc4",
        "1379"
      ],
      [
        "TRANSFER",
        "86400078",
        "acc2",
        "acc5",
        "1219"
      ],
      [
        "TRANSFER",
        "86400079",
        "acc5",
        "acc6",
        "1519"
      ],
      [
        "TRANSFER",
        "86400080",
        "acc2",
        "acc7",
        "1832"
      ],
      [
        "TRANSFER",
        "86400081",
        "acc6",
        "acc8",
        "1645"
      ],
      [
        "TRANSFER",
        "86400082",
        "acc2",
        "acc9",
        "1960"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800083",
        "acc0",
        "transfer11"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800084",
        "acc1",
        "transfer12"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800085",
        "acc2",
        "transfer13"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800086",
        "acc3",
        "transfer14"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800087",
        "acc4",
        "transfer15"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800088",
        "acc5",
        "transfer16"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800089",
        "acc6",
        "transfer17"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800090",
        "acc7",
        "transfer18"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800091",
        "acc8",
        "transfer19"
      ],
      [
        "ACCEPT_TRANSFER",
        "172800092",
        "acc9",
        "transfer20"
      ],
      [
        "TOP_ACTIVITY",
        "172800094",
        "10"
      ]
    ]

print(solution(queries))