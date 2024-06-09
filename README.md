# QunFriends
 Visual analysis tool for QQ group Chat log | QQ群聊天记录可视化分析工具

大部分版本的PC端QQ客户端支持导出聊天记录为txt文件，本项目基于此文件进行分析，为每个用户绘制词云图，并绘制用户的发言时间热力图。
![image](Pics/星海旅人·阿尔法_wordcloud.png)
![image](Pics/Snipaste_2023-07-29_18-28-10.jpg)

## QQ群聊天记录导出方法
设置-安全设置-消息记录-打开消息管理器-找到对应群聊-右键群聊选择导出消息记录-选择txt格式并保存

## 使用方法
请先安装pandas、matplotlib、wordcloud、jieba等第三方库
安装完成后将导出的群聊记录置于项目根目录下，改名为“聊天记录导出.txt”
后运行Scripts文件夹中的`toSheet.py`以将txt文件转化为规范化的`OrganizedData.csv`，这个文件以utf-8-sig编码并可以在大多数版本的excsl中直接查看、修改和保存。
随后，运行`Scripts\forTimeseries.py`和`Scripts\forWordcloud.py`以生成热力图和词云图。
