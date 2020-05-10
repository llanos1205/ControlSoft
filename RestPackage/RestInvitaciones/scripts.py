# generic queries
get_query = "select {keys} from {table} {cond};"
put_query = "insert into {table}({keys}) values({values});"
update_query = "update {table} set {changes} where {cond};"
delete_query = "delete from {table} where {cond}"


def key_value_parser(dict):
    return ",".join(dict.keys()), ",".join(map(lambda x: "'" + x + "'" if type(x) is str else str(x), dict.values()))
def key_value_comparer_parser(dict):
    return ",".join(map(lambda x: (x+"='"+dict[x]+"'") if type(dict[x]) is str else (x+"="+str(dict[x])), dict.keys()))