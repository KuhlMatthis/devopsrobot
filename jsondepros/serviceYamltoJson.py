#!/usr/bin/env python
"""
    pip3 install pyyaml
    pip3 install json
"""

import yaml
import json


depjs={}
with open("distribution.yaml", 'r') as rosfile:
    ros_yaml = yaml.safe_load(rosfile)
    #print(ros_yaml['release_platforms'])
    #print(ros_yaml['version'])
    #print(ros_yaml['type'])
    ros_yaml = ros_yaml['repositories']
    for key, value in ros_yaml.items():
        print(key+' : ')
        for key2,value2 in value.items():
            if(key2=='source'):
                depjs[key]=value2['url']
                print(' -> ' + value2['url'])
            """rosdep = value['source']
            if(rosdep['type']=='git'):
                print(rosdep['url'])
            """
with open('rospackages.json', 'w') as outfile:
        json.dump(depjs, outfile)