import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# 处理一些冲突
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

# *******************************************数据处理开始**************************************************************
# 数据读取
humidity = pd.read_excel('./dataset/3-humidity.xls')  # 湿度数据
bio_amount = pd.read_excel('./dataset/15-plant-bio.xlsx', sheet_name='2016-2020物种数据库')  # 生物量数据
bio_amount = bio_amount.drop('Unnamed: 15', axis=1)  # 去除多余的一列

"""
由于生物量只有5，6，7，8，9月这几个月的数据
同样湿度数据也只取这几个月的数据
"""
# print(humidity.info())
months = [5, 6, 7, 8, 9]
humidity_sub = humidity[humidity['月份'].isin(months)]
humidity_sub.pop('经度(lon)')
humidity_sub.pop('纬度(lat)')

# 将生物量的日期转为月份
# 提取月份, 注意到有一个6月1号的数据，可以将看作5月的数据(特殊处理)
bio_amount['月份'] = bio_amount['日期'] \
    .apply(lambda x: int(x.split('.')[1]) if int(x.split('.')[2]) != 1 else int(x.split('.')[1]) - 1) \
    .astype('int64')  # 这里要注意数据是str类型，所以要转化为int类型，不然不能进行数据运算，导致结果有问题

# merge数据
all_df = bio_amount.merge(humidity_sub, on=['年份', '月份'], how='left')
all_df['年份'] = all_df['年份'].astype('str')
# all_df.to_csv('all_df.csv', index=False)

# 只保留需要的列
needs = ['年份', '月份', '轮次', '处理', '植物种名', '干重(g)', '10cm湿度(kg/m2)',
         '40cm湿度(kg/m2)', '100cm湿度(kg/m2)', '200cm湿度(kg/m2)']
all_df = all_df[needs]
# all_df.to_csv('all_df.csv', index=False)
# *******************************************数据处理结束**************************************************************

# *******************************************数据可视化开始**************************************************************
# 数据可视化看看基本的数据分布，进行粗略的数据分析，看看放牧与这些数据直接的关系

# 1. 看看不同植物与不同月份下的湿度数据分布，因为湿度和放牧之间数据变化不大，只要展示月份之间的变化即可
humidity_process = all_df[['年份', '月份', '处理',  '10cm湿度(kg/m2)', '40cm湿度(kg/m2)',
                            '100cm湿度(kg/m2)', '200cm湿度(kg/m2)']].drop_duplicates().reset_index()

table10 = pd.pivot_table(humidity_process, values='10cm湿度(kg/m2)', index=['年份'], columns=['月份'])

plt.figure(figsize=(18, 14))

plt.subplot(221)
sns.lineplot(data=table10)
plt.title('各个年份不同月份湿度折线图(10cm)')
plt.ylabel('湿度(kg/m2)')
# plt.savefig('./images/各个年份不同月份湿度折线图(10cm).png')
# plt.show()  # 这个必须放在savefig后面不然显示完会清楚图层

table40 = pd.pivot_table(humidity_process, values='40cm湿度(kg/m2)', index=['年份'], columns=['月份'])

plt.subplot(222)
sns.lineplot(data=table40)
plt.title('各个年份不同月份湿度折线图(40cm)')
plt.ylabel('湿度(kg/m2)')
# plt.savefig('./images/各个年份不同月份湿度折线图(40cm).png')

table100 = pd.pivot_table(humidity_process, values='100cm湿度(kg/m2)', index=['年份'], columns=['月份'])

plt.subplot(223)
sns.lineplot(data=table100)
plt.title('各个年份不同月份湿度折线图(100cm)')
plt.ylabel('湿度(kg/m2)')
# plt.savefig('./images/各个年份不同月份湿度折线图(100cm).png')

table200 = pd.pivot_table(humidity_process, values='200cm湿度(kg/m2)', index=['年份'], columns=['月份'])

plt.subplot(224)
sns.lineplot(data=table200)
plt.title('各个年份不同月份湿度折线图(200cm)')
plt.ylabel('湿度(kg/m2)')
# plt.savefig('./images/各个年份不同月份湿度折线图(200cm).png')

plt.savefig('./images/各个年份不同月份湿度折线图(all).png')
# plt.show()

# 2. 生物量与放牧的关系
bio_amount_process = all_df[(all_df['年份'] == '2016') & (all_df['月份'] == 5)]

plt.figure(figsize=(18, 14))

table2016_5 = pd.pivot_table(bio_amount_process, values='干重(g)', index=['处理'], columns=['植物种名'])
sns.lineplot(data=table2016_5)
plt.title('植被各个生物量')
plt.ylabel('干重(g)')
plt.show()

# *******************************************数据可视化结束**************************************************************

