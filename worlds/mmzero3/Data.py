# Field offsets for gAp and gApSeedConfig.
# Names are the ap.h field names. 
# Values are for BizHawk "Combined WRAM" 
# EWRAM address minus 0x02000000

# gAp.ready reads AP_READY once the game has booted, and gAp.version reads AP_VERSION.
AP_READY = 0x335A5041      # Spells out 'APZ3' in little endian
AP_VERSION = 15

# gAp
GAP = 0x0003EE80                
READY = 0x0003EE80              
VERSION = 0x0003EE84            
ITEM_INBOX = 0x0003EE86         
ITEM_INBOX_COUNT = 16
ITEM_INBOX_ELEMENT_SIZE = 2
ITEMS_APPLIED = 0x0003EEA6      
INBOX_WRITE_INDEX = 0x0003EEA8  
INBOX_READ_INDEX = 0x0003EEA9   
CHECKED_LOCATIONS = 0x0003EEAA  
CHECKED_LOCATIONS_COUNT = 29
CHECKED_LOCATIONS_ELEMENT_SIZE = 1
RANK_ELF_USED = 0x0003EEC7      
DISKS_OWNED = 0x0003EEC8        
DEATH_COUNT = 0x0003EECA        
KILL_REQUEST = 0x0003EECC       
CAN_ACCEPT_ITEMS = 0x0003EECD   

# gApSeedConfig, ROM data
SEED_CONFIG_ROM_OFFSET = 0x008009D8
SEED_CONFIG_SIZE = 4
SEED_CONFIG_FIELDS = {   # ap.h name: (offset, size)
    "requiredDisks": (0, 2),
    "startingWeapons": (2, 1),
    "easyExSkill": (3, 1),
}
