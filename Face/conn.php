<?php
// 設置數據庫連接
$servername = "localhost";
$username = "your_username";
$password = "your_password";
$dbname = "your_database";

// 創建數據庫連接<?php
// 設置數據庫連接
$servername = "localhost";
$username = "your_username";
$password = "your_password";
$dbname = "your_database";

// 創建數據庫連接
$conn = new mysqli($servername, $username, $password, $dbname);

// 檢查連接是否成功
if ($conn->connect_error) {
    die("連接數據庫失敗: " . $conn->connect_error);
}

// 獲取POST請求中的圖像數據
$imageData = $_POST['image'];

// 解碼Base64圖像數據
$imageData = str_replace('data:image/jpeg;base64,', '', $imageData);
$imageData = str_replace(' ', '+', $imageData);
$imageData = base64_decode($imageData);

// 生成圖像文件名
$filename = uniqid() . '.jpg';

// 保存圖像文件到指定目錄
$file = fopen($filename, 'w');
fwrite($file, $imageData);
fclose($file);

// 將圖像文件名保存到數據庫
$sql = "INSERT INTO images (filename) VALUES ('$filename')";

if ($conn->query($sql) === TRUE) {
    echo "圖像已保存到數據庫";
} else {
    echo "保存圖像到數據庫失敗: " . $conn->error;
}

// 關閉數據庫連接
$conn->close();
?>