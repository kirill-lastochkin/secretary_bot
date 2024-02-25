def _test():
	converter = TextToNumberConverter()
	test_data = [
		["минус три тысячи пятьсот сорок два", -3542],
		["семь тысяч сто три", 7103],
		["сто тысяч шестьсот двенадцать", 100612],
		["четыреста пять целых шесть десятых", 405.6],
		["пятьдесят девять тысяч", 59000],
		["восемь сотен", 800],
		["две сотни", 200],
		["одна целая сто две тысячных", 1.102],
		["минус ноль целых семьдесят две сотые", -0.72],
	]
	for case in test_data:
		result = converter.convert(case[0])
		assert result == case[1] , f"{result} != {case[1]}"

	test_text = "я иду за сто сорок пять километров и семь верст"
	assert converter.find_numbers(test_text) == [[3, 6], [8, 9]]
	print("Test ok!")

class TextToNumberConverter:
	@staticmethod
	def add(count): return lambda x: x+count

	@staticmethod
	def mul(count): return lambda x: x*count

	_start_tokens = [
		[["ноль"], add(0)],
		[["один", "одна"], add(1)],
		[["два", "две"], add(2)],
		[["три"], add(3)],
		[["четыре"], add(4)],
		[["пять"], add(5)],
		[["шесть"], add(6)],
		[["семь"], add(7)],
		[["восемь"], add(8)],
		[["девять"], add(9)],
		[["десять"], add(10)],
		
		[["десятков", "десяток", "десятка"], mul(10)],
		
		[["одиннадцать"], add(11)],
		[["двенадцать"], add(12)],
		[["тринадцать"], add(13)],
		[["четырнадцать"], add(14)],
		[["пятнадцать"], add(15)],
		[["шестнадцать"], add(16)],
		[["семнадцать"], add(17)],
		[["восемнадцать"], add(18)],
		[["девятнадцать"], add(19)],
		[["двадцать"], add(20)],
		[["тридцать"], add(30)],
		[["сорок"], add(40)],
		[["пятьдесят"], add(50)],
		[["шестьдесят"], add(60)],
		[["семьдесят"], add(70)],
		[["восемьдесят"], add(80)],
		[["девяносто"], add(90)],
		[["сто"], add(100)],
		
		[["сотен", "сотни"], mul(100)],
		
		[["двести"], add(200)],
		[["триста"], add(300)],
		[["четыреста"], add(400)],
		[["пятьсот"], add(500)],
		[["шестьсот"], add(600)],
		[["семьсот"], add(700)],
		[["восемьсот"], add(800)],
		[["девятьсот"], add(900)],
		[["тысяча"], add(1000)],
		
		[["тысяч", "тысячи"], mul(1000)],
	]

	_float_type_tokens = {
		"десятых": 10,
		"десятые": 10,
		"сотых": 100,
		"сотые": 100,
		"тысячных": 1000,
		"тысячные": 1000
	}

	def _match_token(self, token):
		for tokens in self._start_tokens:
			if token in tokens[0]:
					return tokens[1]

	def find_numbers(self, text):
		text = text.strip()
		tokens = text.split(" ")
		number_indicies = []

		in_number = False

		for idx, token in enumerate(tokens):
			if self._match_token(token) or token == "минус":
				if not in_number:
					number_indicies.append([idx, idx + 1])
					in_number = True
				else:
					number_indicies[-1][1] = idx + 1
			else:
				in_number = False

		return number_indicies

	def convert(self, text):
		text = text.strip()
		try:
			tokens = text.split(" ")
			value = 0
			
			minus = False
			if tokens[0] == "минус":
				tokens = tokens[1:]
				minus = True
					
			integer_part = tokens
			float_part = None

			for separator in ("целых", "целая"):
				if separator in tokens:
					integer_part = tokens[:tokens.index(separator)]
					float_part = tokens[tokens.index(separator)+1:-1]
					float_part_type = tokens[-1]

			for token in integer_part:
				value = self._match_token(token)(value)
			
			if float_part != None:
				floatValue = 0
				for token in float_part:
					floatValue = self._match_token(token)(floatValue)
				value += floatValue / self._float_type_tokens[float_part_type]
			
			value *= -1 if minus else 1
			return value
		except Exception as e:
			print(f"Error: {e}")

if __name__ == "__main__":
    _test()