import basic_lang
print("\nGamo programming language interpreter version 1.0.0")
while True:
    text = input('GamoLang >> ')
    result, error = basic_lang.run('<stdin>', text)

    if error: print(error.as_string())
    else: 
        if len(result) > 0:
            print(result)