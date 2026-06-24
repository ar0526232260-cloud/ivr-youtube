import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

# שליפת מפתח ה-API מהגדרות השרת ב-Render
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

@app.route("/search")
def search_youtube():
    # קבלת הטקסט שהמשתמש הקליד בטלפון (למשל חיפוש לפי מספרים או שם)
    query = request.args.get("q", "")
    if not query:
        return Response("ERR: No query provided", mimetype="text/plain")

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 1,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(url, params=params).json()
        items = response.get("items", [])
        if not items:
            return Response("id=none\ntitle=No video found", mimetype="text/plain")

        video_id = items[0]["id"]["videoId"]
        video_title = items[0]["snippet"]["title"]

        # החזרת תשובה במבנה פשוט שימות המשיח יודעת לקרוא
        return Response(f"id={video_id}\ntitle={video_title}", mimetype="text/plain")
    except Exception as e:
        return Response(f"ERR: {str(e)}", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
