'''
 flask 객체 생성
 기본 환경설정
 환경 변수, 디비 초기화
 라우트(블루 프린트)
 라이프사이클(생애주기)
 필터(세션처리)
'''
from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
# 서버 시작점에서부터 패키 경로를 따진다.
from service.model import selectLogin, selectTradeList as stl, selectSearchWithKeyword
from service.model import insertBbsData, selectBbsList, selectWineInfo, searchWineInfo, selectWineDetail, inputPointInfo, selectId, selectRec
from service.userRec import learn
# from service.model import * 하면 예약어 쓸수가 없음 as불가능

# 플라스크 앱 생성W
def createApp():
    app = Flask(__name__)
    # 1. 세션 키 생성 => 통상 값은 해쉬값(중복되지 않는 임의값) 사용
    app.secret_key = 'adfad2321fa34dfasdfadfafdff13131kjjlk12' # 사용자가 많지 않으므로 임의로 사용
    initRoute(app)
    return app

# 라우트 초기화 담당
def initRoute(app):
    # 라우트 설정
    @app.route('/', methods=['GET', 'POST'])
    def home():
        # learn(1)
        if not 'uid' in session:  # 세션이 없어도 처음 접근할 수 있는 로그인페이지. 뒤/앞으로가기 버튼 안먹음.
            return redirect(url_for('login'))
        # 로그인 성공 => 쿠키 설정.
        resp = make_response(render_template('index.html')) #세션은 모든곳에서 사용가능 id 정보 들어있음.!!
        # 쿠키 세팅
        resp.set_cookie('uid', session['uid']) #쿠키도 자료구조 딕셔너리!
        if request.method == 'GET':
            infos = selectWineInfo()
            print(infos)
            return render_template('index.html', infos=selectWineInfo())
        else:
            taste1 = request.form.get('taste1')
            tasteBig = {'a': 'spicy', 'b': 'fruity', 'c': 'acidity', 'd': 'floral',
                        'e': 'oaky', 'f': 'citrus', 'g': 'woody', 'h': 'light', 'i': 'sweet', 'j': 'dry'}
            taste2 = request.form.get('taste2')
            wineKeyword = request.form.get('wineKeyword')
            if (taste1 == 'Select') and (taste2=='Select') and (wineKeyword == ''):
                return render_template('index.html', infos=selectWineInfo())
            search = {'taste1': tasteBig[taste1],'taste2': taste2, 'wineKeyword': wineKeyword}
            infos=searchWineInfo(search)
            if infos==():
                return render_template("alertEx.html", msg='입력결과가 없습니다.', url='/')
            return render_template('index.html', infos=searchWineInfo(search))

        return resp #응답을 가로채서 던짐.

    # 로그인
    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method=='GET':
            # 쿠키를 읽어와서 아이디창에 채운다.
            uid = request.cookies.get('uid')
            if not uid: # 쿠키 없으면
                uid = '' #쿠키는 아이디를 들고 있거나 없거나.
            return render_template('login.html',
                    title='데이터 분석관리 로그인',uid=uid)
        else: 
            # 잘 넘어오는지 체크
            uid = request.form.get('uid')
            upw = request.form.get('upw')
            # return uid + " : " + upw
            if not uid or not upw:
                return render_template("alertEx.html", msg='정확하게 입력하세요')
            else:
                row = selectLogin(uid,upw)
                if row: #회원이다
                    # 세션설정(회원이 로그인 했음을 서버가 인지하는 방법)
                    # 간단한 것은 서버 메모리 사용, 통상 고급 -> 디비, 써드파트로 관리
                    # 세션 => 딕셔너리
                    # 세션 생성 // 권한이 없으면 접근을 못함.
                    session['uid'] = uid
                    session['name'] = row['name'] #row에 조회결과 있음//
                    return redirect(url_for('home')) # url은 직접 하드코딩하지 않는다!! redirect('/')=>XX
                else: #회원아니다
                    return render_template("alertEx.html", msg='회원아님')
    
    # 로그아웃
    @app.route('/logout') #로그아웃은 화면이 없고 일만하고 던짐.
    def logout():
        # 세션 없이 접근했을 경우 -> 홈페이지로 리다이렉트
        if not 'uid' in session:  # 세션체크
            return redirect(url_for('home'))
        # 세션제거
        if 'uid' in session:
            session.pop('uid', None) #uid를 제거하면서 반환해줌
        if 'name' in session:
            session.pop('name', None)
        # 홈페이지 리다이렉트
        return redirect(url_for('home'))

    # 주식관리 페이지
    @app.route('/stocks')  # 이요청이 오면 다음으로 처리
    def stocks():
        try:  # http://127.0.0.1:5000/?no=2&amt=10 페이지 이동 가능
            pageNo = int(request.args.get('no'))
            list_len = int(request.args.get('amt'))
        except Exception as e:
            pageNo = 1
            list_len = 10
        rows    = stl(pageNo=pageNo, list_len=list_len)
        return render_template('stocks.html', trades=rows)

    # POST 전용
    @app.route('/search', methods=['POST'])
    def search():  # 아무것도 안쓰면 GET방식..
        # 1. 전달된 데이터 획득 -> print로 출력
        keyword = request.form.get('keyword')  # 키:input태그 속성
        print(keyword)
        # 2. 데이터를 d8로 보내서 쿼리 수행
        rows = selectSearchWithKeyword(keyword)
        if not rows:  # 결과가 없다면
            rows = "{}"
        # 3. 검색 결과를 받아서 json으로 응답(기존 웹화면구성)
        # => 이런식으로 구성된 서버=>미들웨어/어플리케이션서버
        return jsonify(rows)

    # 와인추천
    @app.route('/rec')
    def rec():
        # id = selectId(session['uid'])[0]['id']
        # print(id)
        winelist=learn(2)
        print("winelist: "+winelist)
        # if request.method == 'GET':
        return render_template('rec.html'
                               , infos=selectRec(winelist))
        # else:
        #     # 1. 데이터 획득
        #     title       = request.form.get('title')
        #     contents    = request.form.get('contents')
        #     author      = session['uid']
        #     f           = request.files['files'] #파일 여러개 업로드할때 하나만 뜸
        #     # ----------------------------------------------------------------
        #     files       = request.files.getlist('files')
        #     print('='*10)
        #     import os # 원래는 맨위
        #     nmList = list()
        #     for file in files: # 파일리스트
        #         # file : 파일 
        #         print(file.filename)
        #         save_path = os.path.join(os.getcwd(),
        #                              'service', 'static', 'upload', file.filename)
        #         # 모든 파일을 디스크상에 저장
        #         # f->file로 수정후 ctrl+shift+R
        #         file.save(save_path)
        #         nmList.append('/static/upload/'+ file.filename)
        #     print('='*10)
        #     # ----------------------------------------------------------------
        #     data = {
        #         "title":title,
        #         "contents" : contents,
        #         "author": author,
        #         "path":"|".join(nmList)
        #     }
        #     msg = None
        #     url = None
        #     if insertBbsData(data):
        #         # 4. 응답(등록되었습니다.) -> 확인 -> /bbs 이동(get)
        #         msg = "등록 성공"
        #         url = url_for('bbs')
        #     else:
        #         msg = '등록 실패'
        #     return render_template("alertEx.html", msg=msg ,url=url)
            #######################################################3
            # return ''






    # 와인 정보 페이지
    @app.route('/wineinfo/<idx>')  # 이요청이 오면 다음으로 처리
    def wineinfo(idx):
        print(idx)
        details = selectWineDetail(idx)

        return render_template('wineinfo.html',details = details)



    @app.route('/graph', methods=['GET'])
    def graph():
        if request.method == 'GET':
            return render_template('graph.html', rows=selectBbsList())
        # else:
        #     # 1. 데이터 획득
        #     title = request.form.get('title')
        #     contents = request.form.get('contents')
        #     author = session['uid']
        #     f = request.files['files']  # 파일 여러개 업로드할때 하나만 뜸
        #     # ----------------------------------------------------------------
        #     files = request.files.getlist('files')
        #     print('='*10)
        #     import os  # 원래는 맨위
        #     nmList = list()
        #     for file in files:  # 파일리스트
        #         # file : 파일
        #         print(file.filename)
        #         save_path = os.path.join(os.getcwd(),
        #                                  'service', 'static', 'upload', file.filename)
        #         # 모든 파일을 디스크상에 저장
        #         # f->file로 수정후 ctrl+shift+R
        #         file.save(save_path)
        #         nmList.append('/static/upload/' + file.filename)
        #     print('='*10)
        #     # ----------------------------------------------------------------
        #     data = {
        #         "title": title,
        #         "contents": contents,
        #         "author": author,
        #         "path": "|".join(nmList)
        #     }
        #     msg = None
        #     url = None
        #     if insertBbsData(data):
        #         # 4. 응답(등록되었습니다.) -> 확인 -> /bbs 이동(get)
        #         msg = "등록 성공"
        #         url = url_for('bbs')
        #     else:
        #         msg = '등록 실패'
        #     return render_template("alertEx.html", msg=msg, url=url)
            #######################################################3
            # return ''

    @app.route('/tasteofwine', methods=['GET', 'POST'])
    def tasteofwine():
        if request.method == 'GET':
            return render_template('tasteofwine.html', infos=selectWineInfo())

    @app.route('/pointsinfo/', methods=['GET', 'POST'])
    def pointsinfo():
        point_list = {}
        title_list = {}
        user_id = session['uid']
        for i in range(1,11):
            title_list[i] = request.values.get(f'rating_id{i}')
            point_list[i] = request.values.get(f'rating{i}')
            id_list = request.form.get('id')
            id = request.form.get('user_id')
            if (point_list[i]) == None:
                point_list[i] = 0
        print(point_list)
        id=selectId(user_id)
        print(id[0]['id'])
        print(session['uid'])
        print(title_list)

        inputPointInfo(id[0]['id'],point_list,title_list)
        winelist = learn(2)
        
        return render_template('rec.html', infos=selectRec(winelist))
         

