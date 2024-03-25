from flask import Flask, session, render_template , flash ,redirect,request, send_file
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import date, datetime, time, timedelta
from io import BytesIO
from icecream import ic
import pymongo,os,certifi,qrcode,secrets,pytz

from resources.api import QRcodeAPI

ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='backend > ')

load_dotenv()

#初始化資料庫連線
# client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
# db=client.order_system_v2
# users=db['users']
# customer=db.customer
# print('\x1b[6;30;42m' + '資料庫連線成功'.center(87) + '\x1b[0m')

app = Flask(__name__)
app.secret_key =os.getenv('secret_key')
CORS(app)


# 登入檢查裝飾器
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            flash('請先登入')
            return redirect('/login')
    return wrapper

# 加載api
api = Api(app)
api.add_resource(QRcodeAPI,'/api/qrcode')

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)  # 設定 session 的有效期限

# 登入頁面
@app.route('/login')
def login():
    return render_template('login.html')

#Home_page
@app.route('/')
def home():
    return render_template('generate.html')

@app.route('/generate_qrcode', methods=['POST'])
def generate():
    buffer = BytesIO()
    data = request.form.get('data')
    data = "https://127.0.0.1/verify_qrcode?key=" + secrets.token_hex(5) + "&generate_time=" + datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y%m%d%H%M') +"&"+ data
    ic(data)
    img = qrcode.make(data)
    img.save(buffer)
    buffer.seek(0)
    response = send_file(buffer, mimetype='image/png')
    return response

if __name__ == '__main__':
    app.run(debug=True,port=5100)
