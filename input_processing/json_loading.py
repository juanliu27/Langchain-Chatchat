import json

#时间戳检查的列表-set
time_indentifier_list=set(['incubate','centrifuge','beads','dry','prewarm','bath',\
                        'block','boil','store','resuspend','react','spin','rotate'])

'''
    将读取的txt格式的json文本转换为json格式，提取对应的内容。
    对应的json格式为：

'''


def json_to_action(txt: str):
    #print('json_to_action 调用成功')
    # 识别condition内容
    def process_text_list(action):
        # 输出提示信息
        user_input = input('please write the condition required in the task: "{}": '.format(action['task_name']))
        action['condition'] == user_input
        print('the step will be transformed into:'+ action['task_name']+ ''+user_input)

    # 对重复内容进行筛选
    def merge_continuous_duplicates(action_list):
        
        current_id = action_list[0]['task_id']
        count = 1
        seqence_included_list = []

        for i in range(1, len(action_list)):
            if action_list[i]['task_id'] == current_id:
                count += 1
            else:
                if count > 1:
                    action_list[i]['repeated']=(' for {} times'.format(count))
                    seqence_included_list.append(action_list[i])
                else:
                    seqence_included_list.append(action_list[i])
                current_id = action_list[i]['task_id']
                count = 1

        # 处理最后一个元素ss
        if count > 1:
            action_list[i]['repeated']=(' for {} times'.format(count))
            seqence_included_list.append(action_list[i])
        else:
            seqence_included_list.append(action_list[i])
        
        return seqence_included_list

    # 具体函数内容
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

    #print('new_action_list 创建成功')

    #频率添加
    sequenced_list = merge_continuous_duplicates(new_action_list)

    #print(sequenced_list)

    timed_list = []

    for i in range (len(sequenced_list)): 
        end_action_index=[]
        action = sequenced_list[i]
        exit_outer_loop = False  # 标志变量，表示是否要跳出外层循环

        # condition的输入如果继续用ui页面就需要重新调整，如果终端就可以。暂且不改。      
        # if 'conditioned' in action['attributes']:      
        #   process_text_list(action)    
        
        # duration的计算      
        if 'timed' in action['attributes']:        
            if action ['category_id'] == action['action_sequences'][0]:
                for j in range(i,len(sequenced_list)):
                    while j not in end_action_index: #先进先出，出后删除    
                        if sequenced_list[j]['category_id'] == action['action_sequences'][-1]:
                            stop_time = float(sequenced_list[j]['terminal_second'])          
                            end_action_index.append(j)
                            exit_outer_loop = True  # 设置标志变量为True，表示要跳出外层循环
                            break
                    if exit_outer_loop: break 
                            
                duration_sec = stop_time - float(action['initial_second'])
                #添加duration
                if duration_sec > 60:          
                    duration_min=int(duration_sec/60)          
                    action['duration']=' for '+ str(int(duration_min))+' minutes. '      
                else:          
                    action['duration']=' for '+ str(int(duration_sec))+' seconds. '
        if i not in end_action_index:
            timed_list.append(action)
    #print('timed_list 创建成功')

    # 转换成list
    final_text=[]
    for action in timed_list:
        text = ''
        text += action['task_name']
        text += action.get('repeated', '')
        text += action.get('duration', '')
        text += action.get('condition', '')
        final_text.append(text)

    #print (final_text)

    return str(final_text)

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