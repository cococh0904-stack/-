# AI 校園導師小幫手

藍白簡約風格的校園問答網站，包含規則回答、Gemini AI、W03 備援回答。

## 專案檔案
- `index.html`：網站前端
- `app.py`：Flask API 後端
- `requirements.txt`：Python 套件
- `.gitignore`：忽略本機機密與暫存檔

## 部署方式
1. 將整個資料夾上傳至 GitHub repository。
2. 在 Render 建立 **Web Service**，連接此 GitHub repository。
3. Build Command：`pip install -r requirements.txt`
4. Start Command：`gunicorn app:app`
5. 在 Render Environment 設定 `GEMINI_API_KEY` 為你自己的 Gemini API 金鑰。
6. 部署完成後，複製 Render 網址，將 `index.html` 中的 `API_BASE` 改成該網址。
7. 前端可用 GitHub Pages 發佈；GitHub Pages 的來源設定選 `main` 分支與 `/ (root)`。

注意：不要把 Gemini API 金鑰貼進 `index.html` 或上傳到 GitHub。
