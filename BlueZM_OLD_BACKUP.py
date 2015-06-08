import es
import gamethread
import playerlib,weaponlib
import math,random
import spe


def load():
	print("BlueZM Enabled")
	es.server.queuecmd("mp_restartgame 1")
	es.server.queuecmd("mp_autoteambalance 0")
	es.server.queuecmd("eventscripts_noisy 1")
	
#****************************************** Lists ******************************************
	global Zombies,Survivors,Spec
	Zombies = []
	Survivors = []
	Spec = []

#****************************************** Vars ******************************************
	#Grace period to ignore player deaths/roundswaps pregame.
	global Grace,Kicked_Bots,LastMan
	LastMan = 0
	Kicked_Bots = 0
	Grace = 1

#****************************************** Utility Blocks ******************************************
	es.addons.registerSayFilter(TeamChat)
	es.addons.registerClientCommandFilter(CommandFilter)

	gamethread.delayedname(.5,"Deplete_Infected_Ammo",Deplete_Infected_Ammo,())
	gamethread.delayedname(5,"Request_RoundType_Update",Request_RoundType_Update,())

	
def unload():
	es.addons.unregisterSayFilter(TeamChat)
	es.addons.unregisterClientCommandFilter(CommandFilter)
	gamethread.cancelDelayed("Grace")
	gamethread.cancelDelayed("Deplete_Infected_Ammo")
	gamethread.cancelDelayed("Request_RoundType_Update")
	gamethread.cancelDelayed("LastMan")
	gamethread.cancelDelayed("clock")

class Round_Manager:
	def __init__(self):
		# SD = Synergized Disinfection (Team Deathmatch), LMA = Last Man Alive, IF = Infection (Plop away we go)
		self.Types = ["SD","LMA"]

	def RM_ERROR(self,error):
		print("[Round Manager Error]: %s"%error)

	def SetRound(self,Type):
		if Type in self.Types:
			if Type == "SD":
				self.Prep_SD()
			if Type == "LMA":
				self.Prep_LMA()
		else:
			self.RM_ERROR("Unknown round type: %s"%Type)

	def RandomRound(self):
		self.RoundType = self.Types[random.randint(0,len(self.Types)-1)]
		if self.RoundType == "SD":
			self.Prep_SD()
		if self.RoundType == "LMA":
			self.Prep_LMA()

	def HandleRoundStart(self):
		if self.Type == "SD":
			pass 
		if self.Type == "LMA":
			pass 
			
		Msg("Handled Round Start: %s"%self.Type)

	def Prep_SD(self):
		pass
		
# The Game Manager (Round By Round)
RM = Round_Manager()


def CommandFilter(userid, args):
	for item in args:
		if "scout" in item or ("engineer" in item and es.getplayerteam(userid) == 2):
			return False
	return True

def color_correct(path,userid):
	#Constructer for Color Correction
	NAME = str("BLUEZM_COLOR_CORRECT")
	index = es.createentity('color_correction')
	es.setentityname(index,NAME)
	es.entitysetvalue(index,'fadeInDuration',0.1)
	es.entitysetvalue(index,'StartDisabled',1)
	es.entitysetvalue(index,'fadeOutDuration',0.1)
	es.entitysetvalue(index,'minfalloff',0)
	es.entitysetvalue(index,'maxfalloff',-1)
	es.entitysetvalue(index,'filename',str(path))
	es.entitysetvalue(index,'maxweight',.6)
	es.spawnentity(index)
	gamethread.delayed(2,es.fire,(userid,NAME,'enable'))
	Msg("Color Correction Enabled")
		
def CC_PREP(path):
	if es.getplayercount() > 0:
		userid = es.getUseridList()[0]
		es.fire(userid,"BLUEZM_COLOR_CORRECT",'kill')
		gamethread.delayed(1,color_correct,(path,userid))		

class Overlay:
	def __init__(self,path,duration):
		self.path = path 
		self.duration = duration
		self.NAME = "BLUEZM_OVERLAY"+str(path)
		self.Prep()
		
	def Prep(self):
		if es.getplayercount() > 0:
			es.fire(es.getUseridList()[0],"BLUEZM_OVERLAY",'kill')
			gamethread.delayed(.5,self.Overlay,())

	def Overlay(self):
		index = es.createentity('env_screenoverlay')
		es.setentityname(index,self.NAME)
		es.entitysetvalue(index,'OverlayTime1',self.duration)
		es.entitysetvalue(index,'OverlayName1',str(self.path))
		es.spawnentity(index)
		gamethread.queue(es.fire,(es.getUseridList()[0],self.NAME,'StartOverlays'))
		gamethread.delayed(self.duration,self.Shutdown,())

	def Shutdown(self):
		id = es.getUseridList()[0]
		es.fire(id,self.NAME,'StopOverlays')
		gamethread.queue(es.fire,(id,self.NAME,'kill'))

