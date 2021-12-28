from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

#client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
client = MongoClient('mongodb+srv://test:sparta@cluster0.mgxkf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbinstaclone
#db.userinfo.insert_one({'id':'test', 'hash':'test'})

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    #id = request.form['id']
    #hassed_pw = request.form['hashpw']
    id = 'test'
    hassed_pw = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
    search_result = list(db.userinfo.find({'$and': [{'id': id}, {'hash': hassed_pw}]}, {'_id':False}))
    # 로그인
    if(len(search_result)==1):
        #datetime.datetime.strptime(str(time_tocken), '%Y-%m-%d %H:%M:%S.%f') 이건 문자열 형식에서 datetime.datetime 타입으로 바꾸어 주는 것
        time_tocken = str(datetime.utcnow()+timedelta(seconds=300))
        #print(time_tocken)
        header = {'id': id, 'time_tocken': time_tocken}
        #python 버전에 따라 다르지만 현 버전에서는 decode 가 필요 없이 그냥 문자열임
        jwt_tocken = jwt.encode(header, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'tocken':jwt_tocken})
    else:
        return jsonify({'result': 'fail', 'msg':'아이디/비밀번호가 정확하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 회원가입
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # DB에 저장
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # ID 중복확인
    return jsonify({'result': 'success'})

################################################################# instagram.html
@app.route('/instagram', methods=['GET'])
def user_get():
    # 이 자리에 DB에서 불러와야 함 user_doc =
    return jsonify({'list': userdoc})


@app.route('/instagram', methods=['POST'])
def user_post():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    user_doc = {
        'title': title_receive,
        'comment': comment_receive
    }
    print(user_doc) # 이 자리에 DB에 insert 해야함
    return jsonify({'msg': '포스팅이 완료되었습니다.'})

################################################################# comment.html(html명 아직 모름)
@app.route('/comment', methods=['GET'])
def user_get2():
    # 이 자리에 DB에서 불러와야 함 user_doc =
    return jsonify({'list': userdoc})


@app.route('/comment', methods=['POST'])
def user_post2():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    user_doc = {
        'title': title_receive,
        'comment': comment_receive
    }
    print(user_doc) # 이 자리에 DB에 insert 해야함
    return jsonify({'msg': '포스팅이 완료되었습니다.'})

# 한 db에서 보낼수 있나? 테스트할 필요성 있을듯


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)