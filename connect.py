import pyodbc

# 定义连接字符串
server = 'tcp:face-vote-fyp.database.windows.net,1433'
database = 'fyp'
username = 'ming'
password = '{P@ssw0rd}'
driver = '{ODBC Driver 17 for SQL Server}'
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

try:
    # 建立数据库连接
    conn = pyodbc.connect(conn_str)
    print("Connected successfully")

    # 执行SQL查询或操作
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # 提交更改（如果有）
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()

except pyodbc.Error as e:
    print("Error connecting to SQL Server:", e)