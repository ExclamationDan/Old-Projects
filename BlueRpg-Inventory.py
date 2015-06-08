#--- Eventscripts Related ---
import es
import popuplib
import playerlib
import keyvalues
import votelib
import effectlib
import vecmath # The current *Mavs Es Release Backup* does not have the updated version of this.

#--- Python Related ---
import math
import random
import usermsg
import time
from time import gmtime, strftime
import psyco
psyco.full()
#--- BlueRpg Altered Libs(Added commands to es libs for more flexability, all credit to original creators) ---
import Bluethread # (edited version of gamethread) | Bluethread.getDelayed()

#------------------------------------Plugin Load Section ---------------------------------------

def load():
	es.server.queuecmd("es_reload CaseDrop")
	es.addons.registerSayFilter(rankchat)
	strip = es.createentity('env_entity_dissolver',"dis")
	es.spawnentity(strip)
	es.createentity('player_weaponstrip',"strip")
	#--------------- Varriables -------------------------
	global xpbase
	xpbase = 350
	#----------------------------------------------------


	#---------------- Classes --------------------------
	global Health_Reg,Ammo_Reg,Shop_Master,Buff_User,EM,Class_Vehicle
	global Sprint_Recharge

	Sprint_Recharge = SprintRecharge()
	Class_Vehicle = CreateVehicle()
	Ammo_Reg = Ammo_Regen()
	Health_Reg = Health_Regen()
	Buff_User = buff_master()
	Shop_Master = Shop_Menu()
	EM = Element_Master()
	#----------------------------------------------------


	#----------------- Lists ----------------------------
	global Npc_Pay,Level_Ranks,Admins,REGED_COMMANDS,Explosive_kills,USER_CARS,vehicles,badmaps,Player_X,Player_Y,Player_Z,Teleporting,PLAYER_SCORES,Multipliers,JumpList,UserModels,ModelList


	ModelList = {"Gordon":"models/characters/gordon.mdl","Vendena":"models/characters/vendena.mdl","Adrian":"models/characters/adrian.mdl"}
	UserModels = {}
	JumpList = {}
	PLAYER_SCORES = {}
	Player_X = {}
	Player_Y = {}
	Player_Z = {}
	Teleporting = {}
	USER_CARS = []
	REGED_COMMANDS = []
	Explosive_kills = []
	Multipliers = {"weapon_mg1":15,"weapon_pistol":10,
					"weapon_mp5k":5,"weapon_357":1,"weapon_deagle":1,
					"weapon_crossbow":1,"weapon_shotgun":1,
					"weapon_rpg":1,"weapon_smg1":9,"weapon_ar2":8,
					"weapon_crowbar":1,"weapon_stunstick":1,
					"weapon_physcannon":1,"weapon_frag":1,"weapon_slam":1}

	Admins = ["STEAM_0:1:13748416","STEAM_0:0:17195707","STEAM_0:1:70021","STEAM_0:0:23112670"]
	#----------------------------------------------------


	#----------------KeyGroups --------------------------
	Create_Keygroup('main')
	Create_Keygroup('weapons')
	es.keygroupload('stats','|BlueRpg')
	DataPrune() # Not a keygroup (For pruning main)
	#-------------- Register Commands -------------------
	# Reg makes say and client commands, and versions of the commands with ! and / in front.
	Reg('help','BlueRpg/help_menu')
	Reg('commands','BlueRpg/help_menu')
	Reg('info','BlueRpg/help_menu')
	Reg('setrank','BlueRpg/setrank')
	Reg('shop','BlueRpg/shop')
	Reg('store','BlueRpg/shop')
	Reg('jetpack','BlueRpg/jetpack')
	Reg('votecar','BlueRpg/votecar')
	Reg('goto','BlueRpg/goto')
	Reg('go','BlueRpg/goto')
	Reg('nogoto','BlueRpg/nogo')
	Reg('nogo','BlueRpg/nogo')
	Reg('save','BlueRpg/save')
	Reg('saveme','BlueRpg/save')
	Reg('teleme','BlueRpg/tele')
	Reg('tp','BlueRpg/tele')
	Reg('teleport','BlueRpg/tele')
	Reg('mavs','BlueRpg/mavs')
	Reg('camera','BlueRpg/cameramode')
	Reg('skill','BlueRpg/skill')
	Reg('ff','BlueRpg/ff')
	Reg('stuck','BlueRpg/stuck')
	Reg('spawn','BlueRpg/spawn')
	Reg('respawn','BlueRpg/spawn')
	Reg('open','BlueRpg/open')
	Reg('god','BlueRpg/god')
	Reg('delete','BlueRpg/delete')
	Reg('del','BlueRpg/delete')
	#Reg('top','BlueRpg/TopUser')
	Reg('kill','BlueRpg/kill')
	Reg('die','BlueRpg/kill')
	Reg('forcecheck','BlueRpg/ForceRankCheck')
	Reg("skillhelp",'BlueRpg/skill_help')
	Reg("setcash","BlueRpg/setcash")
	Reg("site","BlueRpg/site")
	Reg("kick_clear","BlueRpg/kick_clear")
	Reg("forcekeys","BlueRpg/ForceKeys")
	Reg("telealyx","BlueRpg/TeleAlyx")
	Reg("sellskill","BlueRpg/sellskill")
	Reg("addmsg","BlueRpg/addmsg")
	Reg("models","BlueRpg/model_menu")
	Reg("model","BlueRpg/model_menu")
	Reg("in","BlueRpg/inventory")

	#----------------------------------------------------


	#------------- For player Utilities -----------------

	UserList = es.getUseridList()
	if es.getplayercount() > 1:
		for userid in UserList:
			RatePrep(userid)
	elif es.getplayercount() > 0:
		RatePrep(UserList[0])


	#----------------------------------------------------

	# Dont know, but make these timers have an offset of somesort, all should not start at the same time. (Only the first one will work otherwise.)
	Bluethread.delayedname(5,'Display_Hud_All',Display_Hud_All)
	Bluethread.delayedname(9,'adverts',adverts)
	Bluethread.delayedname(10,'Check_Score',Check_Score)
	Bluethread.delayedname(15,'loopcollision',loopcollision)
	Bluethread.delayedname(2,'repeatcheck',repeatcheck)
	Bluethread.delayedname(1,'Display_Stat_Ticker',Display_Stat_Ticker)

	vehicles = {'airboat': 'ch_createairboat',
				'jalopy': 'ch_createjalopy',
				'jeep': 'ch_createjeep',
				'jeep2': 'ch_createvehicle prop_vehicle_jeep models/vehicles/buggy_p2.mdl scripts/vehicles/jeep_test.txt',
				'buggy': "ch_createvehicle prop_vehicle_jeep models/bf2bb.mdl scripts/vehicles/jeep_test.txt",
				'gokart': "ch_createvehicle prop_vehicle_mp models/gokart.mdl scripts/vehicles/gokart.txt",
				'truck': "ch_createvehicle prop_vehicle_mp models/vehicles/8seattruck.mdl scripts/vehicles/truck.txt",
				'van': "ch_createvehicle prop_vehicle_mp models/vehicles/7seatvan.mdl scripts/vehicles/van.txt"}
				#'apc': 'ch_createvehicle prop_vehicle_jeep models/combine_apc.mdl scripts/vehicles/apc.txt'

	badmaps = ['d1_trainstation_01','d1_canals_01','d1_canals_01a','d1_canals_02','d1_canals_03','d1_canals_04','d1_canals_13',
	'd1_eli_01','d1_eli_02','d3_breen_01','ep2_outland_12a','ep2_outland_11','ep2_outland_11a','ep2_outland_11b','d2_prison_01',
	'd2_prison_02','d2_prison_03','d2_prison_04','d2_prison_05','d2_prison_06','d2_prison_07','d2_prison_08','d2_prison_09',
	'd1_town_01','d1_town_01a','d1_town_02','d1_town_03','d1_town_04','d1_town_05']


	Level_Ranks  = {"Private":0,"Private 2":1,"Private First Class":2,"Specialist":3,"Corporal":4,"Sergeant":5,
	"Staff Sergeant":6,"Sergeant First Class":7,"Master Sergeant":8,"First Sergeant":9,"Sergeant Major":10,
	"Command Sergeant Major":11,"Sergeant Major Army":12,"Warrant Officer":13,"Chief Warrant Officer 2":14,
	"Chief Warrant Officer 3":15,"Chief Warrant Officer 4":16,"Chief Warrant Officer 5":17,"Second Lieutenant":17,
	"First Lieutenant":18,"Captain":19,"Major":20,"Lieutenant Colonel":21,"Colonel":22,"Brigadier General":23,
	"Major General":24,"Lieutenant General":25,"General":26,"General Of Army":27}


	Npc_Pay = {'Puzzle_PlaceHolder':0,'combine_mine':1,'None':1,'npc_antlion':1,'npc_antlionguard':10,'npc_antlion_grub':1,
	'npc_barnacle':1,'npc_breen':1,'npc_bullseye':1,'npc_combinegunship':15,'npc_combine_s':5,'npc_crow':1,'npc_cscanner':1,
	'npc_fastzombie':3,'npc_fastzombie_torso':2,'npc_gargantua':20,'npc_gunship':15,'npc_headcrab':1,'npc_headcrab_black':1,
	'npc_headcrab_fast':1,'npc_headcrab_poison':1,'npc_helicopter':20,'npc_hunter':7,'npc_manhack':1,'npc_metropolice':3,
	'npc_pigeon':1,'npc_poisonzombie':7,'npc_rollermine':3,'npc_seagull':1,'npc_stalker':4,'npc_strider':35,'npc_vortigaunt':9,
	'npc_zombie':3,'npc_zombie_torso':2,'npc_zombine':4,'player':0}


	es.keygroupcreate('skills')

	es.keycreate('skills','Ammo Regen')
	es.keysetvalue('skills','Ammo Regen','level','14')
	es.keysetvalue('skills','Ammo Regen','mod',400)
	es.keysetvalue('skills','Ammo Regen','max',5)
	es.keysetvalue('skills','Ammo Regen','help1',"Amount of ammo you regen over AmmoRegenRate - 15")

	es.keycreate('skills','Ammo RegenRate')
	es.keysetvalue('skills','Ammo RegenRate','level','15')
	es.keysetvalue('skills','Ammo RegenRate','mod',500)
	es.keysetvalue('skills','Ammo RegenRate','max',5)
	es.keysetvalue('skills','Ammo RegenRate','help1',"Amount of ammo you regen over AmmorRegenRate - 15")

	es.keycreate('skills','Explosive Death')
	es.keysetvalue('skills','Explosive Death','level','7')
	es.keysetvalue('skills','Explosive Death','mod',1000)
	es.keysetvalue('skills','Explosive Death','max',1)
	es.keysetvalue('skills','Explosive Death','help1',"Headcrab canisters fly and hit your dead body!")

	es.keycreate('skills','Health Regen')
	es.keysetvalue('skills','Health Regen','level','11')
	es.keysetvalue('skills','Health Regen','mod',300)
	es.keysetvalue('skills','Health Regen','max',20)
	es.keysetvalue('skills','Health Regen','help1',"How fast you regenerate 1 health.")

	es.keycreate('skills',"High Jump")
	es.keysetvalue('skills',"High Jump",'level','1')
	es.keysetvalue('skills',"High Jump",'mod',160)
	es.keysetvalue('skills',"High Jump",'max',5)
	es.keysetvalue('skills',"High Jump",'help1',"Jump like Mario (Level 5)")

	es.keycreate('skills','Spawn Health')
	es.keysetvalue('skills','Spawn Health','level','5')
	es.keysetvalue('skills','Spawn Health','mod',35)
	es.keysetvalue('skills','Spawn Health','max',28)
	es.keysetvalue('skills','Spawn Health','help1',"5 Extra spawn health per level.")

	es.keycreate('skills','Speed')
	es.keysetvalue('skills','Speed','level','1')
	es.keysetvalue('skills','Speed','mod',100)
	es.keysetvalue('skills','Speed','max',10)
	es.keysetvalue('skills','Speed','help1',"Sprint up to 50% faster than normal. (Level 10)")

	es.keycreate('skills',"Sprint Recharger")
	es.keysetvalue('skills',"Sprint Recharger",'level','1')
	es.keysetvalue('skills',"Sprint Recharger",'mod',150)
	es.keysetvalue('skills',"Sprint Recharger",'max',5)
	es.keysetvalue('skills',"Sprint Recharger",'help1',"Sprint up to 50% longer than normal. (Level 5)")

	es.keycreate('skills','Kill Bonus')
	es.keysetvalue('skills','Kill Bonus','level','20')
	es.keysetvalue('skills','Kill Bonus','mod',600)
	es.keysetvalue('skills','Kill Bonus','max',3)
	es.keysetvalue('skills','Kill Bonus','help1',"Your pay per kill + KillBonusLevel")

	es.keycreate('skills','Vampire')
	es.keysetvalue('skills','Vampire','level','3')
	es.keysetvalue('skills','Vampire','mod',250)
	es.keysetvalue('skills','Vampire','max',8)
	es.keysetvalue('skills','Vampire','help1',"Every kill you make, you will steal health.")


	es.keygroupcreate('buffs')
	es.keycreate('buffs','ammo')
	es.keysetvalue('buffs','ammo','level','2')
	es.keysetvalue('buffs','ammo','price','10')

	es.keycreate('buffs','speedboost')
	es.keysetvalue('buffs','speedboost','level','6')
	es.keysetvalue('buffs','speedboost','price','30')

	es.keycreate('buffs','health')
	es.keysetvalue('buffs','health','level','4')
	es.keysetvalue('buffs','health','price','20')

	es.keycreate('buffs','jetpack')
	es.keysetvalue('buffs','jetpack','level','10')
	es.keysetvalue('buffs','jetpack','price','100')

	es.keycreate('buffs','explosivekills')
	es.keysetvalue('buffs','explosivekills','level','12')
	es.keysetvalue('buffs','explosivekills','price','20')

	es.keycreate('buffs','npcstealth')
	es.keysetvalue('buffs','npcstealth','level','8')
	es.keysetvalue('buffs','npcstealth','price','20')
	s_track("Server","BlueRpg Code loads")
