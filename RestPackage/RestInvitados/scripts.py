# generic queries
getQuery = "select {keys} from {table} {cond};"
putQuery = "insert into {table}({keys}) values({values});"
updateQuery = "update {table} set {changes} where {cond};"
deleteQuery = "delete from {table} where {cond}"


def keyValueParser(obj):
    values = ",".join(map(lambda x: "'" + x + "'" if type(x) is str else str(x), obj.values()))
    keys = ",".join(map(lambda x: "\"" + x + "\"", obj.keys()))
    return keys, values


def keyValueComparerParser(obj):
    return ",".join(
        map(lambda x: ("\"" + x + "\"='" + obj[x] + "'") if type(obj[x]) is str else (
                    "\"" + x + "\"=" + str(obj[x])), obj.keys()))
