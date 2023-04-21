from translate_utils import translator
from file_utils import ZipJsonFile
import os

class ModTranslator:
    def __init__(self, original_language, translated_language):
        self._original_language = original_language #zh_cn
        self._translated_language = translated_language #zh_tw
        self._mod_file_name = ""
        self._mod_file_path = ""
        self._translator = translator(self._original_language, self._translated_language)

    def _log(self, msg):
        print(f"「{self._mod_file_name}」：{msg}")
    
    def translate_mod(self, mod_file_path):
        self._mod_file_path = mod_file_path
        self._mod_file_name = os.path.basename(self._mod_file_path)
        
        self._log(f"正在翻譯{self._mod_file_name}...")
        
        mod_file = ZipJsonFile(self._mod_file_path)
        
        original_lang_file_name = f"{self._original_language}.json"
        translated_lang_file_name = f"{self._translated_language}.json"
        
        # 找到包含指定之原始檔、翻譯檔的所有路徑
        original_file_paths = mod_file.find_target_file_paths_in_zip(original_lang_file_name)
        translated_file_paths = mod_file.find_target_file_paths_in_zip(translated_lang_file_name)
        self._log(f"模組中共有 {len(original_file_paths)} 個{original_lang_file_name}檔案 : {original_file_paths}")  
        self._log(f"模組中共有 {len(translated_file_paths)} 個{translated_lang_file_name}檔案 : {translated_file_paths}")

        for original_file_path in original_file_paths:
            # 取得原始檔的當前目錄
            original_file_dir = os.path.dirname(original_file_path)
            
            # 建立一個檔案處理者，負責操作該模組壓縮檔中指定路徑的讀取以及寫入
            file_handler = ZipJsonFile(self._mod_file_path, original_file_dir)
            
            # 取得原始檔目錄下，翻譯檔的路徑
            translated_file_path_in_dir = file_handler.find_target_file_paths_in_zip(translated_lang_file_name)
            
            # 若當前目錄下已有翻譯檔，則略過翻譯
            if translated_file_path_in_dir:
                self._log(f"「{original_file_dir}」路徑下已有翻譯檔，略過此路徑")
                continue
            
            # 讀取原始檔
            original_json_data = file_handler.read_json_file_in_zip(original_lang_file_name)
            
            # 將語系檔轉換成目標語言
            translated_json_data = self._translator.translate_json(original_json_data)
            
            # 寫入zipfile中
            file_handler.write_json_file_in_zip(translated_json_data, translated_lang_file_name)
            self._log(f"已將{original_file_path}路徑中的{original_lang_file_name}，轉換成{translated_lang_file_name}，並儲存於{original_file_dir}")

    def translate_mods(self, mods_folder_dir):
        file_paths = os.listdir(mods_folder_dir)
        mod_file_paths = []
        for mod_file in file_paths:
            _, ext = os.path.splitext(mod_file)
            if ext == '.jar':
                mod_file_paths += [os.path.join(mods_folder_dir, mod_file)]
                
        # 逐個翻譯模組
        for mod_file_path in mod_file_paths:
            self.translate_mod(mod_file_path) 
