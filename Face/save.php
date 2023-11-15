<?php
// 假設你已經有一個數據庫連接，並且有一個名為"users"的表，其中包含用戶名和相應的圖像數據。

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 從前端接收圖像數據
    $imageData = $_POST['image'];

    // 將數據解碼為圖片
    $decodedImage = base64_decode($imageData);

    // 生成一個唯一的圖像文件名
    $imageName = uniqid() . '.jpg';

    // 將圖像保存到伺服器上的指定目錄
    $imagePath = 'path/to/save/' . $imageName;
    file_put_contents($imagePath, $decodedImage);

    // 將圖像與數據庫中的圖像進行比較
    $userExists = false; // 标记用户是否存在

    // 在数据库中查询用户信息
    // 例如：SELECT * FROM users WHERE image_path = '$imagePath'

    // 如果查询到匹配的用户记录
    if ($userExists) {
        // 登录成功
        echo "Login successful";
    } else {
        // 登录失败
        echo "Login failed";
    }
}
?>