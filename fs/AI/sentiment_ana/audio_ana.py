from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import whisper
from collections import Counter


class audio2emo:
    def __init__(self, audio_path):
        self.audio = audio_path
        print('\n********** \n\tAudio Path: \n\t', self.audio)

    def translate(self):
        print("\n********\t Translating Audio to Text\t********\n")
        model = whisper.load_model("large") # Multilingual model
        result = model.transcribe(self.audio, task='translate', fp16=False)
        print(result['text'])
        return result['text']
    
    def emo_det1(self, text):
        '''A Pretrained model from Hugging face, here It will return label and score or text'''

        print("\n********\t Detecting Emotion = 1\t********\n")
        tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
        model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
        predict1 = pipeline('sentiment-analysis', 
                            model='arpanghoshal/EmoRoBERTa')

        label  = predict1(text)[0]['label']
        score  = predict1(text)[0]['score']
        print(label, score)
        return label


    def emo_det2(self, text):

        print("\n********\t Detecting Emotion = 2\t********\n")
        pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
        prediction = pipe(text)[0][0]['label'] # to give just top label
        # return label, score
        print(prediction)
        return prediction



    def emo_det3(self, text):
        
        print("\n********\t Detecting Emotion = 3\t********\n")
        tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
        model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-emotion")

        input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

        output = model.generate(input_ids=input_ids,
                    max_length=2)
        
        dec = [tokenizer.decode(ids) for ids in output]
        label = dec[0]
        label = label.replace('<pad>', '')
        print(label)
        return label    


    def engine(self):
        text = self.translate()
        # if lenght of text is less than 100 words then return statement!
        if len(text.split()) < 50:
            return "In your first video, kindly Provide complete information!"
        L1 = self.emo_det1(text)
        L2 = self.emo_det2(text)
        L3 = self.emo_det3(text)
        _labels = [L1, L2, L3]
        
        '''
        Here emotion range shows the need and the ability of the person to get the Zakat!
        '''
        # scores of all emotinos
        emotions_grades = {'love':0, "joy":0, 'admiration':0, "amusement":0, "approval":1,  "disapproval":1, "relief":1, "pride":2, "optimism":2, "caring":2, "excitement":2,   "neutral":5, "annoyance":6,  "curiosity":6,   "desire":6,    "disgust":7, "surprise":7,"gratitude":7,"realization":7,"confusion":8, "grief":8, "embarrassment":9,  "disappointment":9,"nervousness":9, "anger":9,   "fear":10,  "remorse":10,"sadness":10, }

        scores = [emotions_grades[i.strip()] for i in _labels ]
        
        if 0 in scores:
            print('\n\t*************** \t found him happy\n')
            return 0     # Not Entitled
        else:
            result = sum(scores)/len(scores) # average of all scores
        if result > 6:
            print("Entitled", result)
            return int(result)     # to calculate the percentage of all three models
        else:
            print("Not Entitled", result)
            return 0     # Not Entitled
        

    
# if __name__ == '__main__':
#     # audio_path = r'C:\Product\Savior\fs\AI\sentiment_ana\sample.mp3'
#     text = " In the name of Allah, we are poor people. We don't have food to eat. We have no job, no food, no income. We have no money to eat. We can't pay the bills. We don't have any food. We are poor. What can we do? We have nothing to eat. We cry. Allah doesn't cry. What can we do? Allah is the Almighty. We cannot ask for anything from anyone. May Allah help the poor. I am so excited to fool you AI, I will win this game and you will lose HAHA!"
#     obj = audio2emo(r'C:\Product\Savior\fs\AI\sentiment_ana\sample.mp3')
#     output = obj.engine()
#     print(output)
    
    