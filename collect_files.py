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
        if extension:
            result_name = f"{name_part}_{number}{extension}"
        else:
            result_name = f"{name_part}_{number}"
        number += 1
    
    return result_name

def gather_files(source, destination, depth_limit=None):
    if not os.path.isdir(source):
        sys.stderr.write(f"Error: Source directory missing: {source}\n")
        return False
    
    os.makedirs(destination, exist_ok=True)
    
    for root, _, files in os.walk(source):
        current_depth = root[len(os.path.abspath(source)):].count(os.sep)
        
        if depth_limit is not None and current_depth > depth_limit:
            continue
        
        for file in files:
            src_path = os.path.join(root, file)
            dst_name = make_unique_name(destination, file)
            dst_path = os.path.join(destination, dst_name)
            
            try:
                shutil.copy2(src_path, dst_path)
            except Exception as e:
                sys.stderr.write(f"Copy failed for {src_path}: {str(e)}\n")
    
    return True

def main():
    parser = ArgumentParser()
    parser.add_argument('source', help="Input directory")
    parser.add_argument('destination', help="Output directory")
    parser.add_argument('--max-depth', type=int, help="Maximum depth level")
    args = parser.parse_args()
    
    if not gather_files(args.source, args.destination, args.max_depth):
        sys.exit(1)

if __name__ == '__main__':
    main()
