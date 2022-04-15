class TextStats:
    number_of_lines = 0
    number_of_words = 0
    number_of_noalpha = 0

    def __init__(self, text):
        self.compute(text)

    def compute(self, text):
        self.number_of_lines = len(text.split('\n'))
        words = text.split()
        self.number_of_words = len(words)
        temp = 0
        for w in words:
            if not w.isalnum():
                temp += 1
        self.number_of_noalpha = temp

    def show(self):
        print(f'lines: {self.number_of_lines},\nwords: {self.number_of_words},\nnonalpha: {self.number_of_noalpha},')