def TeamChat(userid, text, teamonly):
	text = str(str(text).strip('"'))
	if es.exists('saycommand',text.split(' ')[0]) or text.split(' ')[0].lower() in ["!vote","!kick","!ban","!tele","!teleport","!burn","!slay","!noclip","!beacon","!happy","!slap","!nominate","!rtv","rtv","/rtv","votekick","voteban","!votekick","!voteban","!me","/me"]:
		return (userid, text, teamonly)
	else:
		if es.getplayerteam(userid) == 1:
			return (userid, text, teamonly)
		if es.getplayerteam(userid) == 2:
			es.msg('#multi','[#greenInfected#default] %s: #default%s'%(es.getplayername(userid),text))
		if es.getplayerteam(userid) == 3:
			es.msg('#multi','[#greenSurvivor#default] %s: #default%s'%(es.getplayername(userid),text))
		es.cexec_all('play common/talk.wav')
		return (0, None, None)

def Msg(msg):
	name = "#default[#greenBlueZM#default]"
	es.msg("#multi","%s: %s"%(name,msg))
	

def Request_RoundType_Update():
	global Grace,LastMan
	Infect = es.getplayercount(2) 
	Surv = es.getplayercount(3)
	if not Grace and not LastMan:
		if not (Infect == 1 and Surv == 1):
			if Infect == 1:
				LastMan_Enable(2)
			if Surv == 1:
				LastMan_Enable(3)
	gamethread.delayedname(5,"Request_RoundType_Update",Request_RoundType_Update,())

def LastMan_Enable(Team):
	global LastMan,ClockTime
	ClockTime = 30
	LastMan = 1
	Teams = {2:"Infected",3:"Survivors"}
	Name = Teams[Team]
	Msg("TimeLimit Enabled! #green%s#default Seconds before #green%s#default lose!"%(30,Name))
	gamethread.delayedname(30,"LastMan",ForceLose,(Team))
	gamethread.delayedname(1,"clock",Clock,())

def Clock():
	global ClockTime
	if int(ClockTime) <= 2:
		gamethread.cancelDelayed("clock")
	if int(ClockTime) > 9:
		es.emitsound("player", es.getUseridList()[0],"pl_hoodoo\\alarm_clock_ticking_3.wav", 1, 0)
		gamethread.delayedname(2.7,"clock",Clock,())
		ClockTime -= 3 
	else:
		Msg("Ten Seconds To Sudden Death!")
		es.emitsound("player", es.getUseridList()[0],"pl_hoodoo\\alarm_clock_alarm_3.wav", 1, 0)
		gamethread.cancelDelayed("clock")
		ClockTime = 0
			
def ForceLose(Team):
	es.server.queuecmd("mp_forcewin %s"%(Team))
	
def Request_SetPlayerMaxHealth(Userid,Health):
	for item in es.createentitylist("tf_player_manager"):
		Ent = item
		break
	index = int(playerlib.getPlayer(Userid).get('index'))
	Template = GetTemplate(str("CTFPlayerResource.m_iMaxHealth.0"),index)
	es.setindexprop(Ent,Template,Health)
	es.setplayerprop(Userid,"CTFPlayer.baseclass.baseclass.m_bGlowEnabled",1)
	es.setplayerprop(Userid,"CTFPlayer.baseclass.m_flMaxspeed",random.randint(300,400))
	
def GetTemplate(Temp,index):
	Template = str(Temp)
	if index > 9:
		Template += str(index)
	else:
		Template += "0"+str(index)
	return(Template)
		
