import os, json
def prettyJSON(data, file_name): # code to make prettified output of json files
	if not os.path.exists("pretty"):
		os.mkdir("pretty")
	pretty = open("pretty/" + file_name[0:file_name.find(".")] + "_pretty.json", "w", encoding="utf-8")
	pretty.write(json.dumps(json.loads(data), ensure_ascii=False, indent = 4))
	pretty.close()