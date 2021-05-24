import mysql.connector
connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )


def fields(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results
