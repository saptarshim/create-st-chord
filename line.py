# MIT License

# Copyright (c) 2024 Saptarshi Mondal (saptarshi.mondal@gmail.com)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from global_def import VALID_CHORD_CHAR, VALID_CHORD_MODIFIER, LINE_STATE

from tools import get_lines, write_lines, check_if_this_chord_line, chord_or_lyric_first
from tools import create_chord_list, create_ST_lyrics_line_from_list
from tools import get_next_line_index, preproces_each_line, postproces_each_line


class Line:
    def __init__(self, lineno, linestring):
        print("Constructor for Line Called")
        self._lineno = lineno
        self._linestring = linestring
        

    
    @property
    def linestring(self):
        return self._linestring
    
    @property
    def lineno(self):
        return self._lineno
    

    @linestring.setter
    def linestring(self, value):
        self._linestring = value


    @lineno.setter
    def lineno(self, value):
        self._lineno = value


class Chord(Line):
    def __init__(self, lineno, linestring):
        print("Constructor for Chord Called")
        super().__init__(lineno, linestring)  # Call the parent class constructor
        self._chord_list = [[]]
        self.proccess()
        
    
    @property
    def chord_list(self):
        return self._chord_list
    
    @chord_list.setter
    def chord_list(self, value):
        self._chord_list = value    

        
    def proccess(self):
        print("This is a method from process")
        chord_list_count = 0
        #chord_line = super().linestring
        chord_line = self.linestring
        for index, char in enumerate(chord_line):
            
            if (char in VALID_CHORD_CHAR) or (char in VALID_CHORD_MODIFIER):

                #If this is a chord modifier treat differntly
                if char in VALID_CHORD_MODIFIER:
                    #chord modifier can only happen after a valid Capital chord character 
                    info = self.chord_list [chord_list_count]
                    str = info[1]
                    str = str + char
                    new_info = [info[0], str]
                    self.chord_list[chord_list_count] = new_info    
                else:
                    chord_info = [index, char]
                    self.chord_list.append(chord_info)
                    chord_list_count += 1
        
        self.chord_list = self.chord_list[1:]

    def get_chord_list(self):
        return self.chord_list


class Lyric(Line):
    def __init__(self, lineno, linestring):
        super().__init__(lineno, linestring)  # Call the parent class constructor
        print("Constructor for Lyric Called")

    def proccess(self):
        print("This is a method from Lyric")


class Comment(Line):
    def __init__(self, lineno, linestring):
        super().__init__(lineno, linestring)  # Call the parent class constructor
        

    def proccess(self):
        print("This is a method from Comment")
    
class Blank(Line):
    def __init__(self, lineno, linestring):
        super().__init__(lineno, linestring)  # Call the parent class constructor

    def proccess(self):
        print("This is a method from Blank")


class ST_CHORD (Line):
    def __init__(self, chord, lyric):
            
        print("Constructor for ST_CHORD Called")
        self._chord = chord   #Instance of a Chord class
        self._lyric = lyric   #Instance of a Lyric class
        self.combined_chord_lyrics = ''
        self.process()


    @property
    def chord(self):
        return self._chord
    
    @chord.setter
    def linestring(self, value):
        self._chord = value


    @property
    def lyric(self):
        return self._lyric
    
    @lyric.setter
    def lyric(self, value):
        self._lyric = value



    def process(self):

        chord = self.chord
        lyrics = self.lyric
        chord_list = chord.chord_list 

        thisChord = chord_list[0]

        lyrics_start_index = 0
        lyrics_end_index = thisChord[0]
        lyrics_line = lyrics.linestring

        if thisChord[0] > 0:
            #this chord didn't start at the beging of the line
            self.combined_chord_lyrics = lyrics_line[0: lyrics_end_index]
        
        length = len(chord_list)
        
        if length == 1:
            chord_val = thisChord[1]
            line_to_add = lyrics_line[lyrics_end_index:]
            self.combined_chord_lyrics =  self.combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
            #print(combined_chord_lyrics)
        else:
            for i in range(length):  #(length - 1)
                thisChord = chord_list[i]
                #After the last chord add the reaming lyrins at the end of the line 
                if i == (length - 1):
                    #This is the last iteration
                    lyrics_len = len(lyrics_line)
                    if lyrics_len > lyrics_end_index:
                        chord_val = thisChord[1]
                        line_to_add = lyrics_line[lyrics_end_index: lyrics_len]
                        self.combined_chord_lyrics = self.combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
                else:
                    nextChord = chord_list[i+1] # Do you need to check if this is out of bound 
                    chord_val = thisChord[1]
                    lyrics_start_index = thisChord[0]
                    lyrics_end_index = nextChord[0]
                    line_to_add = lyrics_line[lyrics_start_index:lyrics_end_index]
                    self.combined_chord_lyrics = self.combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
                    
        self.combined_chord_lyrics.strip()

    @property
    def linestring(self):
        return self.combined_chord_lyrics

