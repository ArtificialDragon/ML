import numpy as np
import mysql.connector
from mysql.connector import Error
from revenue_from_ECkr import CreditModel

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your_database',
            user='your_username',
            password='your_password'
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def insert_results(connection, B, params):
    try:
        cursor = connection.cursor()
        query = """INSERT INTO results (B, B0, Bpr, x, Ckr, gamma, alpha, t, t_pi, C_ps)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (B, params['B0'], params['Bpr'], params['x'], params['Ckr'],
                               params['gamma'], params['alpha'], params['t'], 
                               str(params['t_pi']), str(params['C_ps'])))
        connection.commit()
        print("Record inserted successfully into results table")
    except Error as e:
        print("Failed to insert record into MySQL table", e)

def main():
    # Параметры модели
    B0 = 100
    Bpr = 150
    x = 0.5
    gamma = 0.1
    alpha = 0.3
    t = 30
    Ckr = 50000
    t_pi = [10, 20, 30, 40, 50]
    C_ps = [1000, 2000, 3000, 4000, 5000]
    K_t = 5

    # Создание экземпляра модели
    credit_model = CreditModel(B0, Bpr, x, Ckr, gamma, alpha)
    
    # Установка параметров
    credit_model.set_t(t)
    credit_model.set_periods_and_payments(t_pi, C_ps)
    credit_model.set_K_t(K_t)
    
    # Вычисление значения выручки
    B = credit_model.calculate_B()
    print("B(Ckr, t) =", B)
    
    # Подключение к базе данных и запись результатов
    connection = connect_to_db()
    if connection:
        params = {
            'B0': B0,
            'Bpr': Bpr,
            'x': x,
            'Ckr': Ckr,
            'gamma': gamma,
            'alpha': alpha,
            't': t,
            't_pi': t_pi,
            'C_ps': C_ps
        }
        insert_results(connection, B, params)
        connection.close()

if __name__ == "__main__":
    main()
