from flask import Flask, request, send_file, render_template
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # عرض صفحة HTML عند زيارة الموقع
    return render_template('index.html')

@app.route('/download')
def download_image():
    # الحصول على رابط الصورة من معلمات الطلب
    url = request.args.get('url')
    
    # إعداد رأس "User-Agent" لمحاكاة متصفح فعلي
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # إرسال الطلب إلى الرابط مع الرأس "User-Agent"
        response = requests.get(url, stream=True, headers=headers)
        
        # التحقق من نجاح الطلب
        response.raise_for_status()
        
        # تخزين الصورة مؤقتًا في الذاكرة
        img_data = BytesIO(response.content)
        
        # إرسال الصورة للمتصفح كملف لتحميله
        return send_file(img_data, mimetype='image/jpeg', as_attachment=True, download_name="downloaded_image.jpg")
    
    except requests.exceptions.RequestException as e:
        return f"خطأ في تنزيل الصورة: {e}", 400

if __name__ == "__main__":
    app.run(debug=True)
