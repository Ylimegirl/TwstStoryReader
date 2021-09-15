import re
name_ref = [["トレイン", "Trein"], ["リドル", "Riddle"], ["エース", "Ace"], ["デュース", "Deuce"], ["トレイ", "Trey"], ["ケイト", "Cater"], ["レオナ", "Leona"], ["ラギー", "Ruggie"], ["ジャック", "Jack"], ["アズール", "Azul"], ["ジェイド", "Jade"], ["フロイド", "Floyd"], ["カリム", "Kalim"], ["ジャミル", "Jamil"], ["ヴィル", "Vil"], ["ルーク", "Rook"], ["エペル", "Epel"], ["イデア", "Idia"], ["オルト", "Ortho"], ["マレウス", "Malleus"], ["リリア", "Lilia"], ["シルバー", "Silver"], ["セベク", "Sebek"], ["クロウリー", "Crowley"], ["クルーウェル", "Crewel"], ["バルガス", "Vargas"], ["サム", "Sam"], ["グリム", "Grim"]]
dorm_ref = [["ハーツラビュル", "Heartslabyul"], ["サバナクロー", "Savanaclaw"], ["オクタヴィネル", "Octavinelle"], 	["スカラビア", "Scarabia"], ["ポムフィオーレ", "Pomefiore"], ["イグニハイド", "Ignihyde"], ["ディアソムニア", "Diasomnia"]]

def nameTrans(string):
	for trans in name_ref:
		string = string.replace(trans[0], trans[1])
	for trans in dorm_ref:
		string = re.sub(trans[0] + "寮生(\S*)", trans[1] + " Student \g<1>", string)
	string = string.replace("・", "/")
	return string

def replaceNewLine(string):
	return string.replace("\n", "\n\t")

def formatDialogue(string):
	string = string.replace("[HERO_NAME]", "ユウ")
	return replaceNewLine(string)