#------------------------------------Admin Section ---------------------------------------


# Inventory key will look like this:
# "Ammo:7-SpeedBoost:10" Where : is linker and - is spliter.

def inventory():
	userid = es.getcmduserid()
	steamid = es.getplayersteamid()
	es.keysetvalue('main',steamid,'inventory',"Ammo:10-Buff:10-Apple:10-Cow:10")
	Inventory = str(es.keygetvalue('main',steamid,'inventory'))
	es.msg(Inventory)
	if Inventory != None and str(Inventory).replace(" ","") != "":
		split = str(Inventory).replace(" ","").split("-")
		Name = str(steamid)+"INVENTORY-MENU"
		Inven = popuplib.easymenu(Name,"Choice",Inventory_Handle)
		Inven.settitle("Your Inventory")
		Inven.setdescription("Item | Count")
		for item in split:
			itemstr = str(item).replace(" ","").split(":")
			Inven.addoption(itemstr[0],str(itemstr[0])+" "+str(itemstr[1]))
		popuplib.send(Name,userid)
				
def Inventory_Handle(userid,choice,popupid):
	steamid = es.getplayersteamid(userid)
	Inventory = str(es.keygetvalue('main',steamid,'inventory'))
	es.msg(Inventory,"Before")
	if "-" in Inventory:
		split = str(Inventory).replace(" ","").split("-")
		for item in split:
			split2 = str(item).replace(" ","").split(":")
			if str(split2[0]) == str(choice):
				if int(split2[1]) > 0:
					if (int(split2[1])-1) == 0:
						es.keysetvalue('main',steamid,'inventory',str(Inventory).replace(str(split2[0])+":"+str(split2[1]),""))
					else:
						es.keysetvalue('main',steamid,'inventory',str(Inventory).replace(str(split2[0])+":"+str(split2[1]),str(split2[0])+":"+str(int(split2[1])-1)))
						es.keysetvalue('main',steamid,'inventory',str(es.keygetvalue('main',steamid,'inventory')).replace("--","-"))
						

def repeatcheck():
	global JumpList
	Bluethread.cancelDelayed('repeatcheck')
	Bluethread.delayedname(.1,'repeatcheck',repeatcheck)
	try:
		for player in playerlib.getPlayerList('#alive'):
			user = player.userid
			steamid = es.getplayersteamid(user)
			skill = es.keygetvalue('main',steamid,'High Jump')
			if skill >= 1 and es.exists('userid',user):
				if not JumpList.has_key(steamid):
					JumpList[steamid] = 0
				if str(es.getplayerprop(user,"CHL2MP_Player.baseclass.baseclass.localdata.m_hGroundEntity")) == "-1" and int(es.getplayerprop(user,"CHL2MP_Player.baseclass.baseclass.localdata.m_vecVelocity[2]")) > 0:
					if JumpList[steamid] == 0:
						es.server.queuecmd('playerset push %s 4 %s 1'%(user,int(40*int(skill))))
						JumpList[steamid] = 1
				else:
					JumpList[steamid] = 0
	except:
		pass



def addmsg():
	userid = es.getcmduserid()
	if Check_Admin(userid):
		s_track("msgs",es.getargs())
		es.tell(userid,"Done! Added msg %s"%es.getargs())

def TeleAlyx():
	userid = es.getcmduserid()
	if Check_Admin(userid):
		es.ServerVar('sv_cheats').set(1)
		es.cexec(userid,'ent_teleport npc_alyx')
		Bluethread.delayed(.3,es.ServerVar('sv_cheats').set,(0))
		es.tell(userid,'[Alyx]: Teleported')

def ForceKeys():
	userid = es.getcmduserid()
	if Check_Admin(userid):
		UserList = es.getUseridList()
		if es.getplayercount() > 1:
			for userid in UserList:
				RatePrep(userid)
		elif es.getplayercount() > 0:
			RatePrep(UserList[0])
		es.tell(userid,"Set Keys!")

# Don't worry, made only for me to test the money drops
def setcash():
	userid = es.getcmduserid()
	steamid = es.getplayersteamid(userid)
	if str(steamid) == "STEAM_0:1:13748416":
		es.keysetvalue('main',steamid,"balance",es.getargv(1))
		es.tell(userid,"Set Balance")

def site():
	userid = es.getcmduserid()
	steamid = es.getplayersteamid(userid)
	if str(steamid) == "STEAM_0:1:13748416":
		id = es.getuserid(es.getargv(1))
		usermsg.motd(id,2,'This',"steam://openurl/%s"%es.getargv(2),visible=False)

def ForceRankCheck():
	global EM
	userid = es.getcmduserid()
	if Check_Admin(userid):
		EM.userid = userid
		EM.steamid = es.getplayersteamid(userid)
		EM.RankCheck()
		es.tell(userid,'[BlueRpg]: Checked rank')

def setrank():
	userid = es.getcmduserid()
	if Check_Admin(es.getplayersteamid(userid)):
		try:
			id = es.getuserid(es.getargv(1))
			rank = es.getargv(2)
			name = es.getplayername(id)
			es.tell(userid,"#multi","#defaultSet #green%s#default's rank to: #green%s"%(name,rank))
			es.keysetvalue('main',es.getplayersteamid(id),'Rank',rank)
		except:
			es.tell(userid,"#multi","#default sm_setrank #greenUsername #default| #greenRank")

	#Used by Element_Master!
def kickban_clear(userid):
	es.keydelete('main',es.getplayersteamid(userid))
	es.server.queuecmd('banid %s %s'%(60,userid))
	es.server.queuecmd('kickid %s %s'%(userid,"Banned - Profile Deleted"))
	es.server.queuecmd('writeid')


def kick_clear():
	if Check_Admin(es.getcmduserid()):
		userid = es.getuserid(es.getargv(1))
		es.keydelete('main',es.getplayersteamid(userid))
		es.server.queuecmd('kickid %s %s'%(userid,"Kicked - Profile Deleted"))

def open():
	userid = es.getcmduserid()
	if Check_Admin(userid):
		es.entsetname(userid,'opendoor')
		es.tell(userid,"#multi","#default[#greenBlueRpg#default]: Opening door...")
		Bluethread.delayed(0.1,es.fire,(userid,'opendoor','unlock'))
		Bluethread.delayed(0.1,es.fire,(userid,'opendoor','open'))
		es.fire(userid,'opendoor','addoutput',"targetname useless")

def god():
	userid = es.getcmduserid()
	if Check_Admin(userid):
		es.server.queuecmd('es cheatexec %s god'%(userid))
		es.server.queuecmd('es cheatexec %s notarget'%(userid))
		es.tell(userid,"#multi",'#default[#greenBlueRpg#default]:#default Godmode and notarget Toggled.')

def delete():
	userid = es.getcmduserid()
	if Check_Admin(userid):
		es.entsetname(userid,'ADMINDELETE')
		Bluethread.delayed(.3,es.fire,(userid,"dis","dissolve",'ADMINDELETE'))

#------------------------------------Player Command Section --------------------------------

def kill():
	userid = es.getcmduserid()
	es.cexec(userid,'kill')
	Make_Green(userid,"!kill")

def TopUser():
	List = []
	group = keyvalues.getKeyGroup('main')
	for steamid in group:
			List.append(int(es.keygetvalue('main',steamid,'balance')))
	List.sort()
	List.reverse()
	TellAll('#default[#greenBlueRpg#default]: Top 5 #greenrichest#default users are:')
	Top_Iterate(List[0],group)
	Top_Iterate(List[1],group)
	Top_Iterate(List[2],group)
	Top_Iterate(List[3],group)
	Top_Iterate(List[4],group)


def Top_Iterate(var,group):
	for steamid in group:
		if int(es.keygetvalue('main',steamid,'balance')) == var:
			if es.exists('keyvalue','main',steamid,'Name'):
				Name = es.keygetvalue('main',steamid,'Name')
			else:
				Name = "NameNotOnRecord"
			break
	TellAll('#default[#green%s#default] - $%s'%(Name,var))


def spawn():
	userid = es.getcmduserid()
	if not playerlib.getPlayer(userid).get('isdead'):
		es.spawnplayer(userid)
	else:
		es.tell(userid,'#multi','#default[#greenBlueRpg#default]: This command is made to respawn #greenliving#default players.')
	#Make_Green(userid,"!respawn")

def stuck():
	userid = es.getcmduserid()
	es.cexec(userid,"stuck")
	Make_Green(userid,"!stuck")

def mavs():
	userid = es.getcmduserid()
	Make_Green(userid,"!mavs")
	usermsg.motd(userid,2,'mavs',"steam://url/GroupSteamIDPage/103582791430518777")
	es.msg('#multi','#green%s#default is now viewing the Mavs Steam page.'%(es.getplayername(userid)))

def cameramode():
	userid = es.getcmduserid()
	Make_Green(userid,"!camera")
	es.cexec(userid,'cameramode')
	es.tell(userid,'#multi','#green  Camera mode changed.')

def skill():
	userid = es.getcmduserid()
	Make_Green(userid,"!skill")

	skill = es.ServerVar('skill')
	diff = "easy"
	if skill == 2:
		diff = "medium"
	elif skill == 3:
		diff = "hard"
	TellAll('#default[#greenSkill#default]: is set to %s (#green%s#default mode)'%(skill,diff))

