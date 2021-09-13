import re
import json
import os

if not os.path.exists("inputs"):
	os.mkdir("inputs")
if not os.path.exists("outputs"):
	os.mkdir("outputs")
files = os.listdir("inputs")

print("Parsing files...")

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
	new_file.write("Label\tContent\n---------------------------------------------")
	for group in dict:
		for x in dict[group]:
			for y, z in x.items(): #i don't know if there's a way to do this without three goddamn levels of nesting no. twst's file formatting sucks
				if y == "serif" and "text" in z.keys() and "speaker" in z.keys():
					new_file.write("\n" + z["speaker"]["text"] + "\t" + re.sub("\n", "\n\t", z["text"]))
				elif y == "title" and "textWhite" in z.keys() and "textGold" in z.keys():
					new_file.write("\nTITLE\t" + z["textWhite"] + "\n\t(" + z["textGold"] + ")")
				elif y == "place" and "jp" in z.keys() and "en" in z.keys():
					new_file.write("\nPLACE\t" + z["jp"] + "\n\t" + z["en"])
				elif y == "balloon" and "text" in z.keys() and "speaker" in z.keys():
					new_file.write("\n" + z["speaker"] + "\t" + re.sub("\n", "\n\t", z["text"]))
	new_file.close()
	print("> Parsed " + item)

print("Finished parsing all files.")