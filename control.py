import json
import os


async def main(new_data,value_key:str,filename:str):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  # ファイルが空や壊れてたら新規辞書
    else:
        data = {}
        
    new_data = new_data[value_key]
    data[value_key] = new_data
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
async def read(filename :str):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  # ファイルが空や壊れてたら新規辞書
    
    return data