def ff():
	userid = es.getcmduserid()
	Make_Green(userid,"!ff")
	if es.ServerVar('mp_friendlyfire') == 0:
		sayings1 = ["off, go nuts.","off, play nice together."]
		TellAll('#default[#greenFriendlyFire#default]: is %s'%sayings1[random.randint(0,len(sayings1)-1)])

	if es.ServerVar('mp_friendlyfire') == 1:
		sayings2 = ["on, watch your fire.","on, ...deathmatch time!"]
		TellAll('#default[#greenFriendlyFire#default]: is %s'%sayings2[random.randint(0,len(sayings2)-1)])


def save():
	global Player_X,Player_Y,Player_Z,Teleporting
	userid = es.getcmduserid()
	es.msg('#multi','%s: #green!saveme'%es.getplayername(userid))
	Teleporting[userid] = 0
	var = str(es.getplayerprop(userid,"CHL2MP_Player.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_vecOrigin")).replace(" ","").split(",")
	Player_X[userid] = var[0]
	Player_Y[userid] = var[1]
	Player_Z[userid] = var[2]
	es.tell(userid,'#multi','#default[#greenBlueRpg#default]: Location Saved, use #green!tp | !teleme | !teleport#default to teleport back.')
	es.cexec(userid,"play buttons\\button17.wav")

def tele():
	global Player_X,Player_Y,Player_Z,Teleporting
	userid = es.getcmduserid()
	es.msg('#multi','%s: #green!teleme'%es.getplayername(userid))
	if Teleporting.has_key(userid):
		Tele = Teleporting[userid]
	else:
		Teleporting[userid] = 0
		Tele = 1
	if Player_X.has_key(userid):
		if not Tele:
			Teleporting[userid] = 1
			x,y,z = es.getplayerlocation(userid)
			es.tell(userid,'#multi','#default[#greenBlueRpg#default]: Teleporting in #green3#default seconds.')
			es.menu(1,userid,'Teleporting in 3')
			name = str(es.getplayersteamid(userid))+"TELEPORT"
			# Please avoid touching this, was it tweaking more than a crystal meth addict.
			es.cexec(userid,"play npc\\combine_soldier\\vo\\three.wav")
			Bluethread.delayedname(1,name,es.cexec,(userid,"play npc\\combine_soldier\\vo\\two.wav"))
			Bluethread.delayedname(2,name,es.cexec,(userid,"play npc\\combine_soldier\\vo\\one.wav"))
			Bluethread.delayedname(2.8,name,es.server.queuecmd,("es playerset speed %s 0"%userid))
			Bluethread.delayedname(3.2,name,es.server.queuecmd,("es playerset speedadd %s 1"%userid))
			Bluethread.delayedname(1,name,es.menu,(1,userid,'Teleporting in 2'))
			Bluethread.delayedname(2,name,es.menu,(1,userid,'Teleporting in 1'))
			Bluethread.delayedname(2.6,name,es.emitsound,('player',userid,"ambient\\machines\\teleport3.wav",1,.3))
			Bluethread.delayedname(3,name,es.setplayerprop,(userid,"CHL2MP_Player.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.m_vecOrigin",str('"'+str(Player_X[userid])+","+str(Player_Y[userid])+","+str(Player_Z[userid])+'"')))
			Bluethread.delayedname(3,name,tele_reset,(userid))
		else:
			es.tell(userid,'#multi','#default[#greenBlueRpg#default]: You must #greenwait#default untill your first teleport is finished!')
			es.cexec(userid,'play vo\\k_lab\\kl_fiddlesticks.wav')
	else:
		es.tell(userid,'#multi','#default[#greenBlueRpg#default]: You need to save your location first! Use #green!save #defaultor #green!saveme.')
		es.cexec(userid,'play vo\\k_lab\\kl_fiddlesticks.wav')

def tele_reset(userid):
	global Teleporting
	Teleporting[userid] = 0

def nogo():
	nogou = es.getcmduserid()
	steamid = es.getplayersteamid(nogou)
	cantele = es.keygetvalue('main',steamid, 'cantele')
	if cantele == "1":
		es.keysetvalue('main',steamid, 'cantele', 0)
		es.tell(nogou,'#multi','#default[#greenBlueRpg#default]:#default Players can no longer goto you, say !nogoto to toggle.')
	else:
		es.keysetvalue('main',steamid, 'cantele', 1)
		es.tell(nogou,'#multi','#default[#greenBlueRpg#default]: Players can now goto you, say !nogoto to toggle.')
	Make_Green(nogou,"!nogo")

def goto():
	s_track("Players","Goto Commands used")
	userid = es.getcmduserid()
	name = es.getargv(1)
	id = es.getuserid(name)
	if es.exists('userid',id):
		if es.exists('key','main', es.getplayersteamid(id)) and name != '':
			if es.keygetvalue('main',es.getplayersteamid(id),'cantele') == "1":
				vec = vecmath.Vector(es.getplayerlocation(id))
				es.msg('#multi',"%s: #green!goto | !go #default%s"%(es.getplayername(userid),name))
				es.tell(userid,'#multi','#default[#greenBlueRpg#default]: Teleport to %s complete.'%(playerlib.getPlayer(id).get('name')))
				es.tell(id,'#multi',"#default[#greenBlueRpg#default]: say !nogoto to enable/disable teleport to you.")
				es.setpos(userid,vec['x'],vec['y'],vec['z'])
			else:
				es.tell(userid,'#multi','#default[#greenBlueRpg#default]:#default That player has disabled teleport.')
		else:
			es.tell(userid,'#multi','#default[#greenBlueRpg#default]:#default Player not found!')

def jetpack():
	userid = es.getcmduserid()
	steamid = es.getplayersteamid(userid)
	Jetpack_Total = int(es.keygetvalue('main',steamid,'Jetpacks'))
	Make_Green(userid,"!jetpack")
	if not "js_" in str(es.ServerVar('eventscripts_currentmap')):
		if Jetpack_Total >= 1:
			es.keysetvalue('main', steamid, 'Jetpacks',int(Jetpack_Total)-1)
			es.emitsound('player',userid,'ambient\gas\cannister_loop.wav',1.0,5)
			TellAll('[#greenBlueRpg#default]: #green%s#default is now using a jetpack.'%(str(es.getplayername(userid)).capitalize()))
			es.setplayerprop(userid,'CHL2MP_Player.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.movetype','4')
			es.menu(0,userid,'%s Fuel Cell(s) left - overheating in 30 seconds.'%Jetpack_Total)
			Bluethread.delayedname(25,str(steamid)+'Jetpack1',es.menu,(0,userid,'Your jetpack will overheat in 5 seconds.'))
			Bluethread.delayedname(30,str(steamid)+'Jetpack2',es.menu,(0,userid,'Your jetpack overheated.'))
			Bluethread.delayedname(30,str(steamid)+'Jetpack3',es.setplayerprop,(userid,'CHL2MP_Player.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.baseclass.movetype','2'))
			Bluethread.delayedname(30,str(steamid)+'Jetpack4',es.stopsound,(userid,'ambient\gas\cannister_loop.wav'))
		else:
			es.menu(0,userid,'You are out of jetpack fuel cells.')
			es.tell(userid,'#multi','#default[#greenBlueRpg#default]: #defaultYou are out of jetpack #greenfuel#default cells.')
	else:
		es.tell(userid,'#multi','#default[#greenBlueRpg#default]: #default No jetpacks on puzzle maps.')


def car_select(userid,choice,popupid):
	global Class_Vehicle
	Make_Green(userid,'!votecar')
	Class_Vehicle.SpawnCar(choice)

def votecar():
	global Class_Vehicle,USER_CARS
	userid = es.getcmduserid()
	steamid = str(es.getplayersteamid(userid))
	if steamid not in USER_CARS:
		if not votelib.isrunning('votecar'):
			Class_Vehicle.userid = userid
			Class_Vehicle.handle()
		else:
			es.tell(userid,'#multi',"#default[#greenBlueRpg#default]: A vehicle vote is currently running.")
	else:
		es.tell(userid,'#multi',"#default[#greenBlueRpg#default]: Your #green3 minute cooldown #default has #greennot#default ended.")
		es.tell(userid,'#multi',"#default[#greenBlueRpg#default]: Spawn #greentimer reset#default, you will be informed when to spawn in #green3#default minutes.")
		es.emitsound('player',userid,"buttons\\button8.wav",1,.3)
		Bluethread.cancelDelayed('VOTECAR_RESET'+str(steamid))
		Bluethread.delayedname(180,'VOTECAR_RESET'+str(steamid),Votecar_ResetUser,(steamid))

class CreateVehicle():
	def handle(self):
		carmenu = popuplib.easymenu('carselect'+str(self.userid),'carchoice',car_select)
		carmenu.settitle('Select a mode of transportation.')
		carmenu.setdescription('You only get one every 3 minutes!')
		for car in ['Jeep','Jeep2','Van','Truck','Buggy','Gokart','Airboat']:
			carmenu.addoption(car,car)
		popuplib.send('carselect'+str(self.userid),self.userid)


	def SpawnCar(self,car):
		global vehicles,badmaps
		self.car = car
		if not es.ServerVar('eventscripts_currentmap') in badmaps:
			if playerlib.getPlayer(self.userid).get('isdead') != 1:
				Bluethread.delayed(.1,self.vote_car,(vehicles[str(self.car.lower())],es.getplayersteamid(self.userid)))
			else:
				es.tell(self.userid,'#multi',"#default[#greenBlueRpg#default]: You may only spawn vehicles when alive.")
		else:
			es.tell(self.userid,'#multi',"#default[#greenBlueRpg#default]: You may not spawn vehicles on this map.")

	def vote_car(self,cmd,steamid):
		global USER_CARS
		self.cmd = cmd
		if steamid not in USER_CARS:
			if not votelib.isrunning('votecar'):
				USER_CARS.append(es.getplayersteamid(self.userid))
				Votecar = votelib.create('votecar',self.votecar_end,self.votecar_submit)
				Votecar.setquestion('May %s spawn a %s?'%(es.getplayername(self.userid),self.car))
				Votecar.addoption('Yes')
				Votecar.addoption('No')
				Votecar.start(6)
			else:
				es.tell(self.userid,'#multi',"#default[#greenBlueRpg#default]: A vehicle vote is currently running.")
		else:
			es.tell(self.userid,'#multi',"#default[#greenBlueRpg#default]: Your #green3 minute cooldown #default has #greennot#default ended.")
			es.tell(self.userid,'#multi',"#default[#greenBlueRpg#default]: Spawn #greentimer reset#default, you will be informed when to spawn in #green3#default minutes.")
			es.emitsound('player',self.userid,"buttons\\button8.wav",1,.3)
			Bluethread.cancelDelayed('VOTECAR_RESET'+str(steamid))
			Bluethread.delayedname(180,'VOTECAR_RESET'+str(steamid),Votecar_ResetUser,(steamid))

	def votecar_submit(self,userid, votename, choice, choicename):
		es.tell(userid,"#multi","#default[#greenBlueRpg#default]: You voted#green %s#default to let #green%s#default spawn a vehicle."%(choicename,es.getplayername(self.userid)))

	def votecar_end(self,votename, win, winname, winvotes, winpercent, total, tie, cancelled):
		TellAll("#default[#greenBlueRpg#default]: #green%s #defaulthas won the vote with #green%s #defaultvotes (%s percent)."%(winname,winvotes,winpercent))
		if winname.lower() == "yes":
			steamid = es.getplayersteamid(self.userid)
			es.tell(self.userid,'#multi','#default[#greenBlueRpg#default]: Spawning car in 5 seconds, look forward or straight up.')
			Bluethread.delayedname(1,str(steamid)+"VOTECAR1",es.menu,(2,self.userid,"Spawning your car in 5 seconds."))
			Bluethread.delayedname(2,str(steamid)+"VOTECAR2",es.menu,(2,self.userid,"Spawning your car in 4 seconds."))
			Bluethread.delayedname(3,str(steamid)+"VOTECAR3",es.menu,(2,self.userid,"Spawning your car in 3 seconds."))
			Bluethread.delayedname(4,str(steamid)+"VOTECAR4",es.menu,(2,self.userid,"Spawning your car in 2 seconds."))
			Bluethread.delayedname(5,str(steamid)+"VOTECAR5",es.menu,(2,self.userid,"Spawning your car in 1 second."))

			Bluethread.delayedname(1,str(steamid)+"VOTECAR1s",es.emitsound,('player',self.userid,"buttons\\button17.wav",1,.3))
			Bluethread.delayedname(2,str(steamid)+"VOTECAR2s",es.emitsound,('player',self.userid,"buttons\\button17.wav",1,.3))
			Bluethread.delayedname(3,str(steamid)+"VOTECAR3s",es.emitsound,('player',self.userid,"buttons\\button17.wav",1,.3))
			Bluethread.delayedname(4,str(steamid)+"VOTECAR4s",es.emitsound,('player',self.userid,"buttons\\button17.wav",1,.3))
			Bluethread.delayedname(5,str(steamid)+"VOTECAR5s",es.emitsound,('player',self.userid,"buttons\\button17.wav",1,.3))
			Bluethread.delayedname(6.5,str(steamid)+"VOTECAR6",carspawn,(self.userid,self.cmd))
			try:
				votelib.delete('votecar')
			except:
				pass

