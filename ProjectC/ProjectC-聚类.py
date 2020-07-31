from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import pandas as pd
import matplotlib.pyplot as plt


# 数据规范化
def data_normalize(train_x):
    # 数据中的字符串数字化
    str_name = ['CarName', 'fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginelocation',
                'enginetype', 'cylindernumber', 'fuelsystem']
    for i in range(len(str_name)):
        le = LabelEncoder()
        train_x[str_name[i]] = le.fit_transform(train_x[str_name[i]])
    # 规范化到 [0,1] 空间
    min_max_scaler = preprocessing.MinMaxScaler()
    train_x = min_max_scaler.fit_transform(train_x)
    return train_x


# K-Means 手肘法：统计不同K取值的误差平方和
def shouzhou(train_x):
    sse = []
    for k in range(1, 50):
        # kmeans算法
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_x)
        # 计算inertia簇内误差平方和
        sse.append(kmeans.inertia_)
    x = range(1, 50)
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(x, sse, 'o-')
    plt.show()


# 轮廓系数
def lunkuo(train_x):
    sc_scores = []
    k_value = []
    for k in range(2, 50):
        kmeans = KMeans(n_clusters=k)
        kmeans_model = kmeans.fit(train_x)
        sc_score = silhouette_score(train_x, kmeans_model.labels_, metric='euclidean')
        sc_scores.append(sc_score)
        k_value.append(k)
    plt.xlabel('k')
    plt.ylabel('SCS')
    plt.plot(k_value, sc_scores, '*-')
    plt.show()


### 使用KMeans聚类
def K_Means(train_x, n_cluster, data):
    kmeans = KMeans(n_clusters=n_cluster)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    generate_result(data,predict_y)

#生成结果集
def generate_result(data, predict_y):
    #直接生成预测结果总表
    data['predict_y'] = predict_y
    #通过找到有vw关键字的车辆对应的预测值进行分类输出
    data_list_containvw = data.loc[data['CarName'].str.contains('vw')]
    vw_predict_y = data_list_containvw['predict_y'].to_list()
    vw_predict_y_nodup = []
    #如果vw车辆在同一分组输出同一分组内所有数据
    #如果vw车辆不在同一分组输出VW车辆所在不同分组内所有数据
    for item in vw_predict_y:
        if item not in vw_predict_y_nodup:
            vw_predict_y_nodup.append(item)
    #分组输出
    for i in range(0,len(vw_predict_y_nodup)):
        #找到和vw车辆同一个预测值对应数据集并输出csv
        data.loc[data['predict_y']==vw_predict_y[i]].to_csv('vw_cluster_result.csv', encoding='utf-8')



def main():
    # 数据读取
    data = pd.read_csv('./CarPrice_Assignment.csv')
    train_x = data.iloc[:, 1:]
    # 处理数据
    train_data = data_normalize(train_x)
    # 手肘法选取K值
    shouzhou(train_data)
    # 轮廓系数法选取K值
    lunkuo(train_data)
    # 确定K值
    K_Num = int(input('请输入聚类的类数K为：'))
    # KMeans聚类
    K_Means(train_data, K_Num, data)



if __name__ == '__main__':
    main()
