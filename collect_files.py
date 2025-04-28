#!/usr/bin/env python3
import os
import shutil
import sys
from argparse import ArgumentParser

def make_unique_name(target_dir, original_name):
    name_part, extension = os.path.splitext(original_name)
    number = 1
    result_name = original_name
    
    while os.path.exists(os.path.join(target_dir, result_name)):
        result_name = name_part + str(number) + extension
        number += 1
    
    return result_name

def gather_files(source, destination, depth_limit=None):
    if not os.path.isdir(source):
        sys.stderr.write("Error: Source directory missing: " + source + "\n")
        return False
    
    os.makedirs(destination, exist_ok=True)
    
    for current_dir, _, files in os.walk(source):
        depth = current_dir[len(os.path.abspath(source)):].count(os.sep)
        
        if depth_limit is not None and depth > depth_limit:
            continue
        
        for file in files:
            src = os.path.join(current_dir, file)
            dst_name = make_unique_name(destination, file)
            dst = os.path.join(destination, dst_name)
            
            try:
                shutil.copy2(src, dst)
            except Exception as e:
                sys.stderr.write("Copy failed for " + src + ": " + str(e) + "\n")
    
    return True

def get_args():
    parser = ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('destination')
    parser.add_argument('--max-depth', type=int)
    return parser.parse_args()

def execute():
    params = get_args()
    
    if not gather_files(params.source, params.destination, params.max_depth):
        sys.exit(1)

if name == 'main':
    execute()