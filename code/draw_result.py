import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
from line_profiler import profile
import os

shichen_list =  [
    "子23", "丑1", "寅3", "卯5", "辰7", "巳9",
    "午11", "未13", "申15", "酉17", "戌19", "亥21"
]  # 每小时太宽泛了，用时辰
font_path = os.path.join("font", "LatinmodernmathRegular-z8EBa.otf")  # 字体路径

def prepare_data() -> pd.DataFrame:
    """数据加载与预处理
    读取数据，原数据列名：时间、昵称、id、文本
    处理文本为空的情况
    添加数据列：小时、时辰、周几、"""
    df = pd.read_csv("OrganizedData.csv", encoding="utf-8-sig", parse_dates=["Time"])
    df["Message"] = df["Message"].fillna("")  # 处理空消息

    df["Hour"] = df["Time"].dt.hour
    # map字典映射，比apply快很多
    hour_to_shichen = {i: shichen_list[((i + 1) // 2) % 12] for i in range(24)}
    df["ShiChen"] = df["Hour"].map(hour_to_shichen)

    df["Day_of_Week"] = df["Time"].dt.dayofweek
    
    df["media_count"] = df["Message"].str.contains("[图片]", regex=False).astype(int)
    df["word_count"] = df["Message"].str.len()
    return df

def generate_statistics(df: pd.DataFrame, top_n: int) -> dict:
    """生成发送者的统计信息"""
    # 消息、图片、字数统计
    stats = df.groupby("Sender").agg(
        message_count=("Sender", "size"),
        pic_count=("media_count", "sum"),
        word_count=("word_count", "sum")
    ).sort_values("message_count", ascending=False)
    
    # 取前 top_n 个发送者
    top_n = len(stats) if len(stats) <= top_n else top_n
    top_senders = stats.head(top_n)
    senders = top_senders.index.tolist()
    
    # 各时辰消息数
    shichen_stats = (
        df[df["Sender"].isin(senders)]
        .groupby(["Sender", "ShiChen"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=shichen_list, fill_value=0)
    )
    return {
        "message_count": top_senders["message_count"],
        "pic_count": top_senders["pic_count"],
        "word_count": top_senders["word_count"],
        "shichen_stats": shichen_stats,
        "senders": senders
    }

def plot_charts(timestr: str, folder_path: str, stats: dict) -> None:
    """绘制并保存图表"""
    # 初始化字体
    font_manager.fontManager.addfont(font_path)# 应对某些奇怪的粗体字母
    plt.rcParams["font.family"] = ["sans-serif", "Latin Modern Math"]
    plt.rcParams["font.sans-serif"] = "SimHei"
    plt.rcParams["axes.unicode_minus"] = False

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), dpi=320)

    plt.suptitle(timestr, fontsize=30)  # 总标题

    # 热力图：各时辰消息分布
    sns.heatmap(
        stats["shichen_stats"],
        ax=ax1,
        linewidths=0.3,
        linecolor="grey",
        cmap="bone_r",
        cbar_kws={"location": "left",
                  "pad": 0.02  # 缩小间距（默认值为0.15）
                  },
        alpha=0.8
    )
    ax1.set_title("聊天分布", fontsize=23)
    ax1.set_xlabel("时辰（开始小时）",fontsize=15)
    ax1.yaxis.tick_right()# 将y轴标签移动到右边
    ax1.set_ylabel(None)
    ax1.tick_params(axis="x", rotation=0, labelsize=12)
    ax1.tick_params(axis="y", rotation=0, labelsize=12)
    ax1.spines["right"].set_position(("outward", 0))  # 将y轴的刻度线移动到右边

    # 柱状图：消息对比
    senders = stats["senders"]
    y_pos = range(len(senders))
    ax2.barh(y_pos, stats["message_count"], color="#CCD2CC", label="消息条数")
    ax2.plot(
        stats["word_count"] / 10, y_pos, 
        color="#976666", marker="o", markersize=10, label="字数×10"
    )
    ax2.plot(
        stats["pic_count"], y_pos,
        color="#976AA6", marker="s", markersize=10, label="发图数"
    )
    ax2.set_title("消息对比", fontsize=20)

    ax2.grid(True)
    ax2.legend(fontsize=20)
    ax2.tick_params(axis="x", rotation=0, labelsize=18)
    
    ax2.set_yticks([])
    ax2.set_ylim(len(senders)-0.5, -0.5)

    plt.tight_layout()
    # 保存图表
    os.makedirs(folder_path, exist_ok=True)
    plt.savefig(f"{folder_path}/{timestr}-水群榜.png")
    plt.close()

@profile
def draw(timestr: str, folder_path: str) -> None:
    df = prepare_data()
    stats = generate_statistics(df, 15)
    plot_charts(timestr, folder_path, stats)

if __name__ == "__main__":
    draw("test", "./")
