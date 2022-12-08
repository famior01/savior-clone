from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from transformers import AutoTokenizer, AutoModelWithLMHead
import whisper
from scipy import stats
from collections import Counter


class audio2emo:
    def __init__(self, audio_path) -> None:
        self.audio = audio_path

    def translate(self, audio):
        model = whisper.load_model("medium")
        result = model.transcribe(audio, task='translate', fp16=False)
        return result['text']
    
    def emo_det1(self, text):
        '''A Pretrained model from Hugging face, here It will return label and score or text'''

        tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
        model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
        predict1 = pipeline('sentiment-analysis', 
                            model='arpanghoshal/EmoRoBERTa')

        label  = predict1(text)[0]['label']
        # score  = predict1(text)[0]['score']
        return label



    def emo_det2(self, text):
        pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
        prediction = pipe(text)[0][0]['label'] # to give just top label
        # return label, score
        return prediction


    def emo_det3(self, text):
        
        tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
        model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")

        input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

        output = model.generate(input_ids=input_ids,
                    max_length=2)
        
        dec = [tokenizer.decode(ids) for ids in output]
        label = dec[0]
        return label    

    def engine(self):
        text = self.translate(self.audio)
        L1 = self.emo_det1(text)
        L2 = self.emo_det2(text)
        L3 = self.emo_det3(text)
        _labels = [L1, L2, L3]

        # if there is mode then show it, else return full list
        ls = Counter(_labels).most_common()
        if ls[0][1] >1:
            return Counter(ls).most_common(1) # return most common
        else:
            return Counter(ls).most_common()

    
if __name__ == '__main__':
    audio_path = './content/sample.mp3'
    obj = audio2emo(audio_path=audio_path)
    output = obj.engine()
    print(output)