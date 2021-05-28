import pymysql
import os
from dotenv import load_dotenv
import pandas as pd


class MySQL_command:
    """
      MySQL 데이터베이스에 접속하여 조작할 수 있게 하는 클래스.
      메서드를 이용해 sql 쿼리문을 실행한다.
    """

    def __init__(self) -> None:
        load_dotenv(dotenv_path="account_information.env", verbose=True)
        mysqlPassword = os.getenv("mysqlPassword")
        self.db_connector = pymysql.connect(
            user="root", passwd=f"{mysqlPassword}", host="127.0.0.1", db="algorithm_trading", charset="utf8"
        )
        self.cursor = self.db_connector.cursor(pymysql.cursors.DictCursor)

    def query(self, sql: str, arguments: list = []):
        """조회 전용 메서드"""
        arguments = tuple(arguments)
        try:
            self.cursor.execute(sql, arguments)
            result = self.cursor.fetchall()
            return pd.DataFrame(result)
        except Exception as e:
            print(e)
            raise

    def mutation(self, sql: str, arguments: list = []):
        """삽입, 수정, 삭제 메서드"""
        arguments = tuple(arguments)
        try:
            self.cursor.execute(sql, arguments)
            self.db_connector.commit()
        except Exception as e:
            print(e)
            raise

