import logging
import dateutil.parser

from scrapy import signals
from scrapy.exporters import XmlItemExporter

class MobygamesPipeline(object):

#	global adult_ratings
#	adult_ratings = ['18', 'Adults Only']
#	global licensed
#	licensed = [u'Licensed\xa0Title']
	
	global group_addon
	group_addon = "extension"
	
	global group_anatomy
	group_anatomy = "Anatomie"
	
	global group_astronomy
	group_astronomy = "Astronomie"		
	
	global group_comic
	group_comic = "Bande Dessinee"
	
	global group_bowling
	group_bowling = "bowling"

	global group_boxing
	group_boxing = "boxe"
	
	global group_cluedo
	group_cluedo = "cluedo"
	
	global group_coinop
	group_coinop = "coin-op"
	
	global group_chess
	group_chess = "echec"	
	
	global group_flipper
	group_flipper = "flipper"		
	
	global group_football
	group_football = "football"	

	global group_snooker		
	group_snooker = "snooker"	
	
	global group_isometric
	group_isometric = "3D iso"		
	
	global group_mastermind
	group_mastermind = "STYLE : mastermind"			

	global group_othello
	group_othello = "STYLE : othello"

	global group_qbert
	group_qbert = "STYLE : qbert"
			
	global groups_map	
	groups_map = {		
		"female protagonist": "Protagonist: Female",		
		"Hardware double buffer" : "Hardware: double buffering",
		"extended RAM" : "Hardware: Extended RAM",
		"Scroll Hard horizontal" : "Hardware: Horizontal scrolling",
		"Scroll Hard vertical" : "Hardware: Vertical scrolling",
		"Scroll Hard multidirectional" : "Hardware: Multidirectional scrolling",
		"Software Scroll" : "Software scrolling",
		"Parallax Scroll" : "Parallax scrolling",
		"Multi-Mode" : "Display: Multi-Mode",
		"Dual Playfield" : "Display: Dual Playfield",
		"MODE0 titlescreen" : "Display: MODE0 Title Screen",
		"MODE1 titlescreen" : "Display: MODE1 Title Screen",
		"MODE2 titlescreen" : "Display: MODE2 Title Screen",
		"MODE0 inside" : "Display: MODE0 In Game",
		"MODE1 inside" : "Display: MODE1 In Game",
		"MODE2 inside" : "Display: MODE2 In Game",
		"MODE1 special" : "Display: MODE1 Raster",
		"Overscan full" : "Display: Full Overscan",
		"Overscan horizontal" : "Display: Horizontal Overscan",
		"Overscan vertical" : "Display: Vertical Overscan",
		"Biggerscreen" : "Display: Big Screen",
		"Smallscreen" : "Display: Small Screen",
		"Normalscreen Smalldisplay" : "Display: Normal Screen",
		"Bande Dessinee" : "Inspiration: Comics",
		"blitz" : "Blitz variants",
		"Dessin Animee" : "Inspiration: TV cartoons",
		"film" : "Inspiration: Movies",
		"livre" : "Inspiration: Literature",
		"memory" : "Concentration variants",
		"serie tv" : "Inspiration: TV series",
		"Speccy Port" : "Speccy Port",
		"STYLE : boulder dash" : "Boulder Dash variants",
		"STYLE : check man" : "Check Man variants",
		"STYLE : marble madness" : "Genre: Rolling ball",
		"STYLE : pac-man" : "Pac-Man variants",
		"STYLE : pingo" : "Pengo variants",	
		"STYLE: puzznic" : "Genre: Tile matching puzzle (creation)",
		"simon" : 'Gameplay feature: "Simon says"',
		"STYLE : tetris" : "Tetris variants",
		"STYLE : tron" : "Genre: Light Cycle",
		"STYLE : yam" : "Yahtzee variants",
		"extension" : group_addon,
		"Anatomie" : group_anatomy,
		"Astronomie" : group_astronomy,
		"bowling" : group_bowling,
		"cluedo" : group_cluedo,
		"coin-op" : group_coinop,
		"echec" : group_chess,
		"flipper" : group_flipper,
		"football" : group_football,
		"snooker" : group_snooker,
		"3D iso" : group_isometric,
		"STYLE : mastermind" : group_mastermind,
		"STYLE : othello" : group_othello,
		"STYLE : qbert" : group_qbert
						
	}
		
	global game_breakout
	game_breakout = "GAME -> Breakout";

	global game_fight
	game_fight = "GAME -> Fight";

	global game_management
	game_management = "GAME -> Management";
		
	global game_arcade
	game_arcade = "GAME -> Arcade";
	
	global game_platform
	game_platform = "GAME -> Platformer";	
	
	global game_quiz
	game_quiz = "GAME -> Quiz";

	global game_shmup
	game_shmup = "GAME -> Shoot'Em Up";

	global game_targetshooting	
	game_targetshooting	 = "GAME -> Target shooting";

	global game_edu_history_geography
	game_edu_history_geography = "EDUCATIONAL -> History, Geography";
	
	global game_edu_math
	game_edu_math = "EDUCATIONAL -> Maths, Geometry";

	global game_edu_grammar
	game_edu_grammar = "EDUCATIONAL -> spelling, Grammar";
			
	global genres_map		
	genres_map = {
		"GAME -> Reflexion": "Puzzle",
		"GAME -> Action": "Action",
		"GAME -> Adventure": "Adventure",
		"GAME -> Race" : "Racing / Driving",
		"GAME -> Management" : "Strategy/Tactics",	
		"GAME -> Role-playing" : "Role-Playing (RPG)",
		"GAME -> Maze" : "Puzzle",
		"GAME -> Run & Gun" : "Action",
		"GAME -> Simulation" : "Simulation",
		"GAME -> Sport" : "Sports",
		"GAME -> Strategy" : "Strategy/Tactics",
		"EDUCATIONAL -> Course, Tutorial" : "Educational",
		"EDUCATIONAL -> Other" : "Educational",
		game_arcade : "Action",
		game_breakout : "Action",
		game_fight : "Action",
		game_management : "Strategy/Tactics",
		game_platform : "Action",
		game_quiz : "Puzzle",
		game_shmup : "Action",
		game_targetshooting : "Action",
		game_edu_history_geography : "Educational",
		game_edu_math : "Educational",
		game_edu_grammar : "Educational"
	}

	global players_map		
	players_map = {
		"1 player": "Single Player",
		"2 alternating players": "2-Player Alternating",
		"3 alternating players": "3-Player Alternating",
		"4 alternating players": "4-Player Alternating",
		"5 alternating players": "5-Player Alternating",
		"6 alternating players": "6-Player Alternating",
		"7 alternating players": "7-Player Alternating",
		"8 alternating players": "8-Player Alternating",
		"9 alternating players": "9-Player Alternating",
		"10 alternating players": "10-Player Alternating",
		"2 simultaneous cooperating players" : "2-Player Simultaneous;Cooperative",
		"3 simultaneous cooperating players" : "3-Player Simultaneous;Cooperative",
		"4 simultaneous cooperating players" : "4-Player Simultaneous;Cooperative",
		"5 simultaneous cooperating players" : "5-Player Simultaneous;Cooperative",
		"6 simultaneous cooperating players" : "6-Player Simultaneous;Cooperative",
		"7 simultaneous cooperating players" : "7-Player Simultaneous;Cooperative",
		"8 simultaneous cooperating players" : "8-Player Simultaneous;Cooperative",
		"9 simultaneous cooperating players" : "9-Player Simultaneous;Cooperative",
		"10 simultaneous cooperating players" : "10-Player Simultaneous;Cooperative",
		"2 simultaneous opposing players" : "2-Player Simultaneous;Versus",
		"3 simultaneous opposing players" : "3-Player Simultaneous;Versus",
		"4 simultaneous opposing players" : "4-Player Simultaneous;Versus",
		"5 simultaneous opposing players" : "5-Player Simultaneous;Versus",
		"6 simultaneous opposing players" : "6-Player Simultaneous;Versus",
		"7 simultaneous opposing players" : "7-Player Simultaneous;Versus",
		"8 simultaneous opposing players" : "8-Player Simultaneous;Versus",
		"9 simultaneous opposing players" : "9-Player Simultaneous;Versus",
		"10 simultaneous opposing players" : "10-Player Simultaneous;Versus",
	}
	
	def __init__(self):
		self.files = {}
	
	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline
	  	 	 	 	 
	def spider_opened(self, spider):
		file = open(spider.settings['FILES_STORE'] + '/%s.xml' % 'export', 'w+b')
		self.files[spider] = file
		self.exporter = XmlItemExporter(file,item_element='game', root_element='games')
		self.exporter.start_exporting()
		return
  	 	 	 	 				
	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()
		return

	def process_item(self, item, spider):
		logging.info("Exporting item:" + item['title'])
		
		# do not export utility fields
		# pop them from item dict
		#~ item.pop("search_num", None)
		#~ item.pop("search_title", None)
		
		item.pop("screenshot_urls", None)
		item.pop("image_urls", None)
						
		# initialize arrays if needed
		self.initKey(item, 'gameplay')
		self.initKey(item, 'group')
		self.initKey(item, 'educational')
		self.initKey(item, 'addon')
		self.initKey(item, 'sport')
		self.initKey(item, 'narrative')
		self.initKey(item, 'visual')
		self.initKey(item, 'pacing')
			
		########################
		###### MAP GROUPS ######
		if 'group' in item.keys() and item['group']:
			groupslist = item['group'].split(";")
			newgroupslist = []
			for g in groupslist:								
				mappedgroup = self.map_group( g );								
				if mappedgroup:					
					if mappedgroup == group_addon:
						item['addon'].append('Map / Level')
					elif mappedgroup == group_anatomy:
						item['educational'].append('Science')
					elif mappedgroup == group_astronomy:
						item['educational'].append('Science')
					elif mappedgroup == group_bowling:
						item['sport'].append('Bowling')
					elif mappedgroup == group_boxing:
						item['sport'].append('Boxing')
					elif mappedgroup == group_cluedo:
						item['narrative'].append('Detective / Mystery')
						item['gameplay'].append('Board Game')
						newgroupslist.append( "Genre: Board game - Clue" )
						newgroupslist.append( "Board game translations" )
					elif mappedgroup == group_coinop:
						item['gameplay'].append('Arcade')
					elif mappedgroup == group_chess:
						item['gameplay'].append('Chess')						
					elif mappedgroup == group_flipper:
						item['gameplay'].append('Pinball')
					elif mappedgroup == group_football:
						item['sport'].append('Football (European) / Soccer')
					elif mappedgroup == group_snooker:
						item['sport'].append('Pool / Snooker')
					elif mappedgroup == group_isometric:
						item['visual'].append('Isometric')						
					elif mappedgroup == group_mastermind:
						item['gameplay'].append('Puzzle-solving')												
						newgroupslist.append( 'Mastermind variants' )
					elif mappedgroup == group_othello:
						item['gameplay'].append('Board Game')
						item['pacing'].append('Turn-based')
						newgroupslist.append( "Board game translations" )
						newgroupslist.append( "Genre: Board game - Reversi / Othello" )
					elif mappedgroup == group_qbert:
						item['gameplay'].append('Puzzle-solving')
						newgroupslist.append( "Q*Bert variants" )
					else:
						newgroupslist.append( mappedgroup )
					
					
			item['group'] = ";".join( newgroupslist )
	    ########################
	    ########################
	    			
		#########################
		###### MAP GENRES  ######
		# check if game is breakout
		# if yes then 
		# 1. add to groups:Breakout variants
		# 2. add custom field gameplay:Paddle / Pong
		# 3. add custom field gameplay:Arcade
		if item['genre'] == game_breakout:
			item['group'] += ';Breakout variants'
			item['gameplay'].append('Paddle / Pong')
			item['gameplay'].append('Arcade')
			
		# if game is of type fight
		# add custom field gameplay:Fighting
		if item['genre'] == game_fight:
			item['gameplay'].append('Fighting')
			
		# if type of game is management, add custom field
		# gameplay:Managerial / Business Simulation
		if item['genre'] == game_management:
			item['gameplay'].append('Managerial / Business Simulation')
			
		# if game is of type arcade, add custom field
		# gameplay:Arcade
		if item['genre'] == game_arcade:
			item['gameplay'].append('Arcade')
			
		# if type is platform, add custom field
		# gameplay:Platform
		if item['genre'] == game_platform:
			item['gameplay'].append('Platform')
		
		# if type is of quiz, add custom field
		# gameplay:Game Show / Trivia / Quiz
		if item['genre'] == game_quiz:
			item['gameplay'].append('Game Show / Trivia / Quiz')
			
		# if has type shmup add custom field
		# gameplay:Shooter
		if item['genre'] == game_shmup:
			item['gameplay'].append('Shooter')

		# if has type of target shooting add custom field
		# gameplay:Shooter			
		if item['genre'] == game_targetshooting:
			item['gameplay'].append('Shooter')
		
		# if game is of educational type history / geography
		# add custom fields
		# 1. Educational:Geography
		# 3. Educational:History
		if item['genre'] == game_edu_history_geography:
			item['educational'].append('Geography')
			item['educational'].append('History')
			
		# if type is of Educational Math, add custom field
		# Educational:Math / Logic
		if item['genre'] == game_edu_math:
			item['educational'].append('Math / Logic')

		# if has type Educational grammar / spelling
		# add custom field educational:Reading / Writing
		if item['genre'] == game_edu_grammar:
			item['educational'].append('Reading / Writing')
						
		#	
		# map genre to mobygames genres
		# remove it if there is no corresponding genre
		#
		if item['genre']:
			item['genre'] = self.map_genre( item['genre'] )
	    ########################
	    ########################
						
						
										
		#########################
		###### MAP PLAYERS ######		
		if 'players' in item.keys() and item['players']:
			playerslist = item['players'].split(";")
			newplayerslist = []
			for p in playerslist:
				mappedplayer = self.map_player( p );				
				if mappedplayer:
					newplayerslist.append( mappedplayer )
			setplayerslist = set( newplayerslist )
			item['players'] = ";".join( setplayerslist )			
	    ########################
	    ########################
	    			    		   		    	    
		# convert year to date 1/1/year
		if 'year' in item.keys() and item['year']:			
			item['date'] = str(dateutil.parser.parse('1/1/' + item['year'][0]))			
			item.pop("year", None)
		if 'year' in item.keys():
			item.pop("year", None)

		# scale score to 1 to 5
		if 'criticScore' in item.keys() and item['criticScore']:
			if " / " in item['criticScore'][0]:
				scores = item['criticScore'][0].split(' / ')
				item['criticScore'][0] = str( int( float(5) * float(scores[0]) / float(scores[1]) ) )				
			else:
				item.pop("criticScore", None)					    
	    	   
