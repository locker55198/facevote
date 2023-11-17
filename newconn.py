def save_to_database(username, image):
    # 連接到MySQL數據庫
    cnx = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    
    cursor = cnx.cursor()

    # 創建保存用戶名和圖片的表（如果表不存在）
    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            image BLOB
        )
    """
    cursor.execute(create_table_query)

    # 將用戶名和圖片插入到表中
    insert_query = """
        INSERT INTO users (username, image) VALUES (%s, %s)
    """
    cursor.execute(insert_query, (username, image))

    # 提交更改並關閉數據庫連接
    cnx.commit()
    cursor.close()
    cnx.close()