import pymysql as sql

def selectLogin(uid, upw):
    db_session = None
    row = None
    try:
        db_session = sql.connect(host='localhost',
                            user='root',
                            password='root',
                            db='python_db',
                            charset='utf8',
                            cursorclass=sql.cursors.DictCursor)
        print("디비접속성공")
        with db_session.cursor() as cursor:
            sql_str = "SELECT * FROM users WHERE uid=%s AND upw=%s;"
            cursor.execute(sql_str, (uid, upw))  # 튜플이 1개일 경우 ('m',
            row = cursor.fetchone() #row는 회원정보
            # 디비쿼리문은 판단하지 않는다.
            # 오직 수행의 결과만을 제시한다.
            # (단, 쿼리상으로 어느정도 로직을 해결할 수 있다.)
    except Exception as e:
        print(e)
    finally:
        if db_session: #비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
            print("디비접속해제성공")
    #쿼리결과인 회원정보리턴
    return row

# 주식목록 가져오기, 이름기준 오름차순정렬 후 상위 10개만 가져오기
# selectTradeList
# pageNum : 페이지번호(사용값, 1, 2, 3 적용값 0,1,2)
# list_len: 한페이지에서 보여지는 데이터의 개수
def selectTradeList(pageNo=1, list_len=10): #기본값부여하면 파라미터 안보내도 가능
    db_session = None
    rows = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='python_db',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)
        print("디비접속성공")
        with db_session.cursor() as cursor:
            # sql_str = "SELECT * FROM tbl_trade ORDER BY NAME ASC LIMIT 0, 10;"
            sql_str = "SELECT * FROM tbl_trade ORDER BY NAME ASC LIMIT %s, %s;" 
            # (pageNo-1)*list_len : 시작페이스 인덱스
            cursor.execute(sql_str, ((pageNo-1)*list_len, list_len))  # 튜플이 1개일 경우 ('m',
            rows = cursor.fetchall()  # row는 회원정보
            # 디비쿼리문은 판단하지 않는다.
            # 오직 수행의 결과만을 제시한다.
            # (단, 쿼리상으로 어느정도 로직을 해결할 수 있다.)
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
            print("디비접속해제성공")
    #쿼리결과인 회원정보리턴
    return rows




# 검색어를 넣어서 결과 가져오기
def selectSearchWithKeyword(keyword):
    db_session = None
    rows = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='python_db',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)
        
        with db_session.cursor() as cursor:
            # %가 중첩으로 사용이 되서 쿼리 수행시 파라미터를
            # 전달하면 오동작하고, 일반 포맷팅도 문제가 된다.
            # format()를 이용하여 쿼리문을 먼저 완성하고 수행
            sql_str ='''
            SELECT CODE, name FROM tbl_trade 
            WHERE NAME LIKE '%{0}%'; 
            '''.format(keyword)
            cursor.execute(sql_str)  # 튜플이 1개일 경우 ('m',
            rows = cursor.fetchall()  # row는 회원정보
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
    return rows

# code를 넣어서 주식 정보 하나 가져오기
def selectStockByCode(code):
    db_session = None
    row = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='python_db',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)
        with db_session.cursor() as cursor:
            sql_str = "SELECT * FROM tbl_trade WHERE CODE = %s;"
            cursor.execute(sql_str, code)  # 튜플이 1개일 경우 ('m',
            row = cursor.fetchone()  # row는 회원정보
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
            print("디비접속해제성공")
    #쿼리결과인 회원정보리턴
    return row

# code에 일치되는 주식 정보를 찾아서 cur, rate를 수정한다.
def updateStockInfoByCode (info):
    db_session = None
    affected_row = 0 # 영향을 받은 row의 수
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='python_db',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)
        
        with db_session.cursor() as cursor:
            sql_str = '''
                UPDATE tbl_trade 
                SET cur=%s, rate=%s
                WHERE CODE=%s;
            '''
            cursor.execute(sql_str, 
                (info.get('cur'),info.get('rate'),info.get('code')))  # 튜플이 1개일 경우 ('m',
        # 실제 반영 => commit()
        db_session.commit() # 수정 실제 반영됨
        affected_row = db_session.affected_rows()
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
    # 영향을 받은 row의 수를 반환
    return affected_row

# 자료실 테이블에 데이터 삽입
# data : dict구조
def insertBbsData(data):
    db_session = None
    affected_row = 0  # 영향을 받은 row의 수
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='python_db',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)

        with db_session.cursor() as cursor:
            sql_str = '''
                INSERT INTO tbl_bbs
                (title, contents, author, path) 
                VALUES
                (%s, %s, %s, %s);
            '''
            cursor.execute(sql_str,
                           (data.get('title'), 
                           data.get('contents'), 
                           data.get('author'), 
                           data.get('path')
                           ))  # 튜플이 1개일 경우 ('m',
        # 실제 반영 => commit()
        db_session.commit()  # 수정 실제 반영됨
        affected_row = db_session.affected_rows()
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
    # 영향을 받은 row의 수를 반환
    return affected_row

