from tosheet import qq_txt_to_csv,get_last_time_range
from draw_result import draw

file_path = r'球球的萨卡兹窝ฅ՞•ﻌ•՞ฅ.txt'  # 将此处替换为您的聊天记录文件路径

banned_id_list=[10000,1000000,  #系统消息
            1342971950, #机械人
            ]

timerange = 'week' # day,week,month,year



# 整理成csv，排除特定用户，指定时间段
sd,ed,idstr = get_last_time_range(timerange)
chat_df = qq_txt_to_csv(file_path,banned_id_list,sd,ed)
chat_df.to_csv(r"OrganizedData.csv",encoding='utf-8-sig')

# 画图
draw(idstr)