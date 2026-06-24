from flask import Flask, request
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def search():
    # קבלת הטקסט שהמשתמש הקיש בטלפון
    query = request.args.get('search', '') or request.form.get('search', '')
    
    if not query:
        # אם המשתמש לא הקיש כלום, נבקש מימות המשיח להקריא הודעה ולקלוט קלט
        return "read=t-נא הקש את שם השיר או הזמר לחיפוש ולאחריו סולמית&mode=recording&max=50"

    # ביצוע החיפוש ביוטיוב (נשתמש בחיפוש חופשי ללא מפתח בשלב זה)
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    try:
        response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text
        # חילוץ ה-ID הראשון של הסרטון מהתוצאות
        start_idx = html.find('/watch?v=')
        if start_idx != -1:
            video_id = html[start_idx+9:start_idx+20]
            
            # כאן אנחנו מחזירים לימות המשיח פקודה להשמיע את הסרטון או לעבור לשלוחה הבאה
            # בשלב זה נגיד לה להקריא את ה-ID שמצאנו כדי לראות שזה עובד
            return f"read=t-נמצא סרטון. מזהה הסרטון הוא {video_id}&id_list={video_id}"
    except Exception as e:
        return "read=t-אירעה שגיאה במהלך החיפוש"
        
    return "read=t-לא נמצאו תוצאות, נסה שנית"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
