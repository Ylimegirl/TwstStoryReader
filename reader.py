import re
import json
import os

if not os.path.exists("inputs"):
	os.mkdir("inputs")
if not os.path.exists("outputs"):
	os.mkdir("outputs")
files = os.listdir("inputs")

def prettyJSON(file_name): # code to make prettified output of json files
	if not os.path.exists("pretty"):
		os.mkdir("pretty")
	pretty = open("pretty/" + file_name[0:file_name.find(".")] + "_pretty.json", "w")
	pretty.write(json.dumps(json.loads(parsed), indent = 4))
	pretty.close() #inb4 no i do not know how to make these not output into unicode escaped characters, sorry!!


print("Parsing files...")

for item in files:
	#grab original text
	ref = open("inputs/" + item, encoding="utf-8")
	parsed = ref.read()
	ref.close()
	
	#prettified output (for debugging/reference)
	#prettyJSON(item)
	
	dict = json.loads(parsed)#converts json to dict format
	newname = "outputs/" + item[0:item.find(".")] + "_parsed.txt"
	if os.path.exists(newname):#deletes _parsed file if it exists
		os.remove(newname)
	new_file = open(newname, "a", encoding="utf-8")
	new_file.write("TwstStoryReader by Ylimegirl v0.3.0\nhttps://github.com/Ylimegirl/TwstStoryReader")
	for group in dict:
		if group.startswith("group"):
			new_file.write("\n---------------------------------------------\nGROUP\t" + group)
			for x in dict[group]:
				for y, z in x.items(): #i don't know if there's a way to do this without three goddamn levels of nesting no. twst's file formatting sucks
					if y == "serif" and "text" in z.keys() and "speaker" in z.keys():# handles main dialogue (serifs)
						if "visible" in z["speaker"].keys():
							if z["speaker"]["visible"] == False:# handles serifs w/o a speaker
								new_file.write("\n[N/A]\t" + re.sub("\n", "\n\t", z["text"]))
						else:
							new_file.write("\n" + z["speaker"]["text"] + "\t" + re.sub("\n", "\n\t", z["text"]))
					elif y == "serif" and not "text" in z.keys(): # skips serifs without text
						pass
					elif y == "choice": # handles choices
						new_file.write("\nCHOICE\t1: " + re.sub("\n", "\n\t", z[0]["text"]) + " (GOTO: " + z[0]["goTo"] + ")")
						new_file.write("\nCHOICE\t2: " + re.sub("\n", "\n\t", z[1]["text"]) + " (GOTO: " + z[1]["goTo"] + ")")
					elif y == "goTo":
						new_file.write("\nGOTO\t" + z["goTo"]) # handles pathing
					elif y == "title" and "textWhite" in z.keys() and "textGold" in z.keys(): # handles titles
						if "personal" in z.keys(): # handles titles for personal stories
							new_file.write("\nTITLE\t" + z["personal"]["rarity"] + " " + z["textGold"] + "\n\t" + z["personal"]["anotherName"] + ": " + z["textWhite"])
						else: # handles other titles
							new_file.write("\nTITLE\t" + z["textWhite"] + "\n\t" + z["textGold"])
					elif y == "title" and not "textWhite" in z.keys(): # skips titles without text
						pass
					elif y == "text" and "text" in z.keys(): # handles generic "text" content
						new_file.write("\nTEXT\t" + re.sub("\n", "\n\t", z["text"]))
					elif y == "place" and "jp" in z.keys() and "en" in z.keys(): # handles place titles
						new_file.write("\nPLACE\t" + z["jp"] + "\n\t" + z["en"])
					elif y == "place" and not "jpn" in z.keys(): # skips places without text
						pass
					elif y == "telop" and "text" in z.keys(): #handles "telops"
						new_file.write("\nTELOP\t" + z["text"])
					elif y == "telop" and not "text" in z.keys(): # skips telops without text
						pass
					elif y == "balloon" and "text" in z.keys() and "speaker" in z.keys(): # handles speech balloons (in rhythmics and battle cutscenes)
						new_file.write("\n" + z["speaker"] + "\t" + re.sub("\n", "\n\t", z["text"]))
					elif y == "balloon" and not "text" in z.keys(): # skips balloons without text
						pass
					elif y == "live2d" or y == "moveCamera" or y == "systemUI" or y == "run" or y == "bgm" or y == "advBgOperator" or y == "touch" or y == "wait" or y == "zoomCamera" or y == "se" or y == "curtain" or y == "spine" or y == "spineCharacter" or y == "sd" or y == "spfx" or y == "shakeCamera" or y == "voice" or y == "transition": # skips a bunch of boring animation/visual logicistical code
						pass
					else: # for debugging mostly and to catch types i missed
						new_file.write("\n" + y + "\t(no code to handle this type of object yet, sorry! --Ylime)")
		elif group.startswith("voice"):
			new_file.write("\n" + group + "\t" + dict[group]["serif"])#voice line jasons are so simple bless
	new_file.close()
	print("> Parsed " + item)

print("Finished parsing all files.")