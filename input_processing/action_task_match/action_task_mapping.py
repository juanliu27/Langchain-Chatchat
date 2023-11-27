import json
import os

#提取action_list对应的id
def get_id_by_name(action_list, dictionary):
    result_dict = []
    for action in action_list:
        for key, value in dictionary.items():
            if value['name'] == action:
                result_dict.append(value['id'])
    return result_dict

condition_required = ["Adjust the pipette volume to","Mix by vortexing","Incubate"]
duration_required = ["water bath the reagents","centrifuge the reagents in the tube","Mix by vortexing","Incubate"]

#提取action列表
with open('input_processing/action_task_match/action_labels.json', 'r') as file:
    data = json.load(file)

target_keys = ['id','name']
action_dict = {index: {key: category[key] for key in target_keys if key in category} for index, category in enumerate(data['action_categories'])}

#提取task-action的mapping关系
with open('input_processing/action_task_match/mapping_dict.json', 'r') as mfile:
    mapping_dict = json.load(mfile)

#转化为action-task的mapping,便于查看
inverted_dict = {value: key for key, values in mapping_dict.items() for value in values}
with open('input_processing/action_task_match/inverted_mapping_dict.json', 'w') as json_file:
    json.dump(inverted_dict, json_file, indent=4)

# "task_categories": [
#     {
#         "id": 0,
#         "name": "task name",
#         "action_name":[]
#         "action_sequences": [],
#         "attributes": []
#     }
# ]

#生成如上格式的task_category字典
task_json = []
for index, (key, value) in enumerate(mapping_dict.items()):
    task_list = {}
    task_list['id'] = index
    task_list['name'] = key
    task_list['action_name'] = value
    task_list['action_sequences'] = get_id_by_name(value,action_dict)
    task_list['attributes']=[]
    if key in condition_required: task_list['attributes'].append('conditioned')
    if key in duration_required: task_list['attributes'].append('timed')
    task_json.append(task_list)


#存储task_category
with open('input_processing/action_task_match/task_category.json', 'w') as json_file:
    json.dump({"task_categories":task_json}, json_file, indent=4)