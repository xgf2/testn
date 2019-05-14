import psycopg2
import settings

def get_row_on_column(table_name, column_name, value):
    
    command = 'SELECT ' + column_name + ' FROM ' + table_name + ' WHERE ' + column_name + ' = %s' 
    result = action_over_table(command, [(value,)])
    return result

def add_rows(table_name, list_data):

    if table_name == 'list_news':

        command = 'INSERT INTO ' + table_name + ' (href, title, image_src, date_news) ' + 'VALUES (%(href)s, %(title)s, %(image_src)s, %(date_news)s);'
        action_over_table(command, list_data)

    elif table_name == 'news':

        command = 'INSERT INTO ' + table_name + ' (href, title_news, image_src_news, text_news, datetime_news) ' + 'VALUES (%(href)s, %(title_news)s, %(image_src_news)s, %(text_news)s, %(datetime_news)s);'
        action_over_table(command, list_data)


def create_tables():

    commands = ['CREATE TABLE list_news (id serial PRIMARY KEY, href varchar, title varchar, image_src varchar, date_news timestamptz);',
    'CREATE TABLE news (id serial PRIMARY KEY, href varchar, title_news varchar, image_src_news varchar, text_news varchar, datetime_news timestamptz);']

    action_over_table(commands)

def drop_tables():

    commands = ['DROP TABLE list_news;',
    'DROP TABLE news;']

    action_over_table(commands)

def action_over_table(commands, list_values = None):

    connect = None
    result = None

    try:
        connect = psycopg2.connect('dbname = %s user = %s password = %s' % (settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD))
        cursor = connect.cursor()

        if type(commands) == str and list_values:
            for values in list_values:
                try:
                    cursor.execute(commands, values)
                    if commands.find('INSERT'):
                        result = cursor.fetchall()
                except psycopg2.Error as e:
                    print('Error psycopg2: %s' % e)
                except psycopg2.ProgrammingError as e:
                    print('ProgrammingError: %s' % e)

        elif type(commands) == list:
            for command in commands:
                try:
                    cursor.execute(command)
                except psycopg2.Error as e:
                    print('Error psycopg2: %s' % e)

        connect.commit()

    except psycopg2.DatabaseError as e:
        if connect:
            connect.rollback()
        print('Error psycopg2 %s' % e)

    finally:
        if connect:
            connect.close()

        return result

if  __name__ == '__main__':
    pass
    drop_tables()
    create_tables()
