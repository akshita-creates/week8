import azure.functions as func
import pyodbc
import json


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def get_database_connection():
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:akshita-admin.database.windows.net,1433;"
        "Database=week8-akshita;"
        "Uid=aksh-admin;"
        "Pwd=serverforme@1234;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(connection_string)


def check_credentials(username, password):

    query = """
        SELECT 1
        FROM [user]
        WHERE username = ? AND password = ?
    """

    with get_database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(query, (username, password))

        return cursor.fetchone() is not None


@app.route(route="login", methods=["GET", "POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:

    if req.method == "POST":

        try:
            credentials = req.get_json()

            username = credentials.get("username")
            password = credentials.get("password")

        except ValueError:

            return func.HttpResponse(
                json.dumps({
                    "error": "Invalid JSON"
                }),
                status_code=400,
                mimetype="application/json"
            )

    else:

        username = req.params.get("username")
        password = req.params.get("password")


    if not isinstance(username, str) or not isinstance(password, str):

        return func.HttpResponse(
            json.dumps({
                "error": "username and password are required"
            }),
            status_code=400,
            mimetype="application/json"
        )


    try:

        if not check_credentials(username, password):

            return func.HttpResponse(
                json.dumps({
                    "error": "invalid username or password"
                }),
                status_code=401,
                mimetype="application/json"
            )


        return func.HttpResponse(
            json.dumps({
                "message": "login successful"
            }),
            status_code=200,
            mimetype="application/json"
        )


    except Exception as e:

        return func.HttpResponse(
            json.dumps({
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
