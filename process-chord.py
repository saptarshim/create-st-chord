
def create_chord_list(chord_line):
    valid_chord_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', '#','b', 'm', '7']
    valid_chord_modifier = ['#','b', 'm', '7']

    chord_list = [[]]
    chord_list_count = 0

    for index, char in enumerate(chord_line):
        #print("Index=", index)
        if char in valid_chord_char:

            #If this is a chord modifier treat differntly
            if char in valid_chord_modifier:
                #chord modifier can only happen after a valid Capital chord character 
                info = chord_list [chord_list_count]
                str = info[1]
                str = str + char
                new_info = [info[0], str]
                chord_list [chord_list_count] = new_info    
            else:
                chord_info = [index, char]
                chord_list.append(chord_info)
                chord_list_count += 1
    
    chord_list = chord_list[1:]
    return chord_list


def create_ST_lyrics_line_from_list(chord_list, lyrics_line):
    combined_chord_lyrics = ''
    lyrics_start_index = 0

    length = len(chord_list) - 1
    for i in range(length):
        thisChord = chord_list[i]
        nextChord = chord_list[i+1]
        chord_val = thisChord[1]
        lyrics_start_index = thisChord[0]
        lyrics_end_index = nextChord[0]
        line_to_add = lyrics_line[lyrics_start_index:lyrics_end_index]
        combined_chord_lyrics = combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
        #After the last chord add the reaming lyrins at the end of the line 
        if i == (length - 1):
            #This is the last iteration
            lyrics_len = len(lyrics_line)
            if lyrics_len > lyrics_end_index:
                combined_chord_lyrics = combined_chord_lyrics + lyrics_line[lyrics_end_index: lyrics_len]
    
    combined_chord_lyrics.strip()

    return combined_chord_lyrics


def create_chord_lyrics_list(lines):
    chord_and_lyric_list = [[]]

    length = len(lines)

    for i in range (0, length-1, 2):

        chord_line = lines[i].strip()
        # TODO: Instrument some sort of checking to mak sure it's the
        #lyrics line
        
        lyric_line = lines[i+1].strip()
        info = [chord_line, lyric_line]
        chord_and_lyric_list.append(info)
        
    chord_and_lyric_list = chord_and_lyric_list[1:]
    return chord_and_lyric_list


def get_st_chord(chord_and_lyric_list):
    st_lyric_list = []
 
    for info in chord_and_lyric_list:
        chord_line = info[0]
        lyric_line = info[1]
        mylist = create_chord_list(chord_line)
        st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)
        st_lyric_list.append(st_chord)

    return st_lyric_list

input_file = 'input.txt'
output_file = 'output.txt'
try:
    # Read text from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
        #print(type(lines))
        
except FileNotFoundError:
    print("Error: Input file not found.")
except Exception as e:
    print("An error occurred:", str(e))

#first_line = lines[0]
#second_line = lines[1]
#print(first_line)
#print(second_line)
#mylist = create_chord_list(first_line)
#print(mylist)
#st_chord = create_ST_lyrics_line_from_list(mylist,second_line)
#print(st_chord)
chord_and_lyric_list = create_chord_lyrics_list(lines)
#print(chord_and_lyric_list)
st_chord = get_st_chord(chord_and_lyric_list)
#print(st_chord)

try:
    output = open(output_file, 'w')

    for line in st_chord:
        nline = line
        output.write(line)
        print(line)
        output.write("\n")

except FileNotFoundError:
    print("Error: Output file not found.")
except Exception as e:
    print("While writing An error occurred:", str(e))
