import json
from pathlib import Path

config_path = Path(__file__).resolve().parent.parent / "config.json"

# 
# Load and parse config.json y
with open(config_path, 'r') as f:
    config_data = json.load(f)

def get_course_config(course_name, mode_name):
    # Traverse the config to find the matching course and mode s
    for university in config_data['universities'].values():
        for degree_level in university.values():
            for subject in degree_level.values():
                course = subject.get(course_name)
                if course and mode_name in course:
                    return course[mode_name]
    raise ValueError('Course or mode not found in config')

def get_course_id(config, university, degree, subject, course):
    return config['universities'][university][degree][subject][course]['course_id']

def get_assistant_ids(course_name, mode_name):
    mode_config = get_course_config(course_name, mode_name)
    assistant_id = mode_config.get('assistant_id')
    if not assistant_id:
        raise ValueError('Assistant IDs not found in configuration.')
    return assistant_id