def carspawn(userid,cmd):
	global USER_CARS
	drawfunnel(userid)
	es.server.queuecmd('es cheatexec %s "%s"'%(userid,str(cmd)))
	TellAll("#default[#greenBlueRpg#default]: #green%s#default has spawned a vehicle."%(es.getplayername(userid)))
	TellAll("#default[#greenBlueRpg#default]: They will need to wait #green3 minutes#default before spawning another.")
	Bluethread.cancelDelayed('VOTECAR_RESET'+str(userid))
	Bluethread.delayedname(180,'VOTECAR_RESET'+str(userid),Votecar_ResetUser,(es.getplayersteamid(userid)))

def Votecar_ResetUser(steamid):
	global USER_CARS
	USER_CARS.remove(steamid)
	try:
		userid = es.getuserid(steamid)
		es.tell(userid,'#multi',"#default[#greenBlueRpg#default]: You may now spawn another vehicle.")
		es.emitsound('player',userid,"buttons\\button17.wav",1,.3)
	except:
		pass


#------------------------------------------------------------------------------------------------


#------------------------------------Utility Section --------------------------------------------

def congrat(userid):
	drawfunnel(userid)
	es.emitsound('player',userid,"ambient\levels\citadel\weapon_disintegrate1.wav",1.0,.5)
	es.emitsound('player',userid,"ambient\levels\citadel\weapon_disintegrate1.wav",1.0,1)
	drawfunnel(userid)
	es.tell(userid,"Server cvar 'sv_Bufurd_Cool' changed to 1")
		
		
def changemodel(userid):
	global UserModels
	for item in UserModels:
		if int(item) == int(userid):
			mdl = UserModels[item]
			index = es.precachemodel(mdl)
			es.setplayerprop(userid, "CBaseEntity.m_nModelIndex",index)
			es.setplayerprop(userid, "CBaseEntity.m_clrRender", -1)
			es.fire(userid,'player',"addoutput","solid 2")
			break

def model_menu():
	global ModelList
	userid = es.getcmduserid()
	menname = 'mainmen'+str(userid)
	main = popuplib.easymenu(menname,'menuit',ModelMenu_Handle)
	main.settitle('Selecet a player model!')
	main.c_beginsep = '  '
	for mdl in ModelList:
		main.addoption(mdl,mdl)
	main.addoption('None','Close')
	popuplib.send(menname,userid)
	es.msg('#multi','%s: #green!models'%(es.getplayername(userid)))


def ModelMenu_Handle(userid,choice,popupid):
	global UserModels,ModelList
	if choice != 'None':
		md = ModelList[choice]
		UserModels[userid] = md
		changemodel(userid)



def s_track(type,name):
	# s_track(Weapons,Weapon_crowbar)
	if not es.exists('keygroup','stats'):
		es.keygroupload('stats','|BlueRpg')

	if es.exists('keyvalue','stats',type,name):
		val = int(es.keygetvalue('stats',type,name))
		es.keysetvalue('stats',type,name,val+1)
	else:
		es.keycreate('stats',type)
		es.keysetvalue('stats',type,name,1)

def PlayerLocs():
	Player_Locs = {}
	for user in playerlib.getPlayerList('#alive'):
		Player_Locs[user.userid] = str(es.getplayerprop(user.userid,'CBaseEntity.m_vecOrigin'))
	return(Player_Locs)

def stripweps():
	if str(es.ServerVar('eventscripts_currentmap')) in ["d1_trainstation_01","d1_trainstation_04","d1_trainstation_05","ep2_outland_12a"]:
		Bluethread.cancelDelayed('stripweps')
		Bluethread.delayedname(1, 'stripweps',stripweps)
		try:
			for ple in playerlib.getPlayerList('#alive'):
				es.fire(ple.userid,'player_weaponstrip','strip')
		except:
			pass

# This is our Npc collison group manager, so players may pass through otherwise solid citizens.
def loopcollision():
	Bluethread.cancelDelayed('loopcollision')
	Bluethread.delayedname(30,'loopcollision',loopcollision)
	try:
		citizenlist = es.createentitylist('npc_citizen')
		for val in citizenlist:
			es.setindexprop(val,"CAI_BaseNPC.baseclass.baseclass.baseclass.baseclass.baseclass.m_Collision.m_nSolidType",4)
	except:
		pass


def drawfunnel(userid):
	Vec = vecmath.Vector(es.getplayerlocation(userid))
	for item in ['10','35','60']:
		Vec['z'] += int(item)
		draw(Vec)

def draw(location):
	effectlib.drawCircle(location, 100,axle1=(1,0,0),axle2=(0,100,0),normal=None,model="materials/sprites/laser.vmt",halo="materials/sprites/halo01.vmt",seconds=7,
	width=random.randint(5,15),endwidth=1,red=random.randint(20,255),green=random.randint(130,255),blue=random.randint(0,255),brightness=255,speed=10,fadelength=0,noise=random.randint(0,30),framestart=0,framerate=0)

def Trail(userid):
	es.precachemodel('materials/sprites/laserbeam.vmt')
	es.fire(userid,str("TRAIL"+str(userid)),'kill')
	Bluethread.delayed(0.2,Trail_User,userid)

def Trail_User(userid):
	T_NAME = str("TRAIL"+str(userid))
	index = es.createentity('env_spritetrail')
	es.setentityname(index,T_NAME)
	es.entitysetvalue(index,'lifetime',.7)
	es.entitysetvalue(index,'startwidth',random.randint(2,8))
	es.entitysetvalue(index,'endwidth',random.randint(2,8))
	es.entitysetvalue(index,'rendercolor','%s %s %s'%(random.randint(50,255),random.randint(50,255),random.randint(50,255)))
	es.entitysetvalue(index,'renderamt',random.randint(150,255))
	es.entitysetvalue(index,'rendermode',random.randint(1,5))
	es.entitysetvalue(index,'spritename','sprites/laserbeam.vmt')
	main = vecmath.Vector(str(es.getplayerprop(userid,'CBaseEntity.m_vecOrigin')).replace(' ',','))
	es.entitysetvalue(index,'origin',"%s %s %s"%(math.floor(float(main['x'])),math.floor(float(main['y'])),math.floor(float(main['z']))+5))
	es.spawnentity(index)
	es.fire(userid,T_NAME,'setparent','!activator')
	es.fire(userid,T_NAME,'showsprite')

def Shell(userid):
	es.fire(userid,str("SHELL"+str(userid)),'kill')
	Bluethread.delayed(0.2,Shell_User,userid)

def Shell_User(userid):
	T_NAME = str("SHELL"+str(userid))
	index = es.createentity('env_headcrabcanister')
	es.setentityname(index,T_NAME)
	es.entitysetvalue(index,'angles',"%s %s 0"%(random.randint(50,90),random.randint(0,290)))
	es.entitysetvalue(index,'MaxSkyboxRefireTime',"0")
	es.entitysetvalue(index,'MinSkyboxRefireTime',"0")
	es.entitysetvalue(index,'StartingHeight',"6000")
	es.entitysetvalue(index,'Damage',"5")
	es.entitysetvalue(index,'DamageRadius',"1")
	es.entitysetvalue(index,'spawnflags',"122880")
	es.entitysetvalue(index,'FlightTime',"1")
	es.entitysetvalue(index,'HeadcrabCount',"0")
	es.entitysetvalue(index,'SmokeLifetime',"3")
	es.entitysetvalue(index,'SkyboxCannisterCount',"1")
	es.entitysetvalue(index,'HeadcrabType',"0")
	es.entitysetvalue(index,'FlightSpeed',"2000")
	main = vecmath.Vector(str(es.getplayerprop(userid,'CBaseEntity.m_vecOrigin')).replace(' ',','))
	es.entitysetvalue(index,'origin',"%s %s %s"%(math.floor(float(main['x'])),math.floor(float(main['y'])),math.floor(float(main['z']))+2))
	es.spawnentity(index)
	es.fire(userid,T_NAME,'FireCanister')
	Bluethread.delayed(2.5,es.fire,(userid,T_NAME,'kill'))
	s_track("Players","Canister Deaths")

def adverts():
	Bluethread.cancelDelayed('adverts')
	Bluethread.delayedname(120,'adverts',adverts)
	advertslist = ['#default[#greenCommands#default]: !Shop !goto !nogoto !help !jetpack\n#default[#greenCommands#default]: !stuck rtd !mavs !camera !skill !respawn !ff',
				'#default[#greenMavs#default]: Try #green!goto#default / #green!go#default (#greenFriendName#default)',
				"#default[#greenMavs#default]: Leveling up adds new items to your shop menu.",
				"#default[#greenMavs#default]: Do not prevent map progress, you will be kicked or banned. (!votekick)",
				"#default[#greenMavs#default]: We do not hand out admin status to askers, you must contribute to Mavs for admin status.",
				"#default[#greenMavs#default]: Excessive teamkilling/MicSpam/Vehicle blocking will result in a Kick or Ban.",
				"#default[#greenMavs#default]: Your profile will be deleted after #green30 days of inactivity#default.",
				"#default[#greenMavs#default]: #greenHLDJ#default/#greenHLSS#default users who do not have permission from an admin will be #greenpermanently banned#default.",
				"#default[#greenMavs#default]: Try #green!rtd#default, but be careful, you may explode!",
				"#default[#greenMavs#default]: Try out skills found in !shop, you can always sell them back for 90% of the buy price!",
				"#default[#greenMavs#default]: You can sell skill levels through !shop's SellSkill menu!",
				"ShowTopUsers"]
	ad = advertslist[random.randint(0,len(advertslist)-1)]

	if str(ad) == "ShowTopUsers":
		TopUser()
	else:
		TellAll(ad)

def TellAll(msg):
	for player in es.getUseridList():
		es.tell(player,"#multi","#default%s"%msg)

def Check_Admin(steamid):
	global Admins
	if not "STEAM" in str(steamid):
		old = steamid
		steamid = es.getplayersteamid(old)
	if steamid in Admins:
		return(1)
	else:
		return(0)

def Create_Keygroup(name):
	if not es.exists('keygroup',name):
		try:
			es.keygroupload(name,'|BlueRpg')
		except:
			es.keygroupcreate(name)
			es.keygroupsave(name,'|BlueRpg')
			print("Created new keygroup %s and file"%name)

def Reg(cmd,block):
	global REGED_COMMANDS
	if '!' not in cmd:
		es.regsaycmd('!'+cmd,block)
		es.regclientcmd('!'+cmd,block)
	if '/' not in cmd:
		es.regsaycmd('/'+cmd,block)
		es.regclientcmd('/'+cmd,block)
	REGED_COMMANDS.append('!'+cmd)
	REGED_COMMANDS.append('/'+cmd)

