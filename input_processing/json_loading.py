import json

#时间戳检查的列表-set
time_indentifier_list=set(['incubate','centrifuge','beads','dry','prewarm','bath',\
                        'block','boil','store','resuspend','react','spin','rotate'])

'''
    将读取的txt格式的json文本转换为json格式，提取对应的内容。
    对应的json格式为：

'''

def json_to_action(txt: str):
    
    with open('input_processing/action_task_match/task_category.json', 'r') as file:
        task_category = json.load(file)

    json_data = json.loads(txt)
    #时间戳检查的列表-set

    input_text=[]
    new_action_list=[]

    # 创建一个字典，将categories列表中的id与name关联起来
    category_mapping = {category["id"]: category["name"] for category in json_data["action_categories"]}

    # 将actions列表中的category_id映射为对应的name
    for action in json_data["actions"]:
        action["action_text"] = category_mapping.get(action["category_id"], "Unknown")
        for task in task_category['task_categories']:
            if action["category_id"] in task['action_sequences']:
                action['task_id'] = task['id']
                action['task_name'] = task['name']
                action['attributes'] = task['attributes']
                # if action['category_id'] == task['action_sequences'][0]:
                #     action['duration'] =='start'
                # if action['category_id'] == task['action_sequences'][-1]:
                #     action['duration'] =='end'

    #创建的新action_dict
    new_action_list = json_data['actions']

    # 识别condition内容
    def process_text_list(action):
        # 输出提示信息
        user_input = input('please write the condition required in the task: "{}": '.format(action['task_name']))
        action['other'] == user_input
        print('the step will be transformed into:'+ action['task_name']+ ''+user_input)

    for i in range ( len(new_action_list)): 
        action = new_action_list[i]
    
        # condition的输入如果继续用ui页面就需要重新调整，如果终端就可以。暂且不改。      
        # if 'conditioned' in action['attributes']:      
        # process_text_list(action)    
        
        # duration的计算      
        if 'timed' in action['attributes']:        
            if action ['category_id'] == action['action_sequences'][0]:
                num=0          
                for j in range(i,len(new_action_list)):
                    following_action = new_action_list[j]        
                    if following_action['category_id'] == action['action_sequences'][-1]:            
                        num+=1
                        stop_time = float(following_action['terminal_second'])          
                        del new_action_list[j]        
                    while num == 1: break
                duration_sec = stop_time - float(action['initial_second'])      
                if duration_sec > 60:          
                    duration_min=int(duration_sec/60)          
                    action['other']=' for '+ str(int(duration_min))+' minutes. '      
                else:          
                    action['other']=' for '+ str(int(duration_sec))+' seconds. '          

    # 对name进行识别
    # for action in json_data['actions']:
    #     判断时间是否需要获取
    #     if time_indentifier_list.intersection(action['action_text'].split()):
    #         时间可以获取到
    #         duration_sec=int(float(action['terminal_second'])-float(action['initial_second']))
    #         if duration_sec > 60:
    #             duration_min=int(duration_sec/60)
    #             action=action['action_text']+' for '+ str(int(duration_min))+' minutes. '
    #         else:
    #             action=action['action_text']+' for '+ str(int(duration_sec))+' seconds. '
    #         input_text.append(action)
    #     else:
    #         input_text.append(action['action_text'])
    
    # return str(input_text)

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