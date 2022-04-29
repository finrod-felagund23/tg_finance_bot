from config import DB_NAME, HOST, PORT, PASSWORD, USER
from psycopg2.extensions import cursor, connection
import psycopg2
from aiogram import types
import re

my_conn = psycopg2.connect(host = HOST, port = PORT, database = DB_NAME, password = PASSWORD, user = USER)
my_cur = my_conn.cursor()


async def create_user_table(username: str = '', cur: cursor = my_cur, conn: connection = my_conn) -> str:
    """
    Создание таблицы юзера и его категорий. Внесение в категории дефолтных алиасов и категорий.
    :param username: Уникальный юзернейм пользователя телеграм
    :param cur:
    :param conn:
    :return: статус завершения
    """
    ret = 'not exists'
    cur.execute(f""" SELECT EXISTS(SELECT * FROM information_schema.columns WHERE TABLE_NAME='{username.lower()}')""")
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


async def add_expense(msg: types.Message, cur: cursor = my_cur, conn: connection = my_conn) -> str:
    """
    Парсинг сообщения, определение его категории по алиасу, добавление в базу данных.
    :param cur:
    :param conn:
    :param msg: Обычный message: types.Message
    :return: Полное сообщение пользователю о добавлении расхода или ошибке с ним
    """

    # первым словом должно идти число где есть 1 или больше чисел, вторым, слово вообще любое
    match = re.match(r'\d+ .*$', msg.text)
    cost, alias, *surplus = tuple(match.group().split())
    print(f'surplus=={surplus}')

    category = 'Прочее'
    for name, aliases in cur.fetchall():
        if alias in aliases:
            category = name[:]
            break

    cur.execute(f"""
    INSERT INTO {msg.from_user.username.lower()} ( cost_name, cost, category )
        VALUES ( %s, %s, %s )""", [str(alias), float(cost), str(category)])

    cur.execute(f"""SELECT * FROM {msg.from_user.username.lower()}""")
    # await msg.reply('Тест успешен!')
    print(cur.fetchall())
    conn.commit()

    return f'Расход {alias} был добавлен в категорию {category}'
