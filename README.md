# QQQunLogAnalyzer | QQ群记录分析工具
 Visual analysis tool for QQ group Chat log | QQ群聊天记录可视化分析工具

PC端QQ客户端支持导出聊天记录为txt文件（至少老版QQ可以导出为txt记录）
![image](Pics/导出方法.jpg)

本项目基于此文件进行分析，绘制用户的发言时间热力图与时序图。
![image](Pics/例子.png)

## QQ群聊天记录导出方法
设置-安全设置-消息记录-打开消息管理器-找到对应群聊-右键群聊选择导出消息记录-选择txt格式并保存

## 使用方法
请先安装pandas、matplotlib、seaborn等第三方库
安装完成后将导出的群聊记录置于项目根目录下，修改并运行`main.py`以生成热力图和柱状图。

## 注意
主程序中需要修改时间，txt文件，以及黑名单用户。
时间可选上周，昨天，上个月，去年，所有时间。
黑名单用户默认屏蔽了系统消息（10000,1000000），可以自定义屏蔽用户，有些Senderid是邮箱需要注意字符串。

## 说明
项目是fork的，现在自己魔改。感谢原作者的代码，我学到了很多。

## todo
- [ ] 自定义时间段总活跃程度
- [ ] 词云图
- [ ] 单独输出四张图片之一