def Request_TeamUpdate():
	#Lets move the players to their respecive teams.
	#1 = Spectator, 2 = Infected, 3 = Survivors 
	global Zombies,Survivors,Spec,Grace
		
	for Userid in Zombies:
		if es.exists('userid',Userid):
			if es.getplayerteam(Userid) != 2:
				es.changeteam(Userid,2)
		else:
			Zombies.remove(Userid)

	for Userid in Survivors:
		if es.exists('userid',Userid):
			if es.getplayerteam(Userid) != 3:
				es.changeteam(Userid,3)
		else:
			Survivors.remove(Userid)

	for Userid in Spec:
		if es.exists('userid',Userid):
			if es.getplayerteam(Userid) != 1:
				es.changeteam(Userid,1)
		else:
			Spec.remove(Userid)


	if es.getplayercount() > 1 and not Grace:
		if int(es.getplayercount(2)) == 0:
			es.server.queuecmd("sv_cheats 1")
			es.server.queuecmd("mp_forcewin 3")
			gamethread.delayed(.2,es.server.queuecmd,("sv_cheats 0"))

		if int(es.getplayercount(3)) == 0:
			es.server.queuecmd("sv_cheats 1")
			es.server.queuecmd("mp_forcewin 2")
			gamethread.delayed(.2,es.server.queuecmd,("sv_cheats 0"))
	elif es.getplayercount() == 1:
		if not es.isbot(es.getUseridList()[0]):
			es.server.queuecmd("tf_bot_add")
			es.server.queuecmd("tf_bot_add")
			Msg("Well this looks boring, lets throw some bots in.")
					
def Request_Prep_NewPlayer(Userid):
	global Zombies,Survivors,Spec,Grace,Kicked_Bots
	if Userid not in Zombies and Userid not in Survivors and Userid not in Spec:
		if not Grace:
			if not es.isbot(Userid):
				Spec.append(Userid)
			else:
				es.server.queuecmd("tf_bot_kick %s"%es.getplayername(Userid))
				Kicked_Bots += 1
		else:
			Zombify_Cheap(Userid)
	Request_TeamUpdate()
			
def Request_Spectate(Userid):
	global Kicked_Bots,Spec,Zombies,Survivors
	if es.exists('userid',Userid):
		if es.isbot(Userid):
			name = es.getplayername(Userid)
			es.server.queuecmd("tf_bot_kick %s"%name)
			Kicked_Bots += 1 
			Msg("%s Moved to [Bot Spectator]."%name)
		else:
			if Userid in Zombies:
				Zombies.remove(Userid)
			if Userid in Survivors:
				Survivors.remove(Userid)
			if Userid not in Spec:
				Spec.append(Userid)
			es.changeteam(Userid,1)
	else:
		Request_ClearData(Userid)
		
def Request_ClearData(Userid):
	global Zombies,Survivors,Spec
	if Userid in Zombies:
		Zombies.remove(Userid)
	if Userid in Survivors:
		Survivors.remove(Userid)
	if Userid in Spec:
		Spec.remove(Userid)
	
	Request_TeamUpdate()

def Reset():
	global Zombies,Survivors,Spec,Grace,LastMan
	LastMan = 0
	Grace = 1
	Zombies = []
	Survivors = []
	Spec = []
	
def Grace_Off():
	global Grace 
	Msg("Grace Period Is Over.")
	Grace = 0
	gamethread.cancelDelayed("Grace")
	
	if es.getplayercount() > 0:
		Userid = es.getUseridList()[0]
		es.fire(Userid,"func_regenerate","setteam",1)
		es.fire(Userid,"func_regenerate","TeamNum",1)
		es.fire(Userid,"func_respawnroomvisualizer","solid_to_enemies",0)
		Msg("Survivor Ammo Lockers Disabled, Spawnroom Guards Disabled")

#****************************************** Zombie Related Blocks ******************************************
def Zombify_Random():
	global Zombies,Survivors,Spec
	for Userid in es.getUseridList():
		es.changeteam(Userid,3)

	Needed = abs(int(round(int(es.getplayercount())*.3)))
	if Needed > 1:
		Msg("Infecting %s Players:"%Needed)
	elif Needed < 0:
		Msg("Infecting 1 Player:")
		Needed = 1
	if Needed > 0:
		Total = 0
		while(Needed > Total):
			Userid = es.getUseridList()[random.randint(0,es.getplayercount()-1)]
			if es.getplayerteam(Userid) == 3 and Userid not in Zombies:
				Zombies.append(Userid)
				Total += 1
		for Userid in es.getUseridList():
			if Userid not in Zombies:
				Survivors.append(Userid)
		Request_TeamUpdate()
		list = ""
		size = int(len(Zombies))
		if size > 1:
			for id in Zombies:
				size -= 1
				list += es.getplayername(id)
				if size == 1:
					list += ", and "
				
				if int(size) > 1:
					list += ", "
				else:
					list += " "
			Msg("%s have been zombified!"%list)
		elif size != 0:
			list = es.getplayername(int(Zombies[0]))
			Msg("%s has been zombified!"%list)
		Msg("Infected will Spawn with %s health. (Based on total Infected)"%(4000/int(es.getplayercount(2))+1500))
		