#		if 'misc' in item.keys():
#			if [i for i in licensed  if i in item['misc']]:
#				item['licensed'] = ''					           
	
		# delete empty keys
		self.delKey( item, 'genre')
		self.delKey( item, 'gameplay')
		self.delKey( item, 'group')
		self.delKey( item, 'educational')		
		self.delKey(item, 'addon')
		self.delKey(item, 'sport')
		self.delKey(item, 'narrative')
		self.delKey(item, 'visual')
		self.delKey(item, 'pacing')
				
		self.exporter.export_item(item)
		return item

	# map genre to mobygames compatible genres
	def map_genre(self,x):			
		if x in genres_map:			
			return genres_map[x]
		else:
			return None

	# map players to mobygames compatible players
	def map_player(self,x):
		for playerkey in players_map.keys():			
			if playerkey.lower() in x.lower() or x.lower() in playerkey.lower():				
				return players_map[playerkey]
		return None

	# map groups to readable / presentable Amstrad custom groups
	# or map them to related mobygames game groups 
	def map_group(self,x):
		for groupkey in groups_map.keys():			
			if groupkey.lower() in x.lower() or x.lower() in groupkey.lower():				
				return groups_map[groupkey]
		return None
					
	def initKey(self,item,key):
		if key not in item.keys():
			item[key] = []		
							
	def delKey(self,item,key):
		if not item[key]:
				del item[key]
