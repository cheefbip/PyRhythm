
metadata_map = {
    "Title"             : 0,
    "Artist"            : 1,
    "Creator"           : 2,
    "Mode"              : 3,
    "AudioFile"         : 4,
    "CoverFile"         : 5,
    "SongPreviewTime"   : 6,
    "DifficultyName"    : 7,
    "Description"       : 8
}

pyr_sections = {
    "[Metadata]\n"  : 0,
    "[Events]\n"    : 1,
    "[Timing]\n"    : 2,
    "[Velocity]\n"  : 3,
    "[Objects]\n"   : 4
}

class Difficulty():
    def __init__(self, folder, pyrfile):
        self.folder = folder
        self.pyrfile = pyrfile

        self.title = None
        self.artist = None
        self.creator = None
        self.mode = None
        self.audiofile = None
        self.coverfile = None
        self.diffname = None

        self.parsemetadata()

    def parsemetadata(self):
        section = None
        i = 0
        with open(self.folder + "\\" + self.pyrfile) as file:
            for line in file:
                    i += 1
                    if (i > 10) : break
                    if line == "\n" : continue

                    if section == None:
                        section = pyr_sections.get(line)
                        continue
                    
                    if section == 0: # If section == metadata
                        items = line.split(":")
                        md_type = metadata_map.get(items[0])
                        if md_type == 0: # Parsing title
                            self.title = items[1].strip()
                        elif md_type == 1: # Parsing artist
                            self.artist = items[1].strip()
                        elif md_type == 2: # Parsing map creator name
                            self.creator = items[1].strip()
                        elif md_type == 3: # Parsing gamemode
                            self.mode = items[1].strip()
                        elif md_type == 4: # Parsing song file name
                            self.audiofile = items[1].strip()
                        elif md_type == 5: # Parsing song file name
                            self.coverfile = items[1].strip()
                        elif md_type == 7: # Parsing song file name
                            self.diffname = items[1].strip()