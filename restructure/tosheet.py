import re
import pandas as pd
from datetime import datetime,timedelta

def qq_txt_to_csv(file_path,banned_id_list,sd,ed):
    # 读数据
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则筛选
    pattern = r"(\d{4}-\d{2}-\d{2} \d{1,2}:\d{1,2}:\d{2}) (.+?)[\(<]([\dA-z\.@]*)[\)>]\n(.+?)\n\n"
    matches = re.findall(pattern, content)

    # 转化成dataframe格式
    data = {
        'Time': [match[0] for match in matches],
        'Sender': [match[1] for match in matches],
        'SenderID': [match[2] for match in matches],
        'Message': [match[3] for match in matches]
    }
    df = pd.DataFrame(data)

    # 删除特定用户
    for ii in range(len(banned_id_list)):
        df = df.drop(df[df['SenderID']==str(banned_id_list[ii])].index)

    # 把 'Time' 列转换为 datetime 类型
    df['Time'] = pd.to_datetime(df['Time'], format="%Y-%m-%d %H:%M:%S")

    # 筛选特定时间段
    df = df[(df['Time']>=sd)&(df['Time']<=ed)]

    # 然后我们按 'SenderID' 进行分组，并在每个组内按照时间顺序更新 'Sender' 
    df = (df.sort_values('Time').groupby('SenderID')
      .apply(lambda group: group.assign(Sender=group['Sender'].iloc[-1]), include_groups=True)
      .reset_index(drop=True))
    
    # 恢复原始的行顺序
    df = df.sort_index()

    return df

def get_last_time_range(period: str):
    now = datetime.now()
    today_weekday = now.weekday()

    if period == 'week':
        # 上周一0点
        start_date = now - timedelta(days=today_weekday + 7)
        end_data = start_date+timedelta(days=6)
        _, idnum, _ = start_date.isocalendar()
        idstr = f"第{idnum}周"
    elif period == 'month':
        # 上个月的第一天0点
        end_data = now.replace(day=1) - timedelta(days=1)
        start_date = end_data.replace(day=1)
        idstr = f"{start_date.month}"
    elif period == 'year':
        # 上年的第一天0点
        end_data = now.replace(month=1, day=1) - timedelta(days=1)
        start_date = end_data.replace(month=1,day=1)
        idstr = f"{start_date.year}"
    elif period == 'day':
        end_data = now -timedelta(days=1)
        start_date = end_data
        idstr = f"昨日"

    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_data = end_data.replace(hour=23, minute=59, second=59, microsecond=999999)

    return start_date, end_data, idstr

if __name__ == '__main__':
    file_path = r'球球的萨卡兹窝ฅ՞•ﻌ•՞ฅ.txt'  # 将此处替换为您的聊天记录文件路径
    banned_id_list=[10000,1000000,  #系统消息
                1342971950, #机械人
                ]
    sd,ed,idstr = get_last_time_range('year')

    chat_df = qq_txt_to_csv(file_path,banned_id_list,sd,ed)
    print(chat_df)
    chat_df.to_csv(r"OrganizedData.csv",encoding='utf-8-sig')
