import sqlite3
Asilbek = sqlite3.connect('db.sqlite3')

def bot_stat():
    odam = Asilbek.execute('''SELECT id FROM myfiles_til''')
    return odam.fetchall()


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

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            myfiles_til varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self,  tg_user: str, user_ismi: str,balans:str,til:str ):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_User(tg_user, user_ismi,balans,til) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(tg_user, user_ismi ,balans,til), commit=True)

    def ad_referal(self, user_id: str, referal_id=None, balance: str = "0"):
        sql = """
        INSERT INTO myfiles_referal(user_id, referal_id, balance)
        VALUES (?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, referal_id, balance), commit=True)

    def add_shablon(self,  tg_id: str, institut: str,ism_fam:str,saxifa_soni:str ,til:str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_shablon(tg_id, institut,ism_fam,saxifa_soni,til) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(tg_id, institut,ism_fam,saxifa_soni,til), commit=True)

    def add_shablon_kurs(self,  tg_id: str, institut: str,ism_fam:str,sahifa_soni:str ,til:str,kurs_tili:str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_shablon_kurs(tg_id, institut,ism_fam,sahifa_soni,til,kurs_tili) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(tg_id, institut,ism_fam,sahifa_soni,til,kurs_tili), commit=True)

    def add_shablon_pre(self,  tg_id: str, bg_num: str,ism_fam:str,til:str ,slayid_soni:str,pre_tili:str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_shablon_pre(tg_id, bg_num,ism_fam,slayid_soni,til,pre_tili) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(tg_id, bg_num,ism_fam,slayid_soni,til,pre_tili), commit=True)

    def add_admin(self,  tg_user: str, username: str,ismi:str ):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_Admin(tg_user, username,ismi) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=( tg_user, username,ismi), commit=True)


    def add_kanallar(self,  tg_user: str, username: str,ismi:str ):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_kanallar(tg_user, username,ismi) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=( tg_user, username,ismi), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM myfiles_User
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)



    def select_shablon(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_shablon WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_shablon_kurs(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_shablon_kurs WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
    def select_shablon_pre(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_shablon_pre WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def select_admin(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_Admin WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def select_kanallar(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_kanallar WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_admins(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_Admin WHERE TRUE"
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)


    def select_kanallars(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_kanallar WHERE TRUE"
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM myfiles_User;", fetchone=True)

    def count_group(self):
        return self.execute("SELECT COUNT(*) FROM myfiles_kanallar;", fetchone=True)


    def count_admin(self):
        return self.execute("SELECT COUNT(*) FROM myfiles_Admin;", fetchone=True)
    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_admin2(self):
        self.execute("DELETE FROM myfiles_Admin WHERE ", commit=True)

#-------------------------Languages---------------------------

    def create_table_lang(self):
        sql = """
        CREATE TABLE myfiles_til (
            id int NOT NULL,
            lang varchar(3),
            city varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_lang(self, id: int, lang: str = 'uz',city: str = 'NO'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_til(id, lang, city) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, lang, city), commit=True)
    def tugma_olish(self):
        sql = """
        SELECT * FROM myfiles_tugma
        """
        return self.execute(sql, fetchall=True)

    def tugma_olish_en(self):
        sql = """
        SELECT * FROM myfiles_tugma_en
        """
        return self.execute(sql, fetchall=True)

    def tugma_olish_ru(self):
        sql = """
        SELECT * FROM myfiles_tugma_ru
        """
        return self.execute(sql, fetchall=True)

    def delete_admin3(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "DELETE * FROM myfiles_ADMIN WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_User WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def delete_admin(self, id):
        # SQL_EXAMPLE = "UPDATE myfiles_teacher SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        DELETE FROM myfiles_Admin WHERE id=?
        """
        return self.execute(sql, parameters=( id), commit=True)

    def delete_kanallar(self, id):
        # SQL_EXAMPLE = "UPDATE myfiles_teacher SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        DELETE FROM myfiles_kanallar WHERE id=?
        """
        return self.execute(sql, parameters=( id), commit=True)



    def update_shaxar(self, city, id):
        # SQL_EXAMPLE = "UPDATE myfiles_teacher SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE myfiles_til SET city=? WHERE id=?
        """
        return self.execute(sql, parameters=(city, id), commit=True)





    def update_referat(self, balance, user_id):
        # SQL_EXAMPLE = "UPDATE myfiles_teacher SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE myfiles_referat SET balance=? WHERE user_id =?
        """
        return self.execute(sql, parameters=(balance, user_id), commit=True)


    def select_editlang(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = " SELECT * FROM myfiles_til WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def update_user_lang(self, lang, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE myfiles_til SET lang=? WHERE id=?
        """
        return self.execute(sql, parameters=(lang, id), commit=True)

    def update_shablon_lang(self, til, tg_id, pre_tili):

        try:
            sql = """
            UPDATE myfiles_shablon_pre
            SET til=? 
            WHERE tg_id=? AND pre_tili=?
            """
            return self.execute(sql, parameters=(til, tg_id, kurs_tili), commit=True)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            return False
    
    def update_shablon_lang_kurs(self, til, tg_id, kurs_tili):

        try:
            sql = """
            UPDATE myfiles_shablon_kurs
            SET kurs_tili=? 
            WHERE tg_id=? AND til=?
            """
            return self.execute(sql, parameters=(til, tg_id, kurs_tili), commit=True)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            return False
    
    
    
    def update_user_lang2(self, til, tg_user):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE myfiles_User SET til=? WHERE tg_user=?
        """
        return self.execute(sql, parameters=(til, tg_user), commit=True)

    def update_user_balans(self, balans,tg_user):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE myfiles_User SET balans=? WHERE tg_user=?
        """
        return self.execute(sql, parameters=(balans,tg_user), commit=True)

    def update_user_city(self, city, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE myfiles_til SET city=? WHERE id=?
        """
        return self.execute(sql, parameters=(city, id), commit=True)


    def select_summa(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = " SELECT * FROM myfiles_summa WHERE TRUE"
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def add_summa_kurs(self, summa: str,sahifa: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_summa_kurs(summa, sahifa) VALUES( ?, ?)
        """
        self.execute(sql, parameters=(sahifa, summa), commit=True)


    def select_summa_kurs(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = " SELECT * FROM myfiles_summa_kurs WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def select_one_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = " SELECT * FROM myfiles_User WHERE TRUE"
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)



    def select_editcity(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = " SELECT * FROM myfiles_til WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_lang(self):
        sql = """
        SELECT * FROM myfiles_til
        """
        return self.execute(sql, fetchall=True)
    def select_all_foidalanuvchilar(self):
        sql="""
        SELECT * FROM myfiles_til
        """
        return self.execute(sql, fetchall=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")