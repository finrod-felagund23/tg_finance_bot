from config import DB_NAME, HOST, PORT, PASSWORD
import psycopg2

connection = psycopg2.connect(host=HOST, port=PORT, db_name=DB_NAME, password=PASSWORD)
cursor = connection.cursor()


def create_user_table(username): pass