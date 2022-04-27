from config import DB_NAME, HOST, PORT, PASSWORD, USER
from psycopg2.extensions import cursor, connection
import psycopg2


my_conn = psycopg2.connect(host = HOST, port = PORT, database = DB_NAME, password = PASSWORD, user = USER)
my_cur = my_conn.cursor()


async def create_user_table(username: str = '', cur: cursor = my_cur, conn: connection = my_conn) -> str:
    ret = 'not exists'
    print(cur)
    print(conn)
    print(username)

    cur.execute(f""" SELECT EXISTS(SELECT * FROM information_schema.columns WHERE TABLE_NAME='{username.lower()}')""")
    # print(cur.fetchone())
    if cur.fetchone()[0]:
        ret = 'exists'
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {username}
    (
        cost_name  varchar(100) NOT NULL,
        cost       float(1)     NOT NULL,
        category   varchar(40)  NOT NULL,
        id         serial       NOT NULL,
        PRIMARY KEY ( id )
    )
    """)

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS categories_{username}
    ( 
        name    varchar( 40 )   NOT NULL,
        aliases text[]          NOT NULL
    )
    """)
    if ret == 'not exists':
        variables = (
            ('Продукты', ['products', 'product', 'продукты', 'овощи']),
            ('Проезд', ['проезд', 'такси', 'автобус', 'taxi', 'bus', 'transport']),
            ('Рофланы', ['сладости', 'rofls', 'cake', 'candies', 'конфеты']),
            ('Прочее', ['*'])
        )
        # cur.executemany(f"""
        # INSERT INTO categories_{username} ( name, aliases )
        #     VALUES ( %s, %s )""", variables)

        for x in variables:
            cur.execute(f"""
            INSERT INTO categories_{username}
                VALUES ( %s, %s )""", x)


    conn.commit()
    return ret
