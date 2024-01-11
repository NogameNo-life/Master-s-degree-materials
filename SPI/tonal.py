from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

text = [
    'LaTeX обеспечивает высокое качество оформления документов',
    'LaTeX является свободным программным обеспечением',
    'LaTeX обеспечивает высокое качество оформления документов,',
    'LaTeX может быть довольно сложным для изучения',
    'LaTeX - это лучшая система компьютерной вёрстки',
    'LaTeX - моя любимая система компьютерной вёрстки',
    'LaTeX - самая прекрасная вещь на свете'
]

results = model.predict(text, k = 2)

for text_line, sentiment in zip(text, results):
    print(text_line, '->', sentiment)