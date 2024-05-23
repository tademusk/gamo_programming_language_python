import basic_lang

while True:
	text = input('GamoLang >> ')
	if text.strip() == "": continue
	result, error = basic_lang.run('<stdin>', text)

	if error:
		print(error.as_string())

		# print("Error")
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))