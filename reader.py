import os
import json
from replacer import nameTrans
from replacer import formatDialogue
from replacer import replaceNewLine
from pretty import prettyJSON

if not os.path.exists("inputs"):
	os.mkdir("inputs")
if not os.path.exists("outputs"):
	os.mkdir("outputs")

files = os.listdir("inputs")
verNum = "0.3.3"

print("Parsing files...")

for item in files:
	#grab original text
	ref = open("inputs/" + item, encoding="utf-8")
	parsed = ref.read()
	ref.close()
	
	#prettified output (for debugging/reference)
	#prettyJSON(parsed, item)
	
	dict = json.loads(parsed)#converts json to dict format
	newname = "outputs/" + item[0:item.find(".")] + "_parsed.txt"
	if os.path.exists(newname):#deletes _parsed file if it already exists
		os.remove(newname)
	new_file = open(newname, "a", encoding="utf-8")
	for group in dict:
		if group.startswith("voice"):
			new_file.write(group + "\t" + dict[group]["serif"] + "\n")#voice line jasons are so simple. bless
		elif group.startswith("group"):
			new_file.write("---------------------------------------------\n[GROUP]\t" + group + "\n")
			for x in dict[group]:
				for y, z in x.items(): #i don't know if there's a way to do this without three goddamn levels of nesting no. twst's file formatting sucks
					if y == "serif" and "text" in z.keys() and "speaker" in z.keys():# handles main dialogue (serifs)
						if "visible" in z["speaker"].keys() and not z["speaker"]["visible"]: # handles serifs w/o a speaker
							new_file.write("SFX\t" + formatDialogue(z["text"]) + "\n")
						else:
							new_file.write(nameTrans(z["speaker"]["text"]) + "\t" + formatDialogue(z["text"]) + "\n")
					elif y == "serif" and not "text" in z.keys(): # skips serifs without text
						pass
					elif y == "choice": # handles choices
						new_file.write("[CHOICE]\t1: " + formatDialogue(z[0]["text"]) + " (GOTO: " + z[0]["goTo"] + ")\n")
						new_file.write("[CHOICE]\t2: " + formatDialogue(z[1]["text"]) + " (GOTO: " + z[1]["goTo"] + ")\n")
					elif y == "goTo":
						new_file.write("[GOTO]\t" + z["goTo"] + "\n") # handles pathing
					elif y == "title" and "textWhite" in z.keys() and "textGold" in z.keys(): # handles titles
						if "episode" in z.keys(): # handles titles for episodes
							new_file.write("[TITLE]\tEpisode " + z["episode"]["storyNum"] + ": " + z["textWhite"] + "\n\t" + z["textGold"] + "\n")
						elif "prologue" in z.keys(): # handles titles for the prologue
							new_file.write("[TITLE]\tPrologue " + z["prologue"]["storyNum"] + ": " + z["textWhite"] + "\n\t" + z["textGold"] + "\n")
						elif "eventEpisode" in z.keys(): # handles titles for events
							new_file.write("[TITLE]\tEvent Episode " + z["eventEpisode"]["storyNum"] + ": " + z["textWhite"] + "\n\t" + z["textGold"] + "\n")
						elif "eventTitle" in z.keys(): # ...also handles titles for events
							new_file.write("[TITLE]\tEvent Episode " + z["eventTitle"]["storyNum"] + ": " + z["textWhite"] + "\n\t" + z["textGold"] + "\n")
						elif "personal" in z.keys(): # handles titles for personal stories
							new_file.write("[TITLE]\t" + z["textGold"] + " " + z["personal"]["rarity"] + ": " + z["personal"]["anotherName"] + "\n\t" + z["textWhite"] + "\n")
						elif "talk" in z.keys(): # handles titles for chats
							new_file.write("[TITLE]\t" + z["textGold"] + " Chat: " + z["talk"]["text"] + "\n\t" + z["textWhite"] + "\n")
						else: # handles other titles
							new_file.write("[TITLE]\t" + z["textWhite"] + "\n\t" + z["textGold"] + "\n")
					elif y == "title" and not "textWhite" in z.keys(): # skips titles without text
						pass
					elif y == "text" and "text" in z.keys(): # handles generic "text" content
						new_file.write("[TEXT]\t" + formatDialogue(z["text"]) + "\n")
					elif y == "place" and "jp" in z.keys() and "en" in z.keys(): # handles place titles
						new_file.write("[PLACE]\t" + z["jp"] + "\n\t" + z["en"] + "\n")
					elif y == "place" and not "jpn" in z.keys(): # skips places without text
						pass
					elif y == "telop" and "text" in z.keys(): #handles "telops"
						new_file.write("[TELOP]\t" + z["text"] + "\n")
					elif y == "telop" and not "text" in z.keys(): # skips telops without text
						pass
					elif y == "balloon" and "text" in z.keys() and "speaker" in z.keys(): # handles speech balloons (in rhythmics and battle cutscenes)
						new_file.write(nameTrans(z["speaker"]) + "\t" + formatDialogue(z["text"]) + "\n")
					elif y == "balloon" and not "text" in z.keys(): # skips balloons without text
						pass
					elif y == "cardSprite" and "cardId" in z.keys(): # handles card graphics
						if "isGroovy" in z.keys() and z["isGroovy"]:
							new_file.write("[CARD]\tShow " + str(z["cardId"]) + " Groovy\n")
						else:
							new_file.write("[CARD]\tShow " + str(z["cardId"]) + "\n")
					elif y == "cardSprite" and "delete" in z.keys() and z["delete"]:
						new_file.write("[CARD]\tHide Card\n")
					elif y == "sprite" and "path" in z.keys() and "fadeIn" in z.keys(): # handles item sprites
						new_file.write("[SPRITE]\t Show " + z["path"][z["path"].rfind("/") + 1:] + "\n")
					elif y == "sprite" and "fadeOut" in z.keys():
						new_file.write("[SPRITE]\tHide sprite\n")
					elif y == "live2d" or y == "moveCamera" or y == "systemUI" or y == "run" or y == "bgm" or y == "advBgOperator" or y == "touch" or y == "wait" or y == "zoomCamera" or y == "se" or y == "curtain" or y == "spine" or y == "spineCharacter" or y == "sd" or y == "spfx" or y == "shakeCamera" or y == "voice" or y == "transition" or y == "spriteUI" or y == "emotion": # skips a bunch of boring animation/visual logicistical code
						pass
					else: # for debugging mostly and to catch types i missed
						new_file.write(y + "\t(no code to handle this type of object yet, sorry! --Ylime)\n")
		elif group.startswith("word"): # this might only exist for the prologue intro but eh
			for x in dict[group]:
				for y, z in x.items():
					if y == "narration" and "text" in z.keys():
						new_file.write("[NARRATION]\t" + replaceNewLine(z["text"]) + "\n")
					elif y == "narration" and not "text" in z.keys():
						pass
					elif y == "voice" or y == "voiceWait":
						pass
					else:
						new_file.write(y + "\t(no code to handle this type of object yet, sorry! --Ylime)\n")
		elif group.startswith("initialize"): # skips past rhythmic animations
			new_file.write("(no dialogue in this type of JSON object!)\n")
			break
		else:
			new_file.write("(no code to handle this type of JSON file yet, sorry! --Ylime)\n")
	new_file.write("---------------------------------------------\nTwstStoryReader v" + verNum + " by Ylimegirl\nhttps://github.com/Ylimegirl/TwstStoryReader")
	new_file.close()
	print("> Parsed " + item)

print("Finished parsing all files.")