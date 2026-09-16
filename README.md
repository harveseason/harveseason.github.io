# Harvey Huang Portfolio

純 HTML / CSS / JS 靜態網站，不需要安裝任何套件。

## 本機預覽
在 `site` 資料夾打開終端機：

```
python3 -m http.server 8000
```
然後用瀏覽器開 http://localhost:8000

## 修改內容
- 作品文字、標籤、圖片順序：`_build/content.py`
- 首頁 / About 版面文字：`_build/build.py`
- 樣式：`assets/css/style.css`，互動：`assets/js/main.js`

改完 `_build` 裡的檔案後執行，重新產生所有頁面：

```
python3 _build/build.py
```

新增作品圖片：放進 `assets/img/<作品 slug>/`（建議寬 1920px 的 jpg），並在 `content.py` 的 `gallery` 加上檔名（不含 .jpg）。
圖片尺寸寫在 `assets/img/manifest.json`，新增圖片後可以一併補上 w / h，避免載入時版面跳動。

## 上線
把整個 `site` 資料夾拖到 Netlify Drop（https://app.netlify.com/drop），或推到 GitHub 後接 Vercel / GitHub Pages 即可。
`_build` 資料夾不影響網站，可一起上傳。
