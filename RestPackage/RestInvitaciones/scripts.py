# generic queries
get_query = "Select {keys} from {table} {cond};"
put_query = "insert into {table}({keys}) values({values});"
update_query = "Update {table} set {changes} where {cond};"
delete_query = "delete from {table} where {cond}"


def key_value_parser(dict):
    return ",".join(dict.keys()), ",".join(map(lambda x: "'" + x + "'" if type(x) is str else str(x), dict.values()))