# 자료실 게시판 최신 데이터 10개만 가져오기
def selectBbsList():
    db_session = None
    rows = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='python_db',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)

        with db_session.cursor() as cursor:
            # %가 중첩으로 사용이 되서 쿼리 수행시 파라미터를
            # 전달하면 오동작하고, 일반 포맷팅도 문제가 된다.
            # format()를 이용하여 쿼리문을 먼저 완성하고 수행
            sql_str = '''
            SELECT * FROM tbl_bbs ORDER BY id DESC limit 6;
            '''
            cursor.execute(sql_str)  # 튜플이 1개일 경우 ('m',
            rows = cursor.fetchall()  # row는 회원정보
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
    return rows

def selectWineDetail(idx):

    print("###################################################################")
    db_session = None
    rows = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='winedata',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)
        
        with db_session.cursor() as cursor:
            # %가 중첩으로 사용이 되서 쿼리 수행시 파라미터를
            # 전달하면 오동작하고, 일반 포맷팅도 문제가 된다.
            # format()를 이용하여 쿼리문을 먼저 완성하고 수행
            sql_str ='''
            SELECT * FROM wineinfo Where id = %s; 
            '''
            cursor.execute(sql_str, idx)  # 튜플이 1개일 경우 ('m',
            rows = cursor.fetchall()  # row는 회원정보
 
        print(rows)
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
    return rows


# 메인페이지 - 와인 데이터 가져오기
def selectWineInfo():
    db_session = None
    rows = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='winedata',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)

        with db_session.cursor() as cursor:
            # %가 중첩으로 사용이 되서 쿼리 수행시 파라미터를
            # 전달하면 오동작하고, 일반 포맷팅도 문제가 된다.
            # format()를 이용하여 쿼리문을 먼저 완성하고 수행
            sql_str = '''
            SELECT * FROM wineinfo ORDER BY id asc limit 10;
            '''
            cursor.execute(sql_str)  # 튜플이 1개일 경우 ('m',
            rows = cursor.fetchall()  # row는 회원정보
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
    return rows
# 메인페이지 - 와인 검색
def searchWineInfo(key):
    print(key)
    
    db_session = None
    rows = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='winedata',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)

        with db_session.cursor() as cursor:
            # %가 중첩으로 사용이 되서 쿼리 수행시 파라미터를
            # 전달하면 오동작하고, 일반 포맷팅도 문제가 된다.
            # format()를 이용하여 쿼리문을 먼저 완성하고 수행
            sql_str = '''
            SELECT * FROM wineinfo WHERE (description LIKE '%{0}%' OR description LIKE '%{1}%') 
            AND (title LIKE '%{2}%' ) ORDER BY id asc LIMIT 12;
            ''' .format(key['taste1'], key['taste2'], key['wineKeyword'])
            print(sql_str)
            # 튜플이 1개일 경우 ('m',
            cursor.execute(sql_str)
            rows = cursor.fetchall()  # row는 회원정보
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
    return rows


def selectUser():
    db_session = None
    row = None
    try:
        db_session = sql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='winedata',
                                 charset='utf8',
                                 cursorclass=sql.cursors.DictCursor)
        print("디비접속성공")
        with db_session.cursor() as cursor:
            sql_str = "SELECT * FROM user_rec ORDER BY id;"
            cursor.execute(sql_str)  # 튜플이 1개일 경우 ('m',
            row = cursor.fetchall()  # row는 회원정보
            # 디비쿼리문은 판단하지 않는다.
            # 오직 수행의 결과만을 제시한다.
            # (단, 쿼리상으로 어느정도 로직을 해결할 수 있다.)
            print(row)
    except Exception as e:
        print(e)
    finally:
        if db_session:  # 비번틀렸을 때 db_session은 None이 되므로 확인하기
            db_session.close()
            print("디비접속해제성공")
    #쿼리결과인 회원정보리턴
    return row

# 코드를 테스트할 때는 원하지 않을 때 작동되지 않도록
# 처리구문필요
if __name__ == '__main__':
    # print(selectLogin('m','1'))  #함수가 리턴안하면 none
    # print(selectLogin('m','2'))  # 함수가 리턴안하면 none
    # print(selectTradeList())
    # selectTradeList() 사용해서 얻은 결과를 가지고  종목명, 고가만 출력
    # for row in selectTradeList(1,5):
    #     print(row['name'], row.get('high'))
    # 존재하는 종목 체크
    # print(selectSearchWithKeyword('삼성'))
    # 없는 종목 테스트
    # print(selectSearchWithKeyword('ㅇㄹㄴㄹ'))
    # print(selectStockByCode('005930'))
    # 종목 정보 수정
    # if None:
    #     info = {
    #         'CODE':'005935',
    #         'cur':'41',
    #         'rate': '2.2'
    #     }
    #     if updateStockInfoByCode(info):
    #         print('수정성공')
    #     else:
    #         print('수정실패')
    # # 자료실 데이터 추가.
    #     data = dict()
    #     data['title']  = '제목'       
    #     data['contents'] = '내용',
    #     data['author'] = '작성자',
    #     data['path'] = '파일경로'
    #     if insertBbsData(data): print('등록성공') #statement한줄일경우 옆으로 써도됨.
    #     else: print('등록실패')
    # # 자료실 데이터 가져오기
    print(selectUser())
    # pass


    
