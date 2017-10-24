from mobygames.spiders.mobygames_spider import MobygamesSpider
from mobygames.items import MobygamesItem
from mobygames.exporter import Exporter 
from mobygames.exporterfromlist import ExporterFromList 


# Genesis
#s = Exporter('/home/charalampos/sega-megadrive-parent-clone.xml')
#s = Exporter('/home/charalampos/sega-megadrive-parent-clone-sample.xml')

# SNES
#s = Exporter('/home/charalampos/snes-parent-clone.xml')

# Amstrad CPC
#s = Exporter('/home/charalampos/amstrad-cpc-tosec.dat')

# Arcade
#s = Exporter('/home/charalampos/mame-v0.174-xml.dat')

# Amiga
#s = Exporter('/home/charalampos/amiga-games-ADF-TOSEC-v2014-08-01_CM.dat')

# Gameboy Advance
#s = Exporter('/home/charalampos/gba-parent-clone.dat')

# Export from txt list file,
# each line is a title name
# s = ExporterFromList('/home/charalampos/gba-parent-clone.dat','Genesis','JPN')
s = ExporterFromList('/home/charalampos/dev/src/scry/mobygames/files/sega-mega-drive-missing/sega-mega-drive-missing.txt','Genesis')

