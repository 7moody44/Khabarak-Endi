<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>Article - خبرك عندي</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .article-container {
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        iframe {
            width: 100%;
            height: 80vh;
            border: none;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .back-btn {
            display: block;
            margin: 20px 0;
            padding: 10px 15px;
            background: #333;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            text-align: center;
        }
    </style>
</head>
<body>
    <!-- Keep header consistent -->
    <header>
        <div class="header-top">
            <div class="logo">
                <span class="red">خبرك</span>
                <span class="green">عندي</span>
            </div>
            <a href="index.html" class="back-btn">Back to Home</a>
        </div>
    </header>

    <!-- Article Viewer -->
    <div class="article-container">
        <iframe id="article-frame" src="about:blank"></iframe>
    </div>

    <script src="js/article.js"></script>
</body>
</html>
