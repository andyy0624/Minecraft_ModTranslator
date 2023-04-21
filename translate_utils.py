import opencc as cc
import requests

def translator(source_language, target_language):
    opencc_supported = {"zh_cn": "s", "zh_tw": "t"}
    if((source_language in opencc_supported) and (target_language in opencc_supported)):
        conversion_type = f"{opencc_supported[source_language]}2{opencc_supported[target_language]}"
        return OpenCCTranslator(conversion_type)
    
    raise Exception('Unsupported translator type')

class _Translator:
    def translate_json(self, source_json_file):
        translation_json_file = {key: self.translate(text) for key, text in source_json_file.items()}
        return translation_json_file

class OpenCCTranslator(_Translator):
    def __init__(self, conversion_type):
        if conversion_type not in ['s2t', 't2s', 's2tw', 'tw2s', 's2hk', 'hk2s']:
            raise Exception('Unsupported conversion type')

        self._converter = cc.OpenCC(f'{conversion_type}.json')

    def translate(self, text):
        translation = self._converter.convert(text)
        return translation
