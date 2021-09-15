import os
import json
def prettyJSON(file_name): # code to make prettified output of json files
	if not os.path.exists("pretty"):
		os.mkdir("pretty")
	pretty = open("pretty/" + file_name[0:file_name.find(".")] + "_pretty.json", "w")
	pretty.write(json.dumps(json.loads(parsed), indent = 4))
	pretty.close() #inb4 no i do not know how to make these not output into unicode escaped characters, sorry!!