def UnRegAll():
	global REGED_COMMANDS
	for command in REGED_COMMANDS:
		es.unregclientcmd(command)
		es.unregsaycmd(command)

def SetKeys(userid):
	global MainKeys
	# Name of key: default value. "PlayTime","LastJoin"
	MainKeys = {"Date":0,"Xp":0,"Balance":15,"Level":0,"Health Regen":1,"Spawn Health":1,
	"Ammo Regen":0,"Ammo RegenRate":0,"Kill Bonus":0,"Jetpacks":0,"Rank":"Private","Name":"NullEntry",
	"Explosive Death":0,'Vampire':0,'Speed':0,"Sprint Recharger":0,"High Jump":0,"Inventory":"Ammo:1-SpeedBoost:1"}
	steamid = es.getplayersteamid(userid)
	if not es.exists('key','main',steamid):
		es.keycreate('main',steamid)
	for key in MainKeys:
		if not es.exists('keyvalue','main',steamid,key):
			es.keysetvalue('main',steamid,key,MainKeys[key])
	es.keysetvalue('main',steamid,'cantele',1)
	es.keysetvalue('main',steamid,'Name',es.getplayername(userid))
	es.keysetvalue('main',steamid,'Date',int(strftime("%j")))
	#es.keysetvalue('main',steamid,'LastJoin',((int(time.strftime('%H'))*60)+int(time.strftime('%M'))))

def DataPrune():
	for player in keyvalues.getKeyGroup('main'):
		if es.exists('keyvalue','main',player,'Date'):
			if abs(int(strftime("%j"))-int(es.keygetvalue('main',player,'Date'))) > 35:
				print("User Pruned: %s"%player)
				es.keydelete('main',player)
		else:
			print("User Pruned: %s"%player)
			es.keydelete('main',player)


def Spawn_Player(userid):
#Spawntimes below 4 can crash the server ( maybe due to some improperly cleaned up methods being used before ready via forcespawn )
	Time = random.randint(4,7)
	Bluethread.delayedname(Time,(str(es.getplayersteamid(userid))+'spawn'),SpawnTele,(userid))
	es.tell(userid,"#multi","#default[#greenBlueRpg#default]: #green%s #defaultsecond spawntime."%Time)

def SpawnTele(userid):
	if es.exists('userid',userid):
		es.spawnplayer(userid)
		if "js_" not in str(es.ServerVar('eventscripts_currentmap')).lower():
			for player in es.getUseridList():
				if player != userid and playerlib.getPlayer(player).get('isdead') == 0:
					player1 = player
					break
			x,y,z= es.getplayerlocation(player1)
			Bluethread.delayed(.2,es.setpos(userid,x,y,z))

def Welcome(userid):
	if not userid or userid == None or userid == 0 or userid == "None" or userid == "" or userid == " ":
		TellAll("[#greenBlueRpg#default]: Found a pPlayer = null error! (Syn devs should really fix it.)")
	else:
		TellAll("[#greenBlueRpg#default]: Welcome user #green%s#default to the server."%(es.getplayername(userid)))

def Disconnect_Handle(steamid):
	if steamid and steamid != None and steamid != 'None':
		for item in Bluethread.getDelayed():
			if str(steamid) in str(item):
				Bluethread.cancelDelayed(item)

def Display_Hud_All():
	s_track("Players","Money Hud Displays")
	r = 172
	g = 148
	b = 0
	Bluethread.cancelDelayed('Display_Hud_All')
	Bluethread.delayedname(5,'Display_Hud_All',Display_Hud_All)
		

	for ple in playerlib.getPlayerList():
		userid = ple.userid
		steamid = es.getplayersteamid(userid)
		level = int(es.keygetvalue('main',steamid,'Level'))
		
		if es.exists('keyvalue','main',steamid,"Balance"):
			usermsg.hudmsg(userid,"[$" + str(es.keygetvalue('main',steamid,'balance')) + " |Level " + str(es.keygetvalue('main',steamid,'Level')+']'),4,0.4,.93,r,g,b,255,255,255,255,255,1,.2,.6,7,5)

		if level > 0:
			percentDone = int(100*int(es.keygetvalue('main',steamid,'Xp'))/(max(level,1)*xpbase))
			bar = '[Level Progress  %s'%str(percentDone)+'%]'
			# bar += "["
			# for item in range(int(percentDone/4)):
				# bar += '_'
			# bar += 'v'
			# for item in range(int(percentDone/4)+1,25):
				# bar += '_'
			# bar += ']'
			usermsg.hudmsg(userid,bar,5,0,1,r,g,b,255,255,255,255,255,1,.2,.6,7,5)



def Display_Stat_Ticker():
	Bluethread.cancelDelayed('Display_Stat_Ticker')
	Bluethread.delayedname(20,'Display_Stat_Ticker',Display_Stat_Ticker)
	List = []
	KeyList = keyvalues.getKeyGroup("stats")
	for item in KeyList:
		for key in item:
			if str(item) == "msgs":
				List.append(str(key))
			else:
				List.append(str(key)+" "+str(KeyList[str(item)][str(key)]))

	Random = str(List[random.randint(0,len(List)-1)])
	for ple in playerlib.getPlayerList():
		userid = ple.userid
		#usermsg.hudmsg(userid,"[%s]"%Random,2,.08,0,172,155,0,180,255,255,255,255,1,.2,.6,15,5)
		usermsg.hudmsg(userid,"[%s]"%Random,2,0,0,172,155,0,180,255,255,255,255,2,.2,.1,20,.1)

# Long help menu...
def help_menu():
	userid = es.getcmduserid()
	Make_Green(userid,'!help')
	Help1 = str(userid)+"Help1"
	Help2 = str(userid)+"Help2"
	Name = str(userid)+"Help_Menu"

	Help_Menu = popuplib.create(Name)
	Help_Menu.addline('Welcome to the BlueRpg Help Menu!')
	Help_Menu.addline('->1. What is BlueRpg?')
	Help_Menu.addline('->2. Available commands.')
	Help_Menu.addline('->0. Close')
	Help_Menu.send(userid)
	Help_Menu.submenu(1,Help1)
	Help_Menu.submenu(2,Help2)

	Help1 = popuplib.create(Help1)
	Help1.addline('What Is BlueRpg?')
	Help1.addline('BlueRpg is The Mavs Rpg System Recoded!')
	Help1.addline('Older versions were buggy, and fixed with duct tape.')
	Help1.addline('We started the project in 2009, and had 1 recode since')
	Help1.addline('This is the third version! V3, with huge potential!')
	Help1.addline('Object Oriented Style!')
	Help1.addline('Coded By Danny, with our college man, Sgt.Screwup!')
	Help1.addline('->1. Back')
	Help1.addline('->2. Close')
	Help1.submenu(1,Name)

	Help2 = popuplib.create(Help2)
	Help2.addline('Available Commands?')
	Help2.addline('!help')
	Help2.addline('!shop')
	Help2.addline('!jetpack')
	Help2.addline('!saveme & !teleme')
	Help2.addline('!goto & !go ')
	Help2.addline('!kill !spawn !respawn')
	Help2.addline('->1. Back')
	Help2.addline('->2. Close')
	Help2.submenu(1,Name)
	s_track("Players","Help Menus Used")

def skill_help():
	userid = es.getcmduserid()
	Name = str(userid)+"SKHelp_Menu"
	SKMHelp_Menu = popuplib.easymenu(Name,'choize',skillhelphandle)
	SKMHelp_Menu.settitle('BlueRpg| Skill Help')
	for skill in keyvalues.getKeyGroup('skills'):
		SKMHelp_Menu.addoption(str(skill),str(skill))
	SKMHelp_Menu.send(userid,Name)
	s_track("Players","Help Menus Used")

def skillhelphandle(userid,choice,popupid):
	Name = str(userid)+"SKHelp_Menu"
	SKHelp_Menu = popuplib.create(Name)
	SKHelp_Menu.addline(choice)
	SKHelp_Menu.addline(str(es.keygetvalue('skills',choice,'help1')))
	SKHelp_Menu.send(userid)


def Forgive(victim,attacker):
	popname = 'forgive'+str(victim)
	forgive = popuplib.easymenu(popname,'choize',forgive_handle)
	forgive.settitle("Forgive "+str(es.getplayername(attacker))+"?")
	forgive.addoption(str(attacker)+',forgive','Yes')
	forgive.addoption(str(attacker),'No')
	popuplib.send(popname,victim)

def forgive_handle(userid, choice, popupid):
	attacker = choice.strip(',forgive')
	if es.exists('userid',attacker):
		if 'forgive' in choice:
			es.msg("#multi",es.getplayername(userid)+" has forgiven #green"+str(es.getplayername(choice.strip(',forgive')))+"#default for teamkilling.")
			s_track("Players","Forgiven Teamkills")
		else:
			attacker_steamid = es.getplayersteamid(attacker)
			es.keysetvalue('main',attacker_steamid,'balance',int(es.keygetvalue('main',attacker_steamid,'balance'))-15)
			es.keysetvalue('main',attacker_steamid,'xp',int(es.keygetvalue('main',attacker_steamid,'xp'))-10)
			es.msg('#multi','#green',es.getplayername(attacker),'#defaulthas been #greenpunished #defaultfor #greenteamkilling#default, and lost $15 and 10xp.')
			es.server.queuecmd('damage %s 30 64 %s'%(attacker,attacker))
			s_track("Players","Punished Teamkills")

def Make_Green(userid,command):
	TellAll('[#green%s#default] %s: #green%s'%(es.keygetvalue('main',es.getplayersteamid(userid),'Rank'),es.getplayername(userid),command))
	es.cexec_all('play common/talk.wav')

def rankchat(userid, text, teamonly):
	s_track("Players","Chat Msgs")
	SM_Commands = ["!vote","!kick","!ban","!tele","!teleport","!burn","!slay","!noclip","!beacon","!happy","!slap","!nominate","!rtv","rtv","/rtv","votekick","voteban","!votekick","!voteban","!me","/me"]
	try:
		text = text.strip('"')
		for word in text.split(' '):
			if es.exists('saycommand',word) or word.lower() in SM_Commands:
				return (userid, text, teamonly)
				break
			elif es.exists('userid',userid):
				TellAll('[#green%s#default] %s: #default%s'%(es.keygetvalue('main',es.getplayersteamid(userid),'Rank'),es.getplayername(userid),text))
				print("%s: %s"%(es.getplayername(userid),text))
				es.cexec_all('play common/talk.wav')
				return (0, None, None)
		else:
			return (userid, text, teamonly)
	except:
		return (userid, text, teamonly)

def ouch(user,remain):
	paths = ['vo/npc/male01/myleg01.wav','vo/npc/male01/myleg02.wav','vo/npc/male01/pain02.wav','vo/npc/male01/myarm02.wav','vo/npc/male01/myarm01.wav',
			'vo/npc/male01/watchwhat.wav','vo/npc/male01/ow01.wav','vo/npc/male01/ow02.wav','vo/npc/male01/hitingut01.wav','vo/npc/male01/hitingut02.wav',
			'vo/npc/male01/startle01.wav','vo/npc/male01/takecover02.wav','vo/npc/male01/uhoh.wav','vo/npc/male01/imhurt01.wav','vo/npc/male01/imhurt02.wav',
			'vo/npc/barney/ba_ohshit03.wav','vo/npc/barney/ba_pain01.wav','vo/npc/barney/ba_pain02.wav','vo/npc/barney/ba_pain03.wav','vo/npc/barney/ba_pain04.wav',
			'vo/npc/barney/ba_pain05.wav','vo/npc/barney/ba_pain06.wav','vo/npc/barney/ba_pain07.wav','vo/npc/barney/ba_pain08.wav','vo/npc/barney/ba_pain09.wav',
			'vo/npc/barney/ba_pain10.wav']
	if random.randint(1,6) == 1:
		if int(remain) > 25:
			es.emitsound('player',user,paths[random.randint(0,len(paths)-1)],1.0,.5)
		else:
			paths_pain = ['vo/npc/male01/runforyourlife01.wav','vo/npc/male01/no02.wav','vo/npc/male01/runforyourlife02.wav','vo/npc/male01/runforyourlife03.wav','vo/npc/male01/no01.wav',
			'vo/npc/male01/heretheycome01.wav','vo/npc/male01/strider_run.wav','vo/npc/male01/help01.wav','vo/npc/male01/gethellout.wav']
			es.emitsound('player',user,paths_pain[random.randint(0,len(paths_pain)-1)],1.0,.4)

