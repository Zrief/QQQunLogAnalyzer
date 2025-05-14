from tosheet import qq_txt_to_csv, get_last_time_range
from draw_result import draw
import os

# 聊天记录目录
namelist = ['低研会官服助战交流群1', "球球被窝"]
for name in namelist:
    file_path = name + '.txt'

    folder_path = f'./{name}'  # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夹 {folder_path} 已创建。")

    # 屏蔽
    banned_id_list = [
        10000,
        1000000,  #系统消息
        1342971950  #机械人
    ]

    # 上周，上上周（比如说上周忘了出图时用），上个月，去年，昨天
    timerange = 'all'  # lastweek, lastlastweek, lastmonth, lastyear, yesterday, all

    # 整理成csv，排除特定用户，指定时间段
    sd, ed, idstr = get_last_time_range(timerange)
    chat_df = qq_txt_to_csv(file_path, banned_id_list, sd, ed)
    chat_df.to_csv(r"OrganizedData.csv", encoding='utf-8-sig')

    # 画图
    draw(idstr, folder_path)
