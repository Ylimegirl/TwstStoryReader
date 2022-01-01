import re, unicodedata

name_ref = [["トレイン", "Trein"], ["リドル", "Riddle"], ["エース", "Ace"], ["デュース", "Deuce"], ["トレイ", "Trey"], ["ケイト", "Cater"], ["レオナ", "Leona"], ["ラギー", "Ruggie"], ["ジャック", "Jack"], ["アズール", "Azul"], ["ジェイド", "Jade"], ["フロイド", "Floyd"], ["カリム", "Kalim"], ["ジャミル", "Jamil"], ["ヴィル", "Vil"], ["ルーク", "Rook"], ["エペル", "Epel"], ["イデア", "Idia"], ["オルト", "Ortho"], ["マレウス", "Malleus"], ["リリア", "Lilia"], ["シルバー", "Silver"], ["セベク", "Sebek"], ["クロウリー", "Crowley"], ["クルーウェル", "Crewel"], ["バルガス", "Vargas"], ["サム", "Sam"], ["グリム", "Grim"]]
misc_ref = [["ハーツラビュル", "Heartslabyul"], ["サバナクロー", "Savanaclaw"], ["オクタヴィネル", "Octavinelle"], ["スカラビア", "Scarabia"], ["ポムフィオーレ", "Pomefiore"], ["イグニハイド", "Ignihyde"], ["ディアソムニア", "Diasomnia"], ["ゴースト", "Ghost"], ["男性", "Man"], ["女性", "Woman"]]

def nameTrans(string):
	for trans in name_ref:
		string = string.replace(trans[0], trans[1])
	for trans in misc_ref:
		string = re.sub(trans[0] + "寮生(\S*)", trans[1] + " Student \g<1>", string)
		string = re.sub(trans[0] + "(\S*)", trans[1] + " \g<1>", string)
	string = string.replace("・", "/")
	string = removeCR(string)
	string = unicodedata.normalize("NFKC", string) # normalizes fullwidth alphanumeric etc. characters to "half-width"
	return string

def formatDialogue(string):
	string = string.replace("[HERO_NAME]", "ユウ")
	return removeCR(string)

def removeCR(string): # removes stray carriage returns?? why are they here?? hello??
	return re.sub("\r(\n|$)", "\g<1>", string)