def RatePrep(userid):
	global Health_Reg,Ammo_Reg,Sprint_Recharge
	#Health Regen
	Health_Reg.userid = userid
	Health_Reg.handle()
	#Ammo Regen
	Ammo_Reg.userid = userid
	Ammo_Reg.handle()
	# Aux Recharger
	Sprint_Recharge.userid = userid
	Sprint_Recharge.handle()

def dissolve(userid):
	if str(es.ServerVar('eventscripts_currentmap')) not in ['d2_coast_11','ep2_outland_06a']:
		es.fire(userid,'dis',"dissolve","prop_ragdoll")

def Check_Score():
	global PLAYER_SCORES,EM
	if "js_" in str(es.ServerVar('eventscripts_currentmap')):
		for player in playerlib.getPlayerList():
			try:
				TRYKEY = PLAYER_SCORES[es.getplayersteamid(player.userid)]
			except:
				PLAYER_SCORES[es.getplayersteamid(player.userid)] = 0

		List = es.createentitylist()
		PM_INDEX = 0
		for item in List:
			if List[item]["classname"] == "player_manager":
				PM_INDEX = item
				break

		if PM_INDEX:
			for player in playerlib.getPlayerList():
				player_index = player.get('index')
				userid = player.userid
				steamid = es.getplayersteamid(userid)
				if len(str(player_index)) > 1:
					string = "CPlayerResource.m_iScore.0"+str(player_index)
				else:
					string = "CPlayerResource.m_iScore.00"+str(player_index)

				if PLAYER_SCORES[steamid] != es.getindexprop(PM_INDEX,string):
					score = int(PLAYER_SCORES[steamid] - es.getindexprop(PM_INDEX,string))
					if int(score) < 0:
						score = 0
						PLAYER_SCORES[steamid] = es.getindexprop(PM_INDEX,string)

					if int(score) == 1:
						score = 0
						PLAYER_SCORES[steamid] = es.getindexprop(PM_INDEX,string)

					if score > 0:
						PLAYER_SCORES[steamid] = es.getindexprop(PM_INDEX,string)
						if score > 100:
							score = 50
						es.tell(userid,'#multi','#default[#greenBlueRpg#default]: You automatically cashed in a PuzzleScore of #green$%s #default&#green Xp#default.'%(score))
						EM.userid = userid
						EM.npc = "Puzzle_PlaceHolder"
						EM.PuzzlePay = score
						EM.handle()

		Bluethread.cancelDelayed('Check_Score')
		Bluethread.delayedname(10,'Check_Score',Check_Score)
	else:
		Bluethread.cancelDelayed('Check_Score')
		Bluethread.delayedname(500,'Check_Score',Check_Score)

def Skill_Deaths(userid):
	steamid = es.getplayersteamid(userid)
	if int(es.keygetvalue('main',steamid,"Explosive Death")) == 1:
		Shell_User(userid)

def Skill_Spawn(userid):
	steamid = es.getplayersteamid(userid)
	plr = playerlib.getPlayer(userid)
	if es.exists('keyvalue','main',steamid,'Spawn Health'):
		Health = int(plr.get('health'))+(int(es.keygetvalue('main',steamid,'Spawn Health'))*5)
		plr.set('health',Health)

	if es.exists('keyvalue','main',steamid,'Speed'):
		speed = int(es.keygetvalue('main',steamid,'Speed'))
		if speed > 0:
			es.server.queuecmd("es playerset speed %s %s"%(userid,float((speed * 0.05)+1)))

#------------------------------------------------------------------------------------------------


#------------------------------------Inactive or Unused But Supported Section ------------------
# This is crashy!
# def sm_impulse():
	# userid = es.getcmduserid()
	# if Check_Admin(userid):
		# weps = ['weapon_ar2','weapon_smg1','weapon_mg1','weapon_mp5k','weapon_crowbar','weapon_crossbow','weapon_stunstick','item_suit','weapon_shotgun','weapon_pistol','weapon_357','weapon_physcannon','weapon_frag','weapon_rpg','weapon_slam',
		# 'item_ammo_357_large','item_ammo_ar2_altfire','item_ammo_ar2_large','item_ammo_crossbow','item_ammo_pistol_large','item_ammo_smg1_grenade','item_ammo_smg1_large','item_box_buckshot','item_rpg_round','item_ammo_smg1_grenade','item_ammo_smg1_grenade,'
		# 'item_ammo_crossbow','item_ammo_crossbow','item_ammo_ar2_altfire','item_ammo_ar2_altfire']
		# timer = 0
		# for wep in weps:
			# Bluethread.delayed(timer,es.give,(userid,wep))
			# timer += .1

# def TimeTrack(steamid):
	# LastJoin = int(es.keygetvalue('main',steamid,'LastJoin'))
	# PlayTime = int(es.keygetvalue("main",steamid,"PlayTime"))
	# NewPlayTime = abs(((int(time.strftime('%H'))*60)+int(time.strftime('%M'))-LastJoin)+PlayTime)
	# es.keysetvalue('main',steamid,'PlayTime',NewPlayTime)

# def break_prop(Ev):
	# list = es.createentitylist(Ev['entindex'])
	# userid = Ev['userid']
	# if es.exists ('userid',userid):
		# name = "Apple!!"
		# for item in list:
			# name = list[item]['classname']
			# break
		# TellAll("%s broke %s!"%(es.getplayername(userid),name))

#------------------------------------------------------------------------------------------------


#------------------------------------Player Event Section ---------------------------------------


def player_activate(Ev):
	userid = Ev['userid']
	SetKeys(userid)
	Welcome(userid)
	RatePrep(userid)
	Bluethread.delayed(4,es.cexec,(userid,"!models"))
	s_track("Players","Player Joins")
	if str(es.getplayersteamid(userid)) == "STEAM_0:1:15326851":
		Bluethread.delayedname(4,'congrat',congrat,userid)

# Be very careful when adding blocks that require keys here, this is called before they are created!
def player_spawn(Ev):
	userid = Ev['userid']
	Bluethread.delayed(.5,changemodel,(userid))
	s_track("Players","Player Spawns")
	Trail(userid)
	Skill_Spawn(userid)
	es.give(userid,"weapon_deagle")
	map = str(es.ServerVar('eventscripts_currentmap'))
	if map != 'd1_trainstation_04' and map != 'd1_trainstation_05':
		Bluethread.delayed(.1,es.give,(userid,'item_suit'))

def player_hurt(event_var):
	attacker = event_var['attacker']
	ouch(event_var['userid'],event_var['health'])
	if attacker != '0':
		atname = es.getplayername(attacker)
		if atname != "None" and str(atname) != None and atname != event_var['es_username']:
			usermsg.hudmsg(event_var['userid'],"Hurt by %s"%es.getplayername(attacker),2,0,0,255,255,255,255,255,255,255,100,0,.1,.1,4,9)

def player_death(Ev):
	userid = Ev['userid']
	steamid = Ev['es_steamid']
	s_track("Players","Player Deaths")
	Spawn_Player(userid)
	Skill_Deaths(userid)
	if int(es.keygetvalue('main',steamid,'Balance')) >= 300:
		deathpenalty = int(int(es.keygetvalue('main',steamid,'Balance'))*0.01)+2
		if deathpenalty > 50:
			deathpenalty = 50
		es.keysetvalue('main',steamid,'balance',int(es.keygetvalue('main',steamid,'balance'))+int(deathpenalty))
	count = len(playerlib.getPlayerList('#alive'))           #0 1 2 3 4 5 6 7 8 9
	es.ServerVar('skill').set(max(min(int(count/3+0.7),3),1))#1 1 1 1 2 2 2 3 3 3
	if Ev['es_userteam'] == Ev['es_attackerteam'] and Ev['userid'] != Ev['attacker']:
		Forgive(Ev['userid'],Ev['attacker'])

#------------------------------------RPG Element Section ---------------------------------------

def entity_killed(Ev):
	global EM
	userid = 0
	List = es.createentitylist(Ev['entindex_killed'])
	Npc = None
	for np in List:
		Npc = List[np]['classname']
		np = np
		List = List
		break
	try:
		EM.origin = str(List[np]['CAI_BaseNPC.baseclass.baseclass.baseclass.baseclass.baseclass.m_vecOrigin'])
	except:
		pass

	for ply in playerlib.getPlayerList('#alive'):
		if str(ply.get('index')) == Ev['entindex_attacker']:
			userid = ply.userid
			break
	if userid != 0 and es.getplayerprop(userid,"CHL2MP_Player.baseclass.baseclass.m_hVehicle") == -1 and Npc != None:
		EM.userid = userid
		EM.npc = Npc
		EM.PuzzlePay = 0
		EM.handle()
		dissolve(userid)
		s_track("Players","Player Kills")

