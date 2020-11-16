from googletrans import Translator

translate_URLS = [
    'translate.google.cn'
]

class translate_google(object):
    """docstring for translate_google"""
    def __init__(self, translate_URLS=translate_URLS):
        super(translate_google, self).__init__()
        self.translate_URLS = translate_URLS
        

    def translate(self ,input_text, source="zh-cn", target="zh-cn", translator=None):
        if translator is None:
            self.translator = Translator(service_urls=self.translate_URLS)
        else:
            self.translator = translator
        if source==target:
            if source=="en":
                return input_text
            else:
                return self.translate(self.translate(input_text,source,'en',self.translator),"en",target,self.translator)
        return self.translator.translate(input_text, src=source, dest=target).text


if __name__ == "__main__":
    input_text = "佢一啲都唔中意呢种感觉，因为佢会畀人喺安逸中沉沦。"
    trans = translate_google()
    print(trans.translate(input_text))
