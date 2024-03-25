from flask import send_file,make_response,render_template
from flask_restful import Resource,reqparse
from icecream import ic
from resources.models import*
import re
ic.configureOutput(includeContext=True)
ic.configureOutput(prefix='backend > ')



class QRcodeAPI(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('data',type=str,location=['values'])

    #      {mode}               [key]           
    # regenerate or verify       True   

    def get(self):
        data = ic(self.parser.parse_args()['data'])
        try:
            mode=re.findall(r"[{](.*?)[}]", data)[0]
            key=re.findall(r"[[](.*?)[]]", data)[0]
            location=re.findall(r"[(](.*?)[)]", data)[0]
            ic({'mode':mode,'key':key,'location':location})
        except:
            return {'message':'請輸入正確格式{mode}[key](location)'},400
        
        if mode == 'regenerate':
            if len(key)==0 or key==None:
                ic(regenerate('None'))
            elif key=='True' or key==True:
                ic(regenerate('True'))
        elif mode == 'verify':
            if ic(verify(key)):
                response = make_response(render_template('verify.html',message='驗證成功'))
            else:
                response = make_response(render_template('verify.html',message='驗證碼失效或發生未知錯誤'))
            response.headers['Content-Type'] = 'text/html'
            return response

                
    def post(self):
        data = ic(self.parser.parse_args()['data'])
        try:
            location=re.findall(r"[(](.*?)[)]", data)[0]
            ic({'location':location})
        except:
            return {'message':'請輸入正確格式(location)'},400
        ic(display(location))
        return send_file(display(location), mimetype='image/png')

    