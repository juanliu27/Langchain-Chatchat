import json

#时间戳检查的列表-set
time_indentifier_list=set(['incubate','centrifuge','beads','dry','prewarm','bath',\
                        'block','boil','store','resuspend','react','spin','rotate'])

'''
    将读取的txt格式的json文本转换为json格式，提取对应的内容。
    对应的json格式为：

'''


def input_json_read(txt: str):
    
    json_data = json.loads(txt)
    #时间戳检查的列表-set
    time_indentifier_list=set(['incubate','centrifuge','beads','dry','prewarm','bath',\
                        'block','boil','store','resuspend','react','spin','rotate'])
    input_text=[]

    # 创建一个字典，将categories列表中的id与name关联起来
    category_mapping = {category["id"]: category["name"] for category in json_data["categories"]}

    # 将actions列表中的category_id映射为对应的name
    for action in json_data["actions"]:
        action["action_text"] = category_mapping.get(action["category_id"], "Unknown")

    # 对name进行识别
    for action in json_data['actions']:
        #判断时间是否需要获取
        if time_indentifier_list.intersection(action['action_text'].split()):
            #时间可以获取到
            duration_sec=int(float(action['terminal_second'])-float(action['initial_second']))
            if duration_sec > 60:
                duration_min=int(duration_sec/60)
                action=action['action_text']+' for '+ str(int(duration_min))+' minutes. '
            else:
                action=action['action_text']+' for '+ str(int(duration_sec))+' seconds. '
            input_text.append(action)
        else:
            input_text.append(action['action_text'])
    
    return str(input_text)

'''
最后输出-task+condition&duration

形成一个dict: action_id-(非零)task-timestamp起止-attribute['','']-task[]

生成新list:
    falsefalse: 正常task-且统计次数
    duration true:
        识别duration [0]: 找最先的task[-1]的action_id, 找timestamp-end
        添加 for x sec/min
    condition true:
        进行condition索要
'''

'''
condition与duration多次连续出现: 

    duration-分开写
    condition-fortimes有

'''

'''
model —> action -> task -> count task, 
'''