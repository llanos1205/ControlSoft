import bd
def handler(event,context):
    responde=bd.Creater()
    return {
        "statusCode":200,
        "body":responde
    }