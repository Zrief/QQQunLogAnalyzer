import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from datetime import datetime
import os

plt.rcParams['font.sans-serif'] = ['Simhei']  #显示中文
plt.rcParams['axes.unicode_minus'] = False    #显示负号
# 创建OutputTimeseries文件夹，如果不存在
if not os.path.exists('OutputTimeseries'):
    os.makedirs('OutputTimeseries')

# 导入数据
df = pd.read_csv('OrganizedData.csv', encoding='utf-8-sig')

# 将 'Time' 列转换为 datetime 类型
df['Time'] = pd.to_datetime(df['Time'])

# 创建一个新的列 'Hour'，表示每条信息发送的小时
df['Hour'] = df['Time'].dt.hour

# 创建一个新的列 'Day_of_Week'，表示每条信息发送的是一周中的哪一天
df['Day_of_Week'] = df['Time'].dt.dayofweek

# 统计每个用户发送的消息总数
message_count = df['Sender'].value_counts()

# 统计每个用户在各个小时发送的消息数量
message_count_by_hour = df.groupby(['Sender', 'Hour']).size().reset_index(name='Counts')

# 如果sender数量大于30，则只展示前30个
if len(message_count) > 20:
    top_senders = message_count.index[:20]
    message_count = message_count.loc[top_senders]
    message_count_by_hour = message_count_by_hour[message_count_by_hour['Sender'].isin(top_senders)]

# 根据时间范围确定图的宽度
time_range = df['Time'].max() - df['Time'].min()
width = max(10, time_range.days / 30)  # 每30天增加1个单位的宽度
barwidth = len(message_count)/2

# 绘制每个用户发送的消息总数的柱状图
plt.figure(dpi=300,figsize=(barwidth, 10))
plt.grid()
sns.barplot(y=message_count.index, x=message_count.values,hue=message_count.index)
plt.title('水群榜（不准确仅供娱乐）',fontsize=20)
plt.xticks(rotation=0,fontsize=15)
plt.tight_layout()

ax = plt.gca()
ax.spines.right.set_color('none')
ax.spines['top'].set_visible(False)
plt.savefig('OutputTimeseries/柱状图.png')

# 绘制每个用户在各个小时发送的消息数量的热力图
message_count_by_hour_pivot = message_count_by_hour.pivot(index='Sender', columns='Hour', values='Counts').fillna(0)
plt.figure(dpi=300,figsize=(width, 10))
sns.heatmap(message_count_by_hour_pivot, cmap='bone_r')
plt.title('消息数热力图')
plt.xlabel('Hour')
plt.tight_layout()
plt.savefig('OutputTimeseries/热力图.png')
