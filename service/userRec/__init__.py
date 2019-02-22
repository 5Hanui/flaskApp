import surprise as sp
import pandas as pd
from service.model import selectUser

def getData(): # 데이터 모으기
    user_list=selectUser()
    # print(user_list)
    rating_dic = {
        'user_id' : [],
        'wine_id': [],
        'points' : []
    }
    for u in user_list:
        rating_dic['user_id'].append(u['id'])
        rating_dic['wine_id'].append(u['title'])
        rating_dic['points'].append(u['point'])
    print(rating_dic)
    return rating_dic

def learn(id):
    print(id)
    dataset=getData()
    # 데이터 셋을 만든다.
    df = pd.DataFrame(dataset)
    # 데이터를 읽어와 surprise에서 사용하는 데이터 형태로
    # 만들어주는 객체, rating_sacle=(최소, 최대) <-평점기준
    reader = sp.Reader(rating_scale=(0.0, 5))
    # 딕셔너리에 담겨있는 데이터의 이름
    # 데이터셋을 만들 때 첫번재 이름이 사용자 구분값, 두번째
    # 이름이 상품 구분값, 세번째 이름이 평점으로 인식하여
    # 데이터를 읽어들이고 데이터셋으로 만든다.
    col_list = ['user_id', 'wine_id', 'points']

    data = sp.Dataset.load_from_df(df[col_list], reader)


    # 학습할 모델
    model = sp.KNNBasic(sim_options={'name': 'pearson'})
    # 학습한다.
    trainset = data.build_full_trainset()
    model.fit(trainset)
    result = model.get_neighbors(id, k=5)
    print(result)
    rec_list=list()
    for r in result:
        rec_list.append(str(dataset['wine_id'][r]))
        print(dataset['wine_id'][r])
    winelist = ','.join(rec_list)
    return winelist
    # for a1 in result:
        


if __name__ == '__main__':
    selectUser()
