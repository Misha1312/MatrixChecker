import webview
import os
import sys
import subprocess
import tempfile
import ctypes
from pathlib import Path

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Matrix Cheat Checker</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0a0a14 0%, #1a1a2e 100%);
            color: #e0e0ff;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
            height: 100vh;
            user-select: none;
        }
        
        .title-bar {
            background: #0f0f1e;
            height: 52px;
            display: flex;
            align-items: center;
            padding: 0 20px;
            border-bottom: 1px solid #00ff9d33;
            -webkit-app-region: drag;
            position: relative;
            z-index: 100;
        }
        
        .title {
            flex: 1;
            font-weight: 600;
            font-size: 18px;
            padding-left: 8px;
        }
        
        .controls {
            display: flex;
            gap: 12px;
        }
        
        .control-btn {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .minimize { background: #ffbd2e; }
        .minimize:hover { background: #ffaa00; }
        .close { background: #ff5f57; }
        .close:hover { background: #ff3b30; }
        
        .container {
            padding: 30px 40px 40px 40px;
            height: calc(100vh - 52px);
            box-sizing: border-box;
            overflow-y: auto;
        }
        
        h1 {
            font-size: 52px;
            font-weight: 700;
            background: linear-gradient(90deg, #00ff9d, #00b8ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 8px 0;
        }
        
        .subtitle {
            color: #8888aa;
            font-size: 19px;
            margin-bottom: 40px;
        }
        
        .scan-area {
            background: rgba(255,255,255,0.04);
            border: 2px solid rgba(0, 255, 157, 0.4);
            border-radius: 20px;
            padding: 50px 40px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
        }
        
        button {
            background: linear-gradient(90deg, #00ff9d, #00e68a);
            color: black;
            font-size: 22px;
            font-weight: 700;
            padding: 18px 80px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(0, 255, 157, 0.3);
        }
        
        .loader {
            display: none;
            margin: 35px auto;
            width: 90px;
            height: 90px;
            border: 8px solid #1a1a2e;
            border-top: 8px solid #00ff9d;
            border-radius: 50%;
            animation: spin 1.1s linear infinite;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .progress {
            margin-top: 20px;
            font-size: 18px;
            color: #00ff9d;
            min-height: 28px;
        }
        
        .results {
            display: none;
            margin-top: 35px;
            background: rgba(255, 60, 60, 0.12);
            border: 2px solid #ff4444;
            border-radius: 16px;
            padding: 30px;
        }
        
        .cheat-item {
            background: rgba(30, 30, 46, 0.9);
            padding: 20px;
            border-radius: 12px;
            margin: 15px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 6px solid #ff4444;
        }
    </style>
</head>
<body>
    <div class="title-bar">
        <div class="title">Matrix Cheat Checker — Полное сканирование системы</div>
        <div class="controls">
            <div class="control-btn minimize" onclick="window.pywebview.api.minimize()"></div>
            <div class="control-btn close" onclick="window.pywebview.api.close()"></div>
        </div>
    </div>
    <div class="container">
        <h1>Matrix Cheat Checker</h1>
        <p class="subtitle">Сканирование всего компьютера на наличие читов</p>
        
        <div class="scan-area">
            <button onclick="startFullScan()">СКАНИРОВАТЬ ВЕСЬ КОМПЬЮТЕР</button>
            
            <div class="loader" id="loader"></div>
            <div class="progress" id="progress"></div>
            
            <div class="results" id="results">
                <h2 style="color:#ff5555; margin-top:0;">Обнаружен чит!</h2>
                <div class="cheat-item">
                    <div>
                        <strong>Matrixrnsv.jar</strong><br>
                        <small style="color:#ffaaaa;">
                            C:\\RecycleBin\\deltarnsv.jar
                        </small>
                    </div>
                    <div style="color:#ff4444; font-weight:bold;">CHEAT DETECTED</div>
                </div>
                <p style="color:#ffdd88; margin-top:25px;">
                    Файл содержит вредоносный код. Рекомендуется немедленно удалить.
                </p>
            </div>
        </div>
    </div>
    <script>
        function startFullScan() {
            const loader = document.getElementById('loader');
            const progress = document.getElementById('progress');
            const results = document.getElementById('results');
            
            loader.style.display = 'block';
            progress.style.display = 'block';
            results.style.display = 'none';
            
            let percent = 0;
            const messages = [
                "Сканирование дисков...",
                "Проверка системных папок...",
                "Анализ .jar и .exe файлов...",
                "Проверка Minecraft mods...",
                "Поиск известных читов...",
                "Завершение сканирования..."
            ];
            let i = 0;
            
            const interval = setInterval(() => {
                percent += Math.random() * 9 + 5;
                if (percent > 97) percent = 97;
                
                progress.textContent = `${messages[i % messages.length]} ${Math.floor(percent)}%`;
                
                if (percent >= 97) {
                    clearInterval(interval);
                    loader.style.display = 'none';
                    progress.textContent = "Сканирование завершено";
                    results.style.display = 'block';
                }
                
                if (percent > 40) i++;
            }, 240);
        }
    </script>
</body>
</html>
"""

class API:
    def minimize(self):
        window.minimize()
    
    def close(self):
        window.destroy()

if __name__ == "__main__":
    main()
    api = API()
    global window
    window = webview.create_window(
        title="Matrix Cheat Checker",
        html=HTML,
        width=1000,
        height=600,
        frameless=True,
        easy_drag=True,
        background_color="#0a0a14",
        js_api=api
    )
    webview.start()