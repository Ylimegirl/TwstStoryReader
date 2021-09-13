import re
import json
import os
if not os.path.exists("inputs"):
	os.mkdir("inputs")
if not os.path.exists("outputs"):
	os.mkdir("outputs")
files = os.listdir("inputs")

for item in files:
	#grab original text
	ref = open("inputs/" + item, encoding="utf-8")
	parsed = ref.read()
	ref.close()
	
	dict = json.loads(parsed)#converts json to dict format
	newname = "outputs/" + item[0:item.find(".")] + "_parsed.txt"
	if os.path.exists(newname):#deletes _parsed file if it exists
		os.remove(newname)
	new_file = open(newname, "a", encoding="utf-8")
	for group in dict:
		for x in dict[group]:
			for y, z in x.items(): #i don't know if there's a way to do this without three goddamn levels of nesting no. twst's file formatting sucks
				if y == "serif" and "text" in z.keys() and "speaker" in z.keys():
					new_file.write(z["speaker"]["text"] + "\t" + re.sub("\n", "\n\t", z["text"]) + "\n")
				elif y == "title" and "textWhite" in z.keys() and "textGold" in z.keys():
					new_file.write("TITLE\t" + z["textWhite"] + "\n\t(" + z["textGold"] + ")\n")
				elif y == "place" and "jp" in z.keys() and "en" in z.keys():
					new_file.write("PLACE\t" + z["jp"] + "\n\t" + z["en"] + "\n")
				elif y == "balloon" and "text" in z.keys() and "speaker" in z.keys():
					new_file.write(z["speaker"] + "\t" + re.sub("\n", "\n\t", z["text"]) + "\n")
	new_file.close()
	print("Parsed " + item + ".")
print("\nFinished parsing all files.")