def Zombify_Cheap(Userid):
	global Zombies,Survivors,Grace
	es.changeteam(Userid,3)
	Needed = int(round(int(es.getplayercount(3))*.3))-int(es.getplayercount(2))
	if Grace:
		if int(Needed) > 0:
			Zombies.append(Userid)
			es.changeteam(Userid,2)
		else:
			Survivors.append(Userid)
			es.changeteam(Userid,3)
	else:
		Request_Spectate(Userid)
	
#****************************************** Player Events ******************************************
def player_death(EV):
	Userid = int(EV['userid'])
	global Zombies,Survivors,Spec,Grace,Kicked_Bots
	if Grace == 0:
		#Zombie to Spectator
		if es.getplayerteam(Userid) == 2:
			if Userid in Zombies:
				Zombies.remove(Userid)
			Request_Spectate(Userid)

		#Survivor to Zombie 
		if es.getplayerteam(Userid) == 3 and EV["attacker"] != Userid:
			if Userid in Survivors:
				Survivors.remove(Userid)
			Zombies.append(Userid)
			es.changeteam(Userid,2)
			Msg("%s Was Zombified by %s!"%(es.getplayername(Userid),es.getplayername(EV['attacker'])))
	Request_TeamUpdate()
	
def player_changeclass(EV):
	Request_WeaponKill_Update()

def player_activate(EV):
	Request_Prep_NewPlayer(EV['userid'])

def Request_WeaponKill_Update():
	# 1 = scout, 2 = sniper, 3 = soldier, 4 = demo, 5 = medic, 6 = heavy, 7 = pyro, 8 = spy, 9 = engie   	
	Userid = es.getUseridList()[0]
	for item in ["tf_weapon_builder","tf_weapon_pda_engineer_build","tf_weapon_pda_engineer_destroy","tf_weapon_pda_spy","tf_weapon_invis"]:
		es.fire(Userid,item,"kill")
		

# Remove Remaining Weapon Chamber Ammo.
def Kill_InfectedClip(Userid):
	handle = es.getplayerhandle(Userid)
	List = es.createentitylist()
	for index in List:
		if "tf_weapon" in List[index]["classname"]:
			for item in List[index]:
				if "clip" in str(item).lower():
					if es.getindexprop(index,'CBaseEntity.m_hOwnerEntity') == handle:
						es.setindexprop(index,item,0)
# Remove Reserve Ammo
def Deplete_Infected_Ammo():
	gamethread.delayedname(.5,"Deplete_Infected_Ammo",Deplete_Infected_Ammo,())
	for Userid in es.getUseridList():
		if es.exists('userid',Userid):
			if es.getplayerteam(Userid) == 2:
				es.setplayerprop(Userid,"CObjectTeleporter.baseclass.m_iUpgradeMetal",0)
				for num in range(4):
					es.setplayerprop(Userid,"CTFPlayer.baseclass.localdata.m_iAmmo.00%s"%num,0)

def player_spawn(EV):
	Userid = int(EV['userid'])
	Team = EV['team']
	Class = EV['class']
	global Zombies,Survivors,Spec
	Request_WeaponKill_Update()
	if Userid in Zombies:
		Kill_InfectedClip(Userid)
		es.setplayerprop(Userid,"CTFPlayer.baseclass.m_iHealth",(4000/es.getplayercount(2))+1000)
		Request_SetPlayerMaxHealth(Userid,(4000/es.getplayercount(2))+1000)
	Request_TeamUpdate()
	
def teamplay_round_win(EV):
	global Grace,Kicked_Bots,ClockTime
	ClockTime = 0
	if int(Kicked_Bots) > 0:
		for num in range(Kicked_Bots):
			es.server.queuecmd("tf_bot_add")
		Kicked_Bots = 0
	Grace = 1
	gamethread.cancelDelayed("Grace")
	gamethread.cancelDelayed("LastMan")
	gamethread.cancelDelayed("clock")
	
	
def teamplay_round_active(EV):
	RM.SetRound("SD")
	
	gamethread.delayed(1.5,Overlay,("BlueZM/synergized_Disinfection.vtf",4))
	if es.getplayercount() > 0:
		Userid = es.getUseridList()[0]
		es.fire(Userid,"func_regenerate","setteam",3)
		es.fire(Userid,"func_regenerate","TeamNum",3)
		es.fire(Userid,"func_respawnroomvisualizer","solid_to_enemies",1)
		es.fire(Userid,"trigger_capture_area","area_time_to_cap",500)
		Reset()
		Zombify_Random()
		gamethread.delayedname(50, "Grace", Grace_Off)
		Request_TeamUpdate()
	
def player_disconnect(EV):
	Request_ClearData(EV['userid'])
