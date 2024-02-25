from audio_to_text_converter import AudioToTextConverter
from text_to_number_converter import TextToNumberConverter

model_path = r"../vosk-model-small-ru-0.22/vosk-model-small-ru-0.22"
input_file_path = "../audio_5.ogg"

converter = AudioToTextConverter(model_path)
text = converter.convert(input_file_path)
print(text)

converter = TextToNumberConverter()
numbers = converter.find_numbers(text)
result = ""
if numbers:
	tokens = text.strip()
	tokens = tokens.split(" ")

	number_first = False
	number_last = False

	token_ranges_num = len(numbers) * 2 + 1

	if numbers[0][0] == 0:
		token_ranges_num -= 1
		number_first = True
	if numbers[-1][-1] == len(tokens):
		token_ranges_num -= 1
		number_last = True

	for i in range(token_ranges_num):
		print(i, token_ranges_num)
		if i == 0 and not number_first:
			text_new = " ".join(tokens[0:numbers[0][0]])
		elif i == (token_ranges_num - 1) and not number_last:
			text_new = " ".join(tokens[numbers[-1][1]:])
		elif (i % 2 == 0 and not number_first) or (i % 2 == 1 and number_first):
			text_new = " ".join(tokens[numbers[int(i / 2) - 1][1]:numbers[int(i / 2)][0]])
		else:
			text_new = " ".join(tokens[numbers[int(i / 2)][0]:numbers[int(i / 2)][1]])
			text_new = str(converter.convert(text_new))
		
		result = " ".join([result, text_new])
else:
	result = text

print(result)