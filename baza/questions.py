import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def question_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Questions(
        test_name TEXT,
        number_question INTEGER,
        question TEXT,
        A TEXT,
        B TEXT,
        C TEXT,
        D TEXT,
        answer TEXT
        );
              """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())
    
    def add_questions(self, test_name, number_question, question, a, b, c, d, answer):
        sql = """
        INSERT INTO Questions(test_name, number_question, question, A, B, C, D, answer) VALUES(?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.execute(sql, parameters=(test_name, number_question, question, a, b, c, d, answer), commit=True)

    def question_names(self):
        sql = """SELECT test_name FROM Questions;"""
        return self.execute(sql, fetchall=True)
    
    def get_questions(self, test_name):
        sql = """SELECT * FROM Questions WHERE test_name = ?;"""
        return self.execute(sql, parameters=(test_name,), fetchall=True)
        
    def test_number(self, test_name):
        sql = """SELECT number_question FROM Questions WHERE test_name = ?;"""
        return self.execute(sql, parameters=(test_name,), fetchall=True)

    def delete_questions(self, test_name):
        sql = """
        DELETE FROM Questions WHERE test_name = ?;
        """
        return self.execute(sql, parameters=(test_name,), commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")