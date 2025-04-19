import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import os


def draw(timestr, folder_path):
    # 创建OutputTimeseries文件夹，如果不存在
    if not os.path.exists("输出图片"):
        os.makedirs("输出图片")
    # 导入数据
    df = pd.read_csv("OrganizedData.csv", encoding="utf-8-sig")

    # 将 'Time' 列转换为 datetime 类型
    df["Time"] = pd.to_datetime(df["Time"])

    # 创建一个新的列 'Hour'，表示每条信息发送的小时
    df["Hour"] = df["Time"].dt.hour

    # 每小时太宽泛了，用时辰
    sclist = [
        "子23",
        "丑1",
        "寅3",
        "卯5",
        "辰7",
        "巳9",
        "午11",
        "未13",
        "申15",
        "酉17",
        "戌19",
        "亥21",
    ]

    df["ShiChen"] = df["Hour"].apply(lambda x: sclist[x % 23 // 2])

    # 这个没用到
    # 创建一个新的列 'Day_of_Week'，表示每条信息发送的是一周中的哪一天
    df['Day_of_Week'] = df['Time'].dt.dayofweek
    print(df)

    # 消息次数
    message_count = df["Sender"].value_counts()

    # 图片次数
    df["media_count"] = df["Message"].str.contains("[图片]", regex=False).astype(int)
    pic_count = df.groupby("Sender")["media_count"].sum()

    # 统计每条消息的总字数
    df["word_count"] = df["Message"].str.len()
    word_count = df.groupby("Sender")["word_count"].sum()

    # 统计在每个时辰的消息数量
    message_count_by_shichen = (
        df.groupby(["Sender", "ShiChen"]).size().reset_index(name="Counts")
    )

    # 如果sender数量大于15，则只展示前15个
    num = 15
    # if len(message_count) < num:
    num = min(len(message_count), num)
    top_senders = message_count.index[:num]  # 前n个
    message_count = message_count.loc[top_senders]  # 前n个的次数
    word_count = word_count.loc[top_senders]  # 前n个的字数
    pic_count = pic_count.loc[top_senders]  # 前n个的图片数

    message_count_by_shichen = message_count_by_shichen[
        message_count_by_shichen["Sender"].isin(top_senders)
    ]  # 时辰

    top_index = [ii for ii in range(len(message_count))]  # 前n个的数字索引

    #应对某些奇怪的粗体字母
    font_manager.fontManager.addfont(r"font\LatinmodernmathRegular-z8EBa.otf")
    plt.rcParams["font.family"] = ["sans-serif", "Latin Modern Math"]
    plt.rcParams["font.sans-serif"] = "SimHei"  # 显示中文
    plt.rcParams["axes.unicode_minus"] = False  # 显示负号

    # 根据时间范围确定图的宽度
    time_range = df["Time"].max() - df["Time"].min()

    # 不知道理由，不理解当时的想法，反正效果还行
    width = max(10, time_range.days / 30)  # 每30天增加1个单位的宽度
    barwidth = len(message_count) / 2  # 柱状图宽度

    plt.figure(dpi=300, figsize=(max(barwidth, 10) + width, 10))


    plt.suptitle(timestr, fontsize=30)# 总标题

    # 柱状图
    ax = plt.subplot(2, 2, 2)
    plt.grid()
    message_count = pd.DataFrame(message_count)

    sns.barplot(
        y="Sender", x="count", data=message_count, color="#CCD2CC", label="消息条数"
    )
    plt.plot(
        word_count.values / 10,
        top_index,
        color="#976666",
        label="总字数/10",
        marker="o",
        markersize=5,
    )
    plt.plot(
        pic_count.values,
        top_index,
        color="#976AA6",
        label="发图数",
        marker="s",
        markersize=5,
    )

    plt.title(f"消息对比", fontsize=20)
    plt.xticks(rotation=0, fontsize=18)
    plt.xlabel("数量")

    plt.yticks([])
    plt.ylabel(None)
    ax.set_ylim([14.5, -0.5])

    plt.tight_layout()
    ax = plt.gca()
    ax.spines.right.set_color("none")
    ax.spines["top"].set_visible(False)
    plt.legend(fontsize=20)

    # 热力图
    message_count_by_shichen_pivot = (
        message_count_by_shichen.pivot_table(
            index="Sender",
            columns="ShiChen",
            values="Counts",
        )
        .fillna(0)
        .reindex(columns=sclist)
        .reindex(index=message_count.index[top_index])
    )

    plt.subplot(2, 2, 1)

    ax = sns.heatmap(
        message_count_by_shichen_pivot,
        linewidths=0.3,
        linecolor="grey",
        cmap="bone_r",
        cbar_kws={"location": "left"},
    )

    # 将y轴标签移动到右边
    ax.yaxis.set_ticks_position("right")
    ax.yaxis.set_label_position("right")
    ax.spines["right"].set_position(("outward", 0))  # 将y轴的刻度线移动到右边

    plt.title(f"聊天分布", fontsize=23)
    plt.xlabel("时辰（开始小时）")
    plt.ylabel(None)

    ax = plt.subplot(2, 2, 3)



    plt.tight_layout()
    plt.savefig(f"{folder_path}/{timestr}-水群榜.png")
    # plt.show()


if __name__ == "__main__":
    draw("test", "./")