class STChordApp:
    def __init__(self, input_file, output_file):
            
        print("Constructor for STChordApp Called")
        self._inputfile = input_file   #Instance of a Chord class
        self._outputfile = output_file   #Instance of a Lyric class
        self._line_obj_list = []
        self._st_chord_list = []
        self._lines = []
        self._chord_first = True
        self._output_lines = []
        self.get_lines()
        self.chord_or_lyric_first()
        self.validate()
        self.process()

    @property
    def st_chord_list(self):
        return self._st_chord_list
    
    @st_chord_list.setter
    def linestring(self, value):
        self._st_chord_list = value

    @property
    def lines(self):
        return self._lines
    
    @st_chord_list.setter
    def lines(self, value):
        self._lines = value

    def get_lines(self):
        input_file = self._inputfile
        lines = None
        try:
            # Read text from the input file
            with open(input_file, 'r') as file:
                lines = file.readlines()
                
        except FileNotFoundError:
            print("Error: Input file not found.")
        except Exception as e:
            print("An error occurred:", str(e))

        processedlines = [[]]

        length = len(lines)

        for i in range (0, length, 1):
            #line = lines[i].strip(); If you do this the leading blank will be deleted from chord line
            line = lines[i]
            if line != '\n': #If this is not a blank line then remove the \n
                line = line.rstrip("\n") # Remove any new line character at the end of the line
            if len(line.strip()) == 0 or line == '\n':
                #Check if this is a blank line
                line_info = [i,LINE_STATE['BLANK'],'\n']
            elif line[0] == '#':
                #Check if this is a comment line
                line_info = [i,LINE_STATE['COMMENT'],line]
            elif check_if_this_chord_line(line):
                #Check if this is a chord line
                line_info = [i,LINE_STATE['CHORD'],line]
            else:
                #This must be a lyrics line
                line_info = [i,LINE_STATE['LYRIC'],line]
                
            processedlines.append(line_info)

        # Remove the first empty list item, This is doesn't hapen if it's a simple list
        self._lines = processedlines[1:]


    def chord_or_lyric_first(self):
        chord_detected = False
        lyrics_detected = False
        
        # Find out the structure of the input, Does it start with Chord or Lyrics 
        lines = self._lines
        for info in lines:
            if info[1] == LINE_STATE['BLANK'] or info[1] == LINE_STATE['COMMENT']:
                #this is a blank or comment line so simply add it to the output
                continue
            elif info[1] == LINE_STATE['CHORD']:
                if lyrics_detected == False:
                    self._chord_first = True
                else:
                    self._chord_first = False
                break         
            elif info[1] == LINE_STATE['LYRIC']:
                if chord_detected == False:
                    self._chord_first = False
                else:
                    self._chord_first = True
            break

    def validate(self):
        if self._lines == None:
            print("Input Error")
        return False

    def create_line_obj(self):
        for line_info in self._lines:
            line_type = line_info[1]
            line_string = line_info[2]
            line_no = line_info[0]

            if line_type == LINE_STATE['CHORD']:
                obj = Chord(line_no, line_string)
            elif line_type == LINE_STATE['LYRIC']:
                obj = Lyric(line_no, line_string)    
            elif line_type == LINE_STATE['COMMENT']:
                obj = Comment(line_no, line_string)
            else: 
                #line_type == LINE_STATE['BLANK']:
                obj = Blank(line_no, line_string)
            
            self._line_obj_list.append(obj)
    
    def create_st_obj(self):
        for index, obj in enumerate(self._line_obj_list):
            if isinstance(obj, Comment) or isinstance(obj, Blank):
                    self._st_chord_list .append(obj)
                    continue

            if self._chord_first:
                if isinstance(obj, Chord):
                    chord = obj
                    lyric = self._line_obj_list[index+1] # TODO: handle this case in vlidate for out of bound
                    st_chord = ST_CHORD(chord, lyric)
                    self._st_chord_list.append(st_chord)
            else:
                if isinstance(obj, Lyric):
                    lyric = obj
                    chord = self._line_obj_list[index+1] # TODO: handle this case in vlidate for out of bound
                    st_chord = ST_CHORD(chord, lyric)
                    self._st_chord_list.append(st_chord)

    def get_line_from_st_obj(self):

        for st in self._st_chord_list:
            line = st.get_line()
            self._output_lines.append(line)

    
    def write_lines(self):
        output_file = self._output_file_txt
        lines = self.get_line_from_st_obj()
        try:
            output = open(output_file, 'w')

            for line in lines:
                output.write(line)

        except FileNotFoundError:
            print("Error: Output file not found.")
        except Exception as e:
            print("While writing An error occurred:", str(e))
        
    def process(self):
        self.create_line_obj()
        self.create_st_obj()
        self.write_lines()
        
        

#Test Code
def main(input_file, output_file):
    st = STChordApp(input_file, output_file)

input_file = 'input.txt'
output_file = 'output.txt'

main(input_file, output_file)


