from vosk import Model, KaldiRecognizer
import json
import wave
import shutil
import os
import soundfile as sf

class AudioToTextConverter:
	def __init__(self, model_path):
		self._model = Model(model_path)
		self._config_path = f"{model_path}/conf/mfcc.conf"
		self._temp_wav_file = "temp.wav"

	def convert(self, input_audio_file_path):
		self._convert_to_wav(input_audio_file_path)
		result = ''

		with wave.open(self._temp_wav_file, "rb") as wf:
			recognizer = KaldiRecognizer(self._model, self.samplerate)
			
			last_n = False

			while True:
				data = wf.readframes(self.samplerate)
				if len(data) == 0:
					break

				if recognizer.AcceptWaveform(data):
					_process_waveform(recognizer, result, last_n)

			res = json.loads(recognizer.FinalResult())
			result += f" {res['text']}"

		self._clean()

		return result

	@staticmethod
	def _process_waveform(recognizer, result, last_n):
		res = json.loads(recognizer.Result())

		if res['text'] != '':
			result += f" {res['text']}"
			last_n = False
		elif not last_n:
			result += '\n'
			last_n = True


	def _convert_to_wav(self, input_audio_file_path):
		data, samplerate = sf.read(input_audio_file_path)
		self._check_samplerate(samplerate)
		
		if input_audio_file_path.endswith(".wav"):
			shutil.copy(input_audio_file_path, self._temp_wav_file)
		elif input_audio_file_path.endswith(".ogg"):
			sf.write(self._temp_wav_file, data, samplerate)
		else:
			raise Exception("Unsupported file format")

	def _clean(self):
		if os.path.exists(self._temp_wav_file):
			os.remove(self._temp_wav_file)

	def _check_samplerate(self, samplerate):
		sample_frequency_opt = "--sample-frequency"
		with open(self._config_path) as file:
			lines = file.readlines()
			for line in lines:
				if sample_frequency_opt in line:
					idx = line.find("=") + 1
					samplerate_config = int(line[idx:])
					if samplerate == samplerate_config:
						self.samplerate = samplerate
						return True
					raise Exception(f"Samplerate in config ({self._config_path}) != samplerate of file ({samplerate_config} != {samplerate})")
		raise Exception(f"Config ({self._config_path}) doesn't contain option {sample_frequency_opt}")

def main():
	model_path = r"../vosk-model-small-ru-0.22/vosk-model-small-ru-0.22"
	input_file_path = "../audio_2.ogg"

	converter = AudioToTextConverter(model_path)
	print(converter.convert(input_file_path))


if __name__ == "__main__":
    main()
			