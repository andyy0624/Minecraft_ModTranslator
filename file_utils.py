import json
import zipfile
import os

class JsonFile:
    def __init__(self, file_path):
        self._file_path = file_path

    def read_json_file(self, json_file_name):
        with open(json_file_name, 'r') as json_file:
            json_data = json.load(json_file)
        return json_data

    def write_json_file(self, json_data, json_file_name):
        with open(json_file_name, 'w') as json_file:
            json.dump(json_data, json_file)


class ZipJsonFile():
    def __init__(self, zip_file_path , folder_dir_in_zip=""):
        self._folder_dir_in_zip = folder_dir_in_zip
        self._zip_file_path = zip_file_path
        self._file_paths_in_zip = self._read_zip_file_paths()

    def read_json_file_in_zip(self, json_file_name):
        with zipfile.ZipFile(self._zip_file_path, 'r') as zip_file:
            json_file_path = os.path.join(self._folder_dir_in_zip, json_file_name).replace('\\', '/')
            with zip_file.open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
        return json_data

    def write_json_file_in_zip(self, json_data, json_file_name):
        with zipfile.ZipFile(self._zip_file_path, 'a') as zip_file:
            json_file_path = os.path.join(self._folder_dir_in_zip, json_file_name).replace('\\', '/')
            json_data_str = json.dumps(json_data, ensure_ascii=False, indent=4)
            zip_file.writestr(json_file_path, json_data_str)
            
            
    
    def find_target_file_paths_in_zip(self, target_file_name):
        # 過濾出指定目錄底下的所有檔案
        file_paths = [file_path for file_path in self._file_paths_in_zip if file_path.startswith(self._folder_dir_in_zip) and not file_path.endswith('/')]
        # 過濾出包含指定文件之所有路徑
        target_file_paths = [file_path for file_path in file_paths if target_file_name in file_path]
        return target_file_paths
    
    def _read_zip_file_paths(self):
        with zipfile.ZipFile(self._zip_file_path, mode="r") as zip_file:
            # 列出jar檔中的所有文件及資料夾
            file_paths_in_zip = zip_file.namelist()
        return file_paths_in_zip
