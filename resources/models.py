from dotenv import load_dotenv
from datetime import datetime
from icecream import ic
from io import BytesIO
from flask import request
import pymongo,os,certifi,secrets,pytz,qrcode

load_dotenv()

client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.qrcode_clockin
qrcode_data=db.qrcode_data

ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='backend > ')

def regenerate(key:str):
    if key=='True':
        key=secrets.token_hex(5)
    qrcode_data.update_many({'status':'valid'},{'$set':{'status':'invalid'}})
    qrcode_data.insert_one({'key':key,'status':'valid','generate_date':datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')})
    return datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')

def verify(key:str):
    data=qrcode_data.find_one({'key':key})
    generate_date=datetime.strptime(str(data['generate_date']), "%Y-%m-%d")
    recent_date=datetime.strptime(str(datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')), "%Y-%m-%d")
    if data['status'] =='invalid' or generate_date!=recent_date :
        return False
    return True

def display(location:str):
    data=qrcode_data.find_one({'status':'valid'})
    if data==None:
        ic(regenerate('True'))
        data=qrcode_data.find_one({'status':'valid'})
    generate_date=datetime.strptime(str(data['generate_date']), "%Y-%m-%d")
    recent_date=datetime.strptime(str(datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')), "%Y-%m-%d")

    if generate_date!=recent_date:
        ic(regenerate('True'))
        data=qrcode_data.find_one({'status':'valid'})
    buffer = BytesIO()
    data = "http://127.0.0.1:5100/api/qrcode?data={verify}["+data['key']+"]("+location+")"
    ic(data)
    img = qrcode.make(data)
    img.save(buffer)
    buffer.seek(0)
    return buffer

    