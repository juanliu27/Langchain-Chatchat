## action_task_category
    根据视频端导出的正则后的204个action为初始内容，task则根据真实protocol文本检索action关键词生成。
    表示action与task的对应关系
    以task为主导信息

    原则：
    - sample, reagents不同
    - task&action一对多，action有且仅出现一次
    - 无实际动作意义的action直接赋空值
    - action可多不少

