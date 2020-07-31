import pandas as pd
import time
from efficient_apriori import apriori as ap


# 数据读取及分析数据提取
file = open('./订单表.csv')
data = pd.read_csv(file)
dataset = data[['客户ID', '产品型号名称']]
dataset = dataset.drop(dataset[dataset.产品型号名称 == 'none'].index)
dataset = dataset.sort_values(by='客户ID', ascending=True)


## 采用efficient_apriori工具包
def apriori():
    start = time.time()
    # 设置索引
    order_series = dataset.set_index('客户ID')['产品型号名称']
    # 将产品型号名称数据按照客户ID且去重后放入transactions中
    transactions = []
    temp_index = 0
    temp = set()
    for i, v in order_series.items():
        if i != temp_index:
            temp = set()
            temp_index = i
            temp.add(v)
            transactions.append(temp)
        else:
            temp.add(v)
    # 对数据进行关联分析
    itemsets, rules = ap(transactions, min_support=0.01, min_confidence=0.3)
    print('频繁项集：', itemsets)
    print('关联规则：', rules)
    end = time.time()
    print("用时：", end - start)



def main():
    apriori()



if __name__ == '__main__':
    main()