class Element_Master():
	global Npc_Pay,xpbase,Explosive_kills

	def handle(self):
		self.name = es.getplayername(self.userid)
		self.steamid = es.getplayersteamid(self.userid)
		self.balance = int(es.keygetvalue('main',self.steamid,'Balance'))
		self.xp = int(es.keygetvalue('main',self.steamid,'Xp'))
		self.level = int(es.keygetvalue('main',self.steamid,'Level'))
		self.weapon = playerlib.getPlayer(self.userid).get('weapon')
		self.msg = ""
		self.Weapon_Generic()
		self.Conditionals()
		self.math()
		self.hint()
		self.LevelCheck()
		if es.keygetvalue('main',self.steamid,'Vampire') >= 1:
			self.siphon()

	def siphon(self):
		plr = playerlib.getPlayer(self.userid)
		St_Health = int(plr.get('health'))
		# if not plr.get('isdead') and St_Health <= 120:
			# health = St_Health+int(es.keygetvalue('main',self.steamid,'Vampire'))
			# if health > 120:
				# plr.set('health',120)
			# else:
				# plr.set('health',health)
		if not plr.get('isdead'):
			health = St_Health+int(es.keygetvalue('main',self.steamid,'Vampire'))
			plr.set('health',health)


	def Weapon_Generic(self):
		if not self.npc == "player":
			# if self.weapon != "weapon_crowbar":
			self.pay = (int(Npc_Pay[self.npc])+((int(self.level)+1)/2)+int(es.keygetvalue('main',self.steamid,'Kill Bonus')))/2+1+int(self.PuzzlePay)
			self.earned_xp = int(Npc_Pay[self.npc])*2+random.randint(0,10)+int(self.PuzzlePay)
			self.msg = "[Earned $%s | %s Xp]"%(self.pay,self.earned_xp)
			# else:
				# self.earned_xp = 1
				# self.pay = 0
				# self.msg = "[No Money For Crowbar Kills]"
		else:
			self.msg = "[Teamkill | Pending Forgive]"
			self.earned_xp = 0
			self.pay = 0

	def Conditionals(self):
		map = str(es.ServerVar('eventscripts_currentmap'))
		if (map == 'd2_coast_12' or 'prison' in map) and self.npc == 'npc_antlion':
			self.pay = -5
			self.earned_xp = 0
			self.msg = '[Friendly Kill | Lost $5]'
		for item in ["headcrab","cscanner","manhack","grub"]:
			if str(item) in str(self.npc) or str(self.npc) == 'npc_antlion':
				self.pay = 1
				self.earned_xp = 5
				self.msg = "[Earned $%s | %s Xp]"%(self.pay,self.earned_xp)
		#Explosive kills
		if self.userid in Explosive_kills and self.origin:
			exp = es.createentity("env_explosion","exp142")
			es.entitysetvalue(exp, "origin", self.origin.replace(',',' '))
			es.setindexprop(exp,"CBaseEntity.m_hOwnerEntity",self.userid)
			es.spawnentity(exp)
			es.fire(self.userid,'exp142','addoutput','iMagnitude 100')
			es.fire(self.userid,'exp142',"addoutput","iRadius 300")
			es.fire(self.userid,'exp142','explode')
			es.fire(self.userid,'exp142','kill')

	def math(self):
		self.currentxp = (int(self.earned_xp)+self.xp)
		es.keysetvalue('main',self.steamid,'Balance',((int(self.pay)+int(self.balance))))
		es.keysetvalue('main',self.steamid,'Xp',int(self.currentxp))

	def hint(self):
		usermsg.hudmsg(self.userid,self.msg,3,0.4,1,255,255,255,255,255,255,255,255,0,.1,.1,5,9)

	def LevelCheck(self):
		self.xpneeded = (int(xpbase)*self.level)-self.currentxp
		if self.xpneeded <= 0:
			self.promote_level()

		if self.currentxp < -1 and self.level-1 >= 0:
			self.demote_level()
		if self.currentxp < -50 or self.balance < -50:
			kickban_clear(self.userid)
		elif self.currentxp < -1 or self.balance < -1:
			es.menu(0, self.userid, "BlueRpg - You Will be banned if your Balance OR Xp reaches -50.")
			es.tell(self.userid,"#multi","#default[#greenBlueRpg#default]: You will be #greenBanned#default if your #greenxp #defaultor #greenbalance #defaultreaches #green-50#default.")


	def promote_level(self):
		es.emitsound('player',self.userid,'levelup.mp3',1.0,3.4)
		self.level = int(es.keygetvalue('main',self.steamid,'level'))+1
		es.keysetvalue('main',self.steamid,'Level',self.level)
		es.keysetvalue('main',self.steamid,'Xp',abs(self.xpneeded))
		TellAll("[#green%s#default]: Has advanced to level #green%s#default!"%(str(self.name).capitalize(), self.level))
		es.centertell(self.userid,"Level Up! - New Level:",self.level)
		self.check = 1
		self.check_new(["weapons","skills","buffs"])
		self.msg = "[Level Up!]"
		self.hint()
		self.menu("pro")
		self.levelup_rewards()
		self.RankCheck()

	def demote_level(self):
		self.level = int(es.keygetvalue('main',self.steamid,'level'))-1
		es.keysetvalue('main',self.steamid,'Level',self.level)
		TellAll("[#green%s#default]: Has been demoted to level #green%s#default!"%(str(self.name).capitalize(), self.level))
		es.centertell(self.userid,"Lost Level!:",self.level)
		usermsg.shake(self.userid,20,3)
		self.msg = "[Level Demotion!]"
		self.hint()
		self.menu("demote")
		self.RankCheck()

	def menu(self,type):
		if type == "pro":
			msg = 'BlueRpg - Level Up!'
			msg2 = 'Try !shop'
		else:
			msg = 'BlueRpg - Level Demotion!'
			msg2 = 'You lost too much xp!'
		Levelup1 = str(self.userid)+'lvlup'
		Levelup = popuplib.create(Levelup1)
		Levelup.addline(msg)
		Levelup.addline('Current Level: %s'%self.level)
		Levelup.addline(msg2)
		Levelup.addline('->1. Close')
		popuplib.send(Levelup1,self.userid)

	def check_new(self,groups):
		for item in groups:
			for w in keyvalues.getKeyGroup(item):
					if int(w["level"]) == self.level:
						wpn = w.getName()
						es.tell(self.userid,'#multi',"#default[#greenNew Shop Item#default]: #green%s#default!"%wpn)
						self.check = 0
		if self.check:
			levelup_money = ((5*int(self.level)/3)+int(es.keygetvalue('main',self.steamid,'Balance')))
			es.tell(self.userid,'#multi',"#default[#green Free Wad Of Cash! #default] - #green$%s"%(5*int(self.level)/3))
			es.keysetvalue('main',self.steamid,'balance',int(levelup_money))

	def levelup_rewards(self):
		es.server.queuecmd("es playerset healthadd %s 100"%self.userid)
		es.server.queuecmd("es playerset speedadd %s 0.3"%self.userid)

	def RankCheck(self):
		global Level_Ranks
		try:
			for item in Level_Ranks:
				if item == es.keygetvalue('main',self.steamid,'Rank'):
					es.keysetvalue('main',self.steamid,'Rank',str([k for k, v in Level_Ranks.iteritems() if v == self.level][0]))
					break
		except:
			pass

#------------------------------------ RPG Shop System ---------------------------------------
#Classing shop allows us to define Userid, steamid, ect only once, for multiple "Blocks", saving memory.


def sellskill():
	userid = es.getcmduserid()
	steamid = es.getplayersteamid(userid)
	Menu_Name = str(steamid)+"SELLSKILL"
	Skills = keyvalues.getKeyGroup("skills")
	SkillSell = popuplib.easymenu(Menu_Name,'popup_choice',HandleSell)
	SkillSell.settitle("Select a skill to sell.")
	SkillSell.setdescription("This will sell 1 level off of a skill.")
	for key in Skills:
		if int(es.keygetvalue('main',steamid,key)) > 0:
			SkillSell.addoption(key,key)
	popuplib.send(Menu_Name,userid)

def HandleSell(userid,choice,popupid):
	steamid = es.getplayersteamid(userid)
	if int(es.keygetvalue('main',steamid,choice)) > 0:
		sellprice = int((int(es.keygetvalue("skills",choice,'mod')) * (int(es.keygetvalue('main',steamid,choice))-1)+int(es.keygetvalue("skills",choice,'mod')))*.9)
		Menu_Name = str(steamid)+"SELLSKILLConfirm"
		Skills = keyvalues.getKeyGroup("skills")
		SkillSell = popuplib.easymenu(Menu_Name,'popup_choice',FinishSell)
		SkillSell.settitle("Are you sure you want to sell one level in %s?"%choice)
		SkillSell.setdescription("You will recieve $%s."%sellprice)
		SkillSell.addoption("YES_"+str(choice),"Yes")
		SkillSell.addoption(0,"No")
		popuplib.send(Menu_Name,userid)

def FinishSell(userid,choice,popupid):
	steamid = es.getplayersteamid(userid)
	if "YES_" in choice:
		key = choice.replace("YES_","")
		if int(es.keygetvalue('main',steamid,key)) > 0:
			lvl = int(es.keygetvalue('main',steamid,key))
			sellprice = int(int(int(es.keygetvalue("skills",key,'mod')) * (int(lvl)-1)+int(es.keygetvalue("skills",key,'mod')))*.9)
			es.tell(userid,"#multi","#default[#greenBlueRpg#default]: You sold #greenone#default level in #green%s#default for $#green%s#default."%(key,sellprice))
			es.keysetvalue('main',steamid,'Balance',int(int(es.keygetvalue('main',steamid,'Balance'))+sellprice))
			es.keysetvalue('main',steamid,key,(int(lvl)-1))
			es.tell(userid,"#multi","#default[#greenBlueRpg#default]: You are now level #green%s#default in %s"%(int(lvl)-1,key))
			s_track("Players","Skills Sold")

def shop():
	global Shop_Master
	userid = es.getcmduserid()
	Make_Green(userid,'!shop')
	Shop_Master.userid = userid
	Shop_Master.handle()
	s_track("Players","Shop Menus Opened")

class Shop_Menu():
	def handle(self):
		self.name = es.getplayername(self.userid)
		self.steamid = es.getplayersteamid(self.userid)
		self.balance = int(es.keygetvalue('main',self.steamid,'Balance'))
		self.xp = int(es.keygetvalue('main',self.steamid,'Xp'))
		self.level = int(es.keygetvalue('main',self.steamid,'Level'))
		self.weapon = playerlib.getPlayer(self.userid).get('weapon')
		self.general_menu()

	def general_menu(self):
		name = "Shop_General"+str(self.userid)
		shopmenu = popuplib.create(name)
		shopmenu.addline("BlueRpg - Shop!")
		shopmenu.addline('Balance| $%s'%self.balance)
		shopmenu.addline('->1.Weapons')
		shopmenu.addline('->2.Buffs')
		shopmenu.addline('->3.Skills')
		shopmenu.addline('->4.Stats')
		shopmenu.addline('->5.VoteCar')
		shopmenu.addline('->6.SellSkills')
		shopmenu.addline('->7-10. Cancel')
		shopmenu.menuselect = genselect
		# on the fly creation
		shopmenu.submenu(1,self.menu("weapons","BlueRpg - Weapons!"))
		shopmenu.submenu(2,self.menu("buffs","BlueRpg - Buffs!"))
		shopmenu.submenu(3,self.menu("skills","BlueRpg - Skills!"))
		shopmenu.submenu(4,self.statsmenu())
		popuplib.send(name,self.userid)

	def menu(self,key,menu_title):
		self.m_name = str(key)+str(self.userid)
		menu = popuplib.easymenu(self.m_name,'popup_choice',HandleBuy)
		menu.settitle(menu_title)
		menu.setdescription("Balance| $%s"%self.balance)
		if str(key) == "skills":
			menu.addoption("Skill Help","Skill Help")
		for item in (keyvalues.getKeyGroup(key)):
			if int(item['level']) <= self.level:
				if not str(key) == "skills":
					menu.addoption(str(item)+'|'+str(key),str(str(item)+' $'+str(es.keygetvalue(key,item,'price'))).capitalize())
				else:
					if int(es.keygetvalue('main',self.steamid,item)) < int(es.keygetvalue(key,item,'max')):
						price = (int(es.keygetvalue(key,item,'mod')) * int(es.keygetvalue('main',self.steamid,item)))+int(es.keygetvalue(key,item,'mod'))
						menu.addoption(str(item)+'|'+str(key),str(str(item)+' $'+str(price)))
					else:
						menu.addoption(None,str(str(item)+' Maxed Out'),0)
		return(self.m_name)

	def statsmenu(self):
		menu = popuplib.easymenu("Stats"+str(self.userid),'popup_choice',HandleBuy)
		menu.settitle("%s's Stats"%self.name)
		key = keyvalues.getKeyGroup('main')

		menu.addoption(None,"Level Progress - "+str(int(100*self.xp/(max(self.level,1)*350)))+"%")
		for item in (key [self.steamid]):
			menu.addoption(None,str(item)+": "+str(key[self.steamid][str(item)]))
		return("Stats"+str(self.userid))

def genselect(userid,choice,popupid):
	if choice == 5:
		es.cexec(userid,'!votecar')
		s_track("Players","VoteCar Votes")
	if choice == 6:
		es.cexec(userid,'!sellskill')

def HandleBuy(userid,choice,popupid):
	global Multipliers
	steamid = es.getplayersteamid(userid)
	if choice and choice != None and choice != "None" and choice != "Skill Help":
		spliter = str(choice).split('|')
		group = str(spliter[1])
		key = str(spliter[0])
		level = es.keygetvalue(group,key,"level")
		allow = Rpg_Math(group,key,userid)
		if allow == 1:
			if group == "skills":
				S_level = int(es.keygetvalue('main',steamid,key))+1
				es.keysetvalue('main',steamid,key,S_level)
			else:
				if group == 'weapons':
					if str(key) == "suit":
						es.give(userid,'item_suit')

					elif str(key) == "frags_6":
						es.give(userid,'weapon_frag')
						for i in range(1,6):
							es.give(userid,'item_ammo_frag')

					elif str(key) == "slams_3":
						for i in range(1,3):
							es.give(userid,'weapon_slam')
					else:
						wep = 'weapon_'+str(key)
						es.give(userid,wep)
						prop = es.keygetvalue('weapons',str(key),'prop')
						ammo = int(es.getplayerprop(userid,prop))+int(2*Multipliers[wep])
						es.setplayerprop(userid,prop,ammo)

						if str(wep) == "weapon_ar2" or str(wep) == "weapon_smg1":
							if str(wep) == "weapon_ar2":
								prop = "CHL2MP_Player.baseclass.baseclass.m_iAmmo.022"
							if str(wep) == "weapon_smg1":
								prop = "CHL2MP_Player.baseclass.baseclass.m_iAmmo.009"
							ammo = int(es.getplayerprop(userid,prop))+1
							if ammo < 2:
								es.setplayerprop(userid,prop,ammo)

				if group == 'buffs':
					global Buff_User
					Buff_User.userid = userid
					Buff_User.block = str(key).lower()
					Buff_User.handle()
	elif choice == "Skill Help":
		es.cexec(userid,'!skillhelp')

