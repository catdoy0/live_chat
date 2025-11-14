from typing import Optional
import mariadb

class DatabasePool:

    pool: Optional[mariadb.ConnectionPool] = None

    conn_string = {
        "user" : "root",
        "password" : "",
        "host" : "127.0.0.1",
        "port" : 3306,
        "database" : "Live_Chat_Database"
    }

    @staticmethod
    def init_poot():
        DatabasePool.pool = mariadb.ConnectionPool(
            pool_name = "mypool",
            **DatabasePool.conn_string
        )

    @staticmethod
    def get_connection():
        if DatabasePool.pool is None:
            raise RuntimeError("Connection Pool not initialized.")
        return DatabasePool.pool.get_connection()


class InitializeDatabase:

    @staticmethod
    def CreateDatabase() -> bool:
        try:
            with mariadb.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3306,
            ) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                CREATE DATABASE IF NOT EXISTS Live_Chat_Database
                               """)
                conn.commit()
                return True

        except mariadb.Error as err:
            print(err)
            return False

    @staticmethod
    def CreateTables() -> bool:
        try:
            with mariadb.connect(**DatabasePool.conn_string) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Accounts (
                    ID INT PRIMARY KEY AUTO_INCREMENT,
                    USERNAME varchar(255) NOT NULL UNIQUE,
                    EMAIL varchar(255) NOT NULL UNIQUE,
                    HASHED_PASS varchar(255),
                    SESSION_VALUE varchar(255)
                    )
                               """)

                return True
        except mariadb.Error as err:
            print(err)
            return False


