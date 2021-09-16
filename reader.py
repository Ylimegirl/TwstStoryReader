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
verNum = "0.4.0"

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
			new_file.write(group + "\t" + replaceNewLine(dict[group]["serif"]).replace("@", "\n\t") + "\n")#voice line jasons are so simple. bless
		elif group.startswith("group"):
			new_file.write("---------------------------------------------\n[GROUP]\t" + group + "\n")
			for x in dict[group]:
				for y, z in x.items(): #i don't know if there's a way to do this without three goddamn levels of nesting no. twst's file formatting sucks
					if y == "serif" and "text" in z.keys() and "speaker" in z.keys():# handles main dialogue (serifs)
						if "visible" in z["speaker"].keys() and not z["speaker"]["visible"]: # handles serifs w/o a speaker
							new_file.write("SFX\t" + formatDialogue(z["text"]) + "\n")
						elif "callNext" in z.keys() and not z["callNext"]: # handles bits of dialogue separated by other actions of some sort
							new_file.write(nameTrans(z["speaker"]["text"]) + "\t" + formatDialogue(z["text"]))
						elif "callClear" in z.keys() and not z["callClear"]: # other half of the callNext code
							new_file.write(formatDialogue(z["text"]) + "\n")
						else:
							new_file.write(nameTrans(z["speaker"]["text"]) + "\t" + formatDialogue(z["text"]) + "\n")
					elif y == "serif" and not "text" in z.keys(): # skips serifs without text
						pass
					elif y == "choice": # handles choices
						count = 1
						for obj in z:
							new_file.write("[CHOICE]\t" + str(count) + ": " + formatDialogue(obj["text"]) + " (GOTO: " + obj["goTo"] + ")\n")
							count+=1
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
					elif y == "narration" and "text" in z.keys(): # handles narration boxes
						new_file.write("[NARRATION]\t" + z["text"] + "\n")
					elif y == "narration" and "fadeOut" in z.keys():
						pass
					elif y == "narration" and "delete" in z.keys() and z["delete"]:
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
						if "delete" in z.keys() and z["delete"]:
							new_file.write("[CARD]\tHide Card " + str(z["cardId"]) + "\n")
						elif "isGroovy" in z.keys() and z["isGroovy"]:
							new_file.write("[CARD]\tShow Card " + str(z["cardId"]) + " Groovy\n")
						else:
							new_file.write("[CARD]\tShow Card " + str(z["cardId"]) + "\n")
					elif y == "cardSprite" and "delete" in z.keys() and z["delete"] == True:
						new_file.write("[CARD]\tHide Card\n")
					elif y == "sprite" and "path" in z.keys(): # handles item sprites
						new_file.write("[SPRITE]\tShow " + z["id"] + " (" + z["path"][z["path"].rfind("/") + 1:] + ")\n")
					elif y == "sprite" and "fadeOut" in z.keys():
						new_file.write("[SPRITE]\tFade out " + z["id"] + "\n")
					elif y == "sprite" and "visible" in z.keys() and z["visible"] == True:
						new_file.write("[SPRITE]\tShow " + z["id"] + "\n")
					elif y == "sprite" and "visible" in z.keys() and z["visible"] == False:
						new_file.write("[SPRITE]\tHide " + z["id"] + "\n")
					elif y == "sprite" and "delete" in z.keys() and z["delete"]:
						new_file.write("[SPRITE]\tHide " + z["id"] + "\n")
					elif y == "movie" and "path" in z.keys(): # handles movies
						new_file.write("[MOVIE]\t" + z["path"] + "\n")
					elif y == "mirrorMovie" and "delete" in z.keys() and z["delete"] == True: # handles movies but for the mirrors
						pass
					elif y == "mirrorMovie" and "mirrorId" in z.keys() and not "animation" in z.keys():
						new_file.write("[MIRROR]\tMovie " + str(z["mirrorId"]) + "\n")
					elif y == "mirrorMovie":
						pass
					elif y == "blot" and "dormitoryId" in z.keys() and "animation" in z.keys() and "phase" in z["animation"].keys(): # handles (over)blot animations
						new_file.write("[BLOT]\tDorm " + str(z["dormitoryId"]) + " Phase " + str(z["animation"]["phase"]) + "\n")
					elif y == "blot" and "animation" in z.keys() and "phase" in z["animation"].keys():
						new_file.write("[BLOT]\tPhase " + str(z["animation"]["phase"]) + "\n")
					elif y == "blot" and "dormitoryId" in z.keys() and not "animation" in z.keys():
						pass
					elif y == "blot" and "delete" in z.keys() and z["delete"]:
						pass
					elif y == "overBlot" and "dormitoryId" in z.keys() and "animation" in z.keys():
						new_file.write("[BLOT]\tDorm " + str(z["dormitoryId"]) + " Overblot\n")
					elif y == "overBlot" and "dormitoryId" in z.keys() and not "animation" in z.keys():
						pass
					elif y == "overBlot" and "delete" in z.keys() and z["delete"]:
						pass
					elif y == "live2d" or y == "moveCamera" or y == "systemUI" or y == "run" or y == "bgm" or y == "advBgOperator" or y == "touch" or y == "wait" or y == "zoomCamera" or y == "se" or y == "curtain" or y == "spine" or y == "spineCharacter" or y == "sd" or y == "spfx" or y == "shakeCamera" or y == "voice" or y == "transition" or y == "spriteUI" or y == "emotion" or y == "vibration" or y == "advBg" or y == "shakeLoopCamera": # skips a bunch of boring animation/visual logicistical code
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