#This simply handles and informs the user of purchases, no giving items.
def Rpg_Math(group,key,userid):
	steamid = es.getplayersteamid(userid)
	balance = int(es.keygetvalue('main',steamid,'Balance'))
	if group == "skills":
		price = int(es.keygetvalue(group,key,'mod')) * int(es.keygetvalue('main',steamid,key))+int(es.keygetvalue(group,key,'mod'))
	else:
		price = int(es.keygetvalue(group,key,"price"))
	if balance < price:
		es.tell(userid,"#multi","#default[#greenBlueRpg#default]: You don't have enough #greenmoney#default!")
		return(0)
	else:
		if group == "skills":
			if int(es.keygetvalue('main',steamid,key)) < int(es.keygetvalue('skills',key,'max')):
				es.keysetvalue('main',steamid,'Balance',int(balance - price))
				TellAll("[#greenBlueRpg#default]: #green%s#default - Bought #green%s#default Level #green%s#default."%(es.getplayername(userid),key,int(es.keygetvalue('main',steamid,key))+1))
				return(1)
			else:
				es.tell(userid,"#multi","#default[#greenBlueRpg#default]: You've #greenmaxed#default out your #green%s#default skill!"%(key))
				return(2)
		else:
			TellAll("[#greenBlueRpg#default]: #green%s#default - Bought #green%s#default."%(es.getplayername(userid),key))
			es.keysetvalue('main',steamid,'Balance',int(balance -price))
		return(1)


# The only fully and mostly untoched system from origional money (Also the latest and last addition to money)
class buff_master():
	def handle(self):
		s_track("Players","Buffs Bought")
		self.steamid = es.getplayersteamid(self.userid)
		exec("a=self."+self.block+"()")

	def generic_timer(self,time,block,userid):
		if es.exists('userid',self.userid):
			delayname = str(self.steamid)+str(block)
			Bluethread.cancelDelayed(delayname)
			Bluethread.delayedname(time,delayname,block,userid)
		else:
			Bluethread.cancelDelayed(delayname)

	def explosivekills(self):
		global Explosive_kills
		Explosive_kills.append(self.userid)
		usermsg.fade(self.userid, 2, 4,96000,100,0,0,50)
		es.tell(self.userid,'#multi','#default[#greenBlueRpg#default]: Everything you kill within 60 seconds will now explode.')
		es.emitsound("player",self.userid,str("vo/npc/barney/ba_goingdown.wav"),1,0)
		es.menu(5,self.userid,"Explosive kills has started.")
		#(This timer can let the player buy a new buff in the same timeframe of the old and not have the new effect ended by the old timer)
		self.generic_timer(120,self.explosivekills_end,self.userid)

	def explosivekills_end(self,userid):
		global Explosive_kills
		Explosive_kills.remove(self.userid)
		es.tell(userid,'#multi','#default[#greenBlueRpg#default]: Explosive kills has worn off.')
		es.menu(5,userid,"Explosive kills has ended.")

	def npcstealth(self):
		usermsg.fade(self.userid, 2, 5,55000,0,0,0,120)
		es.server.queuecmd('cheatexec %s notarget'%self.userid)
		es.tell(self.userid,'#multi',"#green[Mavs]#default: You have 35 seconds of cloak, Npcs can't see you!")
		es.fire(self.userid,'!self',"addoutput","renderfx 3")
		es.menu(5,self.userid,"You are now cloaked to npcs!")
		es.emitsound("player",self.userid,str("vo/npc/male01/okimready03.wav"),1,0)
		self.generic_timer(35,self.npcstealth_end,self.userid)

	def npcstealth_end(self,userid):
		es.tell(userid,'#multi',"#default[#greenBlueRpg#default]: Your cloak has worn off! NPCs can now see you!")
		es.fire(userid,'!self',"addoutput", "renderfx 7")
		es.menu(5,userid,"You are no longer cloaked to NPCs!")
		es.server.queuecmd('cheatexec %s notarget'%self.userid)

	def health(self):
		es.server.queuecmd("es playerset healthadd %s 100"%self.userid)

	def speedboost(self):
		es.server.queuecmd("es playerset speedadd %s 0.5"%self.userid)

	def jetpack(self):
		es.keysetvalue('main',self.steamid,'jetpacks',int(es.keygetvalue('main',self.steamid,'Jetpacks'))+2)
		es.tell(self.userid,'#multi',"#default[#greenBlueRpg#default]: #green!jetpack#default in chat to #greenactivate #defaultthe #greenjetpack#default.")

	def ammo(self):
		wep = playerlib.getPlayer(self.userid).get('weapon')
		wep = str(wep).replace('weapon_','')
		if  wep != "crowbar" and wep != "stunstick" and wep  != "physcannon":
			if wep == 'frag':
				wep = 'frags_6'
			elif wep == 'slam':
				wep = 'slams_18'
			ammo = es.keygetvalue('weapons',wep,'ammo')
			es.give(self.userid,ammo)
			self.giveammo(ammo)

	def giveammo(self,ammo):
		es.give(self.userid,ammo)
		Bluethread.delayed(0.1,es.give,(self.userid,ammo))
		Bluethread.delayed(0.2,es.give,(self.userid,ammo))
		Bluethread.delayed(0.3,es.give,(self.userid,ammo))


class SprintRecharge():
	def handle(self):
		self.steamid = es.getplayersteamid(self.userid)
		if int(es.keygetvalue('main',self.steamid,"Sprint Recharger")) > 1:
			Bluethread.cancelDelayed(str(self.steamid)+'SPRINTRECHARGE')
			Bluethread.delayedname(5,str(self.steamid)+'SPRINTRECHARGE',self.charge,self.userid)

	def charge(self,userid):
		if es.exists('userid',userid):
			steamid = es.getplayersteamid(userid)
			Bluethread.cancelDelayed(str(steamid)+'SPRINTRECHARGE')
			Bluethread.delayedname(7,str(steamid)+'SPRINTRECHARGE',self.charge,userid)
			power = int((int(es.keygetvalue('main',steamid,"Sprint Recharger"))*7)+int(es.getplayerprop(userid,"CHL2MP_Player.baseclass.m_HL2Local.m_flSuitPower")))+5
			if int(power) >= 100:
				es.setplayerprop(userid,"CHL2MP_Player.baseclass.m_HL2Local.m_flSuitPower",100)
			else:
				es.setplayerprop(userid,"CHL2MP_Player.baseclass.m_HL2Local.m_flSuitPower",power)

class Health_Regen():
	def handle(self):
		self.steamid = es.getplayersteamid(self.userid)
		if int(es.keygetvalue('main',self.steamid,"Health Regen")) > 0:
			Bluethread.cancelDelayed(str(self.steamid)+'HEALTHREGEN')
			Bluethread.delayedname(60/int(es.keygetvalue('main',self.steamid,"Health Regen")),str(self.steamid)+'HEALTHREGEN',self.heal,self.userid)

	def heal(self,userid):
		if es.exists('userid',userid):
			steamid = es.getplayersteamid(userid)

			Bluethread.cancelDelayed(str(steamid)+'HEALTHREGEN')
			Bluethread.delayedname(60/int(es.keygetvalue('main',steamid,"Health Regen")),str(steamid)+'HEALTHREGEN',self.heal,userid)

			plr = playerlib.getPlayer(userid)
			St_Health = int(plr.get('health'))
			if not plr.get('isdead') and St_Health <= 120:
				health = St_Health+int(es.keygetvalue('main',steamid,'Health Regen'))
				if health > 120:
					plr.set('health',120)
				else:
					plr.set('health',health)

class Ammo_Regen():
	global Multipliers
	def handle(self):
		self.steamid = es.getplayersteamid(self.userid)
		if int(es.keygetvalue('main',self.steamid,"Ammo Regen")) > 0:
			Bluethread.cancelDelayed(str(self.steamid)+'AMMOREGEN')
			Bluethread.delayedname(15-int(es.keygetvalue('main',self.steamid,"Ammo RegenRate")),str(self.steamid)+'AMMOREGEN',self.supply,self.userid)
	#This code is quite unchanged, not a lot to do to it.
	def supply(self,userid):
		steamid = es.getplayersteamid(userid)
		if es.exists('userid',userid):

			Bluethread.cancelDelayed(str(steamid)+'AMMOREGEN')
			Bluethread.delayedname(15-int(es.keygetvalue('main',steamid,"Ammo RegenRate")),str(steamid)+'AMMOREGEN',self.supply,userid)

			plr = playerlib.getPlayer(userid)
			if not plr.get('isdead'):
				addammo = int(es.keygetvalue('main',steamid,'Ammo Regen'))
				wep = str(plr.get('weapon'))
				if addammo != 0 and addammo != None and wep != 'None' and wep != None:


					AmmoLimits = {"weapon_mg1":200,"weapon_pistol":100,"weapon_mp5k":250,"weapon_357":12,"weapon_deagle":12,"weapon_crossbow":10,"weapon_shotgun":30,"weapon_rpg":3,"weapon_smg1":150,"weapon_ar2":120,"weapon_frag":3,"weapon_slam":5}
					if wep != "weapon_crowbar" and wep != "weapon_stunstick" and wep != "weapon_physcannon" and wep != "weapon_bugbait" and "frag" not in wep and "slam" not in wep:
						if wep == "weapon_crossbow"	and addammo > 1:
							addammo = addammo/2

						prop = es.keygetvalue('weapons',str(wep).replace("weapon_",""),'prop')
						ammo = int(es.getplayerprop(userid,prop))+int(addammo*Multipliers[wep])
						if ammo >= AmmoLimits[wep]:
							ammo = AmmoLimits[wep]
						es.setplayerprop(userid,prop,ammo)

						if wep == "weapon_ar2" or wep == "weapon_smg1":
							if wep == "weapon_ar2":
								prop = "CHL2MP_Player.baseclass.baseclass.m_iAmmo.022"
							if wep == "weapon_smg1":
								prop = "CHL2MP_Player.baseclass.baseclass.m_iAmmo.009"
							ammo = int(es.getplayerprop(userid,prop))+1
							if ammo < 2:
								es.setplayerprop(userid,prop,ammo)

#------------------------------------Plugin Unload Section ---------------------------------------

def unload():
	es.server.queuecmd("es_unload CaseDrop")
	es.remove("dis")
	#Rank chat filter
	es.addons.unregisterSayFilter(rankchat)

	#Halt all active Bluethreads (No errors! Nifty huh?)
	for item in Bluethread.getDelayed():
		Bluethread.cancelDelayed(item)
		#print("Halted Thread: "+str(item))

	#Unregister all Reg() commands.
	UnRegAll()

	try:
		votelib.delete('votecar')
	except ValueError:
		pass

	#Keygroup save / delete section.
	es.keygroupsave('main','|BlueRpg')
	es.keygroupsave('stats','|BlueRpg')
	es.keygroupdelete('main')
	es.keygroupdelete("skills")
	es.keygroupdelete("buffs")
	es.keygroupdelete("weapons")
	es.keygroupdelete("stats")
