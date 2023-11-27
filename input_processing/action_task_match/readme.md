# TASKS
以task为主导关系，生成task与action关联，附加attribute的task_categories。以便后续识别，转换。

---

# RESULTS

## action_labels.json
视频段生成的action对应关系，包含具体id和name信息。

---

## mapping_dict.json

根据视频端导出的正则后的204个action为初始内容，task则根据真实protocol文本检索action关键词生成。

表示action与task的对应关系。task&action一对多，action有且仅出现一次。

以task为主导信息。


原则：
- sample, reagents不同; epi tube, tube规格没管
- 无实际动作意义的action直接赋空值
- action可多不少
- 暂时没有保留ml数
- 1+1,1&1格式文本暂且分开存储
- 一般不会出现的内容:attach, eject

> 有待修正的内容：
>
> set pipette volume :索要condition
>
> tilt cell culture plate: condition? duration? 有的有有的没有
>
> vortex: 目前视频中的内容没有需要duration的，但是protocol中存在需要duration的情况
>
> put 15ml tubes in hood: 实际两个动作，put in hood & put on rack: 先不管了
>
> incubate: 三个起始，一个终止。问题原因：cell culture incubator和incubator实体表达不一致-后续合成一个；96well plate的没有pick动作

---

## inverted_mapping_dict.json
将mapping_dict.json的key与value反转，以action为主导，如果需要索引，更方便查阅。

---

## task_category.json

以如下格式存储task与action关系数据。

    {
        "id": 33,
        "name": "Incubate",
        "action_name": [
            "put cell culture plate in incubator",
            "put cell culture plates in cell culture incubator",
            "put 96 well plate in incubator",
            "pick cell culture plate from incubator"
        ],
        "action_sequences": [
            173,
            174,
            170,
            122
        ],
        "attributes": [
            "conditioned",
            "timed"
        ]
    } 