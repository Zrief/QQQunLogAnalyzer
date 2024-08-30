import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def draw(timestr):
    # 创建OutputTimeseries文件夹，如果不存在
    if not os.path.exists('输出图片'):
        os.makedirs('输出图片')
    # 导入数据
    df = pd.read_csv('OrganizedData.csv', encoding='utf-8-sig')


    # 将 'Time' 列转换为 datetime 类型
    df['Time'] = pd.to_datetime(df['Time'])

    # 创建一个新的列 'Hour'，表示每条信息发送的小时
    df['Hour'] = df['Time'].dt.hour

    # 每小时太宽泛了，用时辰
    sclist = ["子23", "丑1", "寅3", "卯5", "辰7", "巳9","午11", "未13", "申15", "酉17", "戌19", "亥21"]
    df['ShiChen'] = df['Hour'].apply(lambda x:sclist[x%23//2])

    # # 这个没用到
    # # 创建一个新的列 'Day_of_Week'，表示每条信息发送的是一周中的哪一天
    # df['Day_of_Week'] = df['Time'].dt.dayofweek

    # 消息次数
    message_count = df['Sender'].value_counts()

    # 图片次数
    df['media_count'] = df['Message'].str.contains('[图片]', regex=False).astype(int)
    pic_count =df.groupby('Sender')['media_count'].sum()
    
    # 统计每条消息的总字数
    df['word_count'] = df['Message'].str.len()
    word_count = df.groupby('Sender')['word_count'].sum()

    # 统计每个用户在各个小时发送的消息数量
    message_count_by_hour = df.groupby(['Sender', 'Hour']).size().reset_index(name='Counts')

    # 统计在每个时辰的消息数量
    message_count_by_shichen = df.groupby(['Sender', 'ShiChen']).size().reset_index(name='Counts')

    # 如果sender数量大于15，则只展示前15个
    num = 15
    # if len(message_count) < num:
    num = min(len(message_count),num)
    top_senders = message_count.index[:num] # 前n个
    message_count = message_count.loc[top_senders] # 前n个的次数
    word_count = word_count.loc[top_senders] # 前n个的字数
    pic_count = pic_count.loc[top_senders] # 前n个的图片数
    message_count_by_hour = message_count_by_hour[message_count_by_hour['Sender'].isin(top_senders)] # 前n个分时
    message_count_by_shichen = message_count_by_shichen[message_count_by_shichen['Sender'].isin(top_senders)] # 时辰
    top_index = [ii for ii in range(len(message_count))] #前n个的数字索引


    plt.rcParams['font.sans-serif'] = ['Simhei']  #显示中文
    plt.rcParams['axes.unicode_minus'] = False    #显示负号

    # 根据时间范围确定图的宽度
    time_range = df['Time'].max() - df['Time'].min()

    # 不知道理由，不理解当时的想法，反正效果还行
    width = max(10, time_range.days / 30)  # 每30天增加1个单位的宽度
    barwidth = len(message_count)/2 # 柱状图宽度


    # 柱状图
    plt.figure(dpi=200,figsize=(max(barwidth,10), 10))
    plt.grid()
    message_count = pd.DataFrame(message_count)

    sns.barplot(y="Sender", x="count",data=message_count,color='#CCD2CC',label='消息条数')
    plt.plot(word_count.values/10,top_index,color='#976666',label='相对总字数',marker='o',markersize=5)
    plt.plot(pic_count.values,top_index,color='#976AA6',label='发图数',marker='s',markersize=5)

    plt.title(f"水群榜({timestr})",fontsize=18)
    plt.xticks(rotation=0,fontsize=15)
    plt.tight_layout()
    ax = plt.gca()
    ax.spines.right.set_color('none')
    ax.spines['top'].set_visible(False)
    plt.legend()
    plt.savefig(f'输出图片/{timestr}-柱状图.png')

    # 热力图
    message_count_by_shichen_pivot = message_count_by_shichen.pivot_table(index='Sender',columns='ShiChen',values='Counts',).fillna(0).reindex(columns=sclist).reindex(index=message_count.index[top_index])


    plt.figure(dpi=200,figsize=(width, 10))

    ax = sns.heatmap(message_count_by_shichen_pivot,linewidths=0.3, linecolor="grey",cmap='bone_r')
    plt.savefig(f'输出图片/{timestr}-时辰图.png')
    plt.title(f'聊天分布（{timestr}）',fontsize=20)
    plt.xlabel('时辰（开始小时）')
    plt.ylabel('群友')

    plt.tight_layout()
    plt.savefig(f'输出图片/{timestr}-时辰图.png')
