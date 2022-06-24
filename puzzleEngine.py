# Woordzoeker Solver by Tjalling
from timeit import default_timer as timer
import os

words = []
words_found = []
words_not_found = []


def create_words_list():
    global words
    work_dir = os.getcwd()
    file_name = "woordenJulia2.txt"
    file = open((work_dir + "/Puzzels/" + file_name), "rt")
    for woord in file.readlines():
        words.append(woord.rstrip().upper())
    file.close()
    words.sort(key=len,reverse=True)


def create_letters_grid():

    # Bestandsnaam met de letters
    work_dir = os.getcwd()
    print(work_dir)
    file_name = "lettersJulia2.txt" 
    f = open((work_dir + "//Puzzels//" + file_name), "rt")
    
    # Bepaal breedte(col) en lengte(row)
    col = len(f.readline().rstrip())
    f.seek(0)
    row = len(f.readlines())

    # maak 3dgrid laag1 = X, laag2 = Y, laag 3 = 'letter' , isGebruikt , mogelijkheidswaarde.
    # Voorbeeld : [2][1]["r", False,10] = pos (2,1) met letter 'r' is nog niet gebruikt, mogelijksheidswaarde = 10
    global grid
    grid = [[["",False,0] for c in range(col)] for r in range(row)]

    # Vul grid met alle letters:
    f.seek(0)
    i =0
    for rows in f.readlines():
        j=0
        for ch in rows.rstrip():
            grid[i][j][0] = ch.upper()
            j += 1
        i += 1
    f.close()

def set_MogWaa():
    # Cellen krijgen een waarde op basis van mogelijkheid(MogWaa). Hoe hoger, hoe minder kans dat deze gebruikt wordt
    # Hoekcellen hebben maar 3 mogelijke richtingen en krijgt MogWaa 50
    mogWaa_Corners = 50
    grid[0][0][2] = mogWaa_Corners
    grid[0][len(grid[0])-1][2] = mogWaa_Corners
    grid[len(grid)-1][0][2] = mogWaa_Corners
    grid[len(grid)-1][len(grid[0])-1][2] = mogWaa_Corners

    # Buitenste cellen 5 mogelijke richtingen en krijgen MogWaa 30
    # Boven en onderste rij:
    mogWaa_sides = 30
    for i in range(1,len(grid[0])-1):
        grid[0][i][2] = mogWaa_sides
        grid[len(grid)-1][i][2] = mogWaa_sides
    # Linker er rechterrij:
    for i in range(1,len(grid)-1):
        grid[i][0][2] = mogWaa_sides
        grid[i][len(grid[i])-1][2] = mogWaa_sides


def create_sorted_value_list():
    # Maak van bestaande grid 1 grote lijst met alle letters;
    # zodat hierop gezocht kan worden; en kan worden gesorteerd
    global sorted_value_list
    sorted_value_list = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # maak value_list met daarin : Letter, Value, Row, Col (gesorteerd op value)
            list_item = grid[row][col][0],grid[row][col][2],row,col
            sorted_value_list.append(list_item)
    sorted_value_list.sort(key = lambda row: row[1])


def print_grid():
    for row in range(len(grid)):
        print(grid[row])


def get_first_letter_coor_list(woordnr):
    # Maak een lijst met alle overeenkomsten met 1e letter
    matching_letter_list = []
    for letter in sorted_value_list:
        if woordnr[0] == letter[0]:
            matching_letter_list.append((letter[2],letter[3]))
    return(matching_letter_list)


class Direction:
    def __init__(self,name, row_step,col_step):
        self.row_step = row_step
        self.col_step = col_step
        self.name = name

    def chk_in_dir(self,letter,start_position,step=1):
    # controleer of letter overeenkomst met positie met 'step' vanaf startpositie
        row,col = self.get_letter_coor(start_position,step)
        # controleer op letter in grid op positie overeenkomst met de letter

        if grid[row][col][0] == letter: # is er een overeenkomst?
            return True
        else:
            return False

    def get_dir_name(self):
        return self.name

    def get_letter_coor(self, start_position, step):
        row,col = start_position
        letter_coor = (row + step * self.row_step , col + step * self.col_step)
        return letter_coor

    def __str__(self):
        return(self.name)


dir_N = Direction("N",-1,0)
dir_NE = Direction("NE",-1,+1)
dir_E = Direction("E",0,+1)
dir_SE = Direction("SE",+1,+1)
dir_S = Direction("S",+1,0)
dir_SW = Direction("SW",+1,-1)
dir_W = Direction("W",0,-1)
dir_NW = Direction("NW",-1,-1)


def find_direction(word,coordinaat):
    # Geeft een lijst met alle mogelijke richtingen vanuit opgegeven
    # positie waarop de 2e letter vh woord een match vormt met het grid.

    directions_list = []
    match = True

    # is om eerste letter heen de tweede letter?
    directions_objects = [dir_N, dir_NE, dir_E, dir_SE, dir_S, dir_SW, dir_W, dir_NW]
    for direction_object in directions_objects:
        try:
            # Ga elke richting af vanuit met :de 2e letter van het woord, coordinaten van 1e letter
            row,col = coordinaat
            match = direction_object.chk_in_dir(word[1], coordinaat)  # 2e letter eromheen?
            if match: # als eromheen, dan in de lijst
                directions_list.append(direction_object)
            else:
                continue
        except IndexError as err:
            # print(err, direction_object.__name__)
            continue
    return directions_list


def are_other_letters_matched(word,direction,first_letter_coor):
    # zoek in de richting naar de 2e en volgende letters zolang dit goed gaat
    # eerste letter is bekend
    letter_postion = 2 # we beginnen met 3e letter(1 en 2 zijn al bekend)

    if letter_postion > len(word)-1: #woord heeft maar 2 letters
        match=False
        word_found = True
    else:
        word_found = False
        match = True

    while match:
        try:
            match = direction.chk_in_dir(word[letter_postion],first_letter_coor,letter_postion)
            if match and letter_postion == len(word)-1:
                match = False
                word_found = True
                break
            else:
                letter_postion += 1
        except IndexError as e:
            # print("index2error", e)
            match = False
    return word_found


def is_one_unused(word,first_coor, direction):
    # is minstens 1 letter ongebruikt, dan is het woord goedgekeurd, anders niet. (zeilboot/boot verhaal)
    # functie loopt elke letter in grid langs. Telt het aantal 'gebruikte' letters. Dit moet minder dan woordlengte zijn
    used_letters =  0
    for position in range(len(word)):
        coor = direction.get_letter_coor(first_coor,position)
        row,col = coor
        if grid[row][col][1]: # True betekend dat de letter eerder gebruikt is.
            used_letters += 1
    if used_letters < len(word): # er is minsten 1 letter niet gebruikt
        return True
    else:
        return False

def set_status(positie,gebruikt,waarde):
    # zet de status van letter in gebruikt/ongebruikt, en verhoogt de gebruikerswaarde
    grid[positie[0]][positie[1]][1] = gebruikt
    grid[positie[0]][positie[1]][2] += waarde


def solve_puzzle():

    for word in words:
        if find_word(word): # Woord is gevonden
            continue
        else:
            #Woord is niet gevonden
            global words_not_found
            words_not_found = [word]
            pass

def find_word(word):
    # krijg een lijst met alle coordinaten(row/col) met 1e letter vh woord. :
    word_found = False
    first_letter_coor_list = get_first_letter_coor_list(word)

    for first_letter_coor in first_letter_coor_list:
        # krijg een lijst met richtingen waar 2e letter overeenkomt:
        # verstuur hiervoor : woord, en x/y van eerste letter.
        directions_list = find_direction(word,first_letter_coor)
        for direction in directions_list:
            # Voor elk mogelijke richting; controleer of 2e en volgende letter overeenkomt.
            # als alle letters 'op' zijn is het woord dus gevonden. en gaan we terug.
            # verstuur hiervoor : woord, richting en positie van eerste letter.
            # 2e letter is al een match; dat blijkt uit de richtingbepaling
            if word_found:
                break
            if are_other_letters_matched(word,direction,first_letter_coor):
                # check of minstens 1 vd letters 'nietgebruikt' is.
                if is_one_unused(word, first_letter_coor, direction):
                    #alle gebruikte letters krijgen gebruikerswaarde + 10, en worden op 'gebruikt' gezet.
                    for letter in range(len(word)):
                        # pak van alle letters de coordinaten en geeft ze True(isgebruikt) en Magwaa 12.5 mee
                        set_status(direction.get_letter_coor(first_letter_coor, letter), True, 12.5)
                    # woord is gevonden; opslaan van woord met beginletter en richting
                    word_found = True
                    words_found.append([word, first_letter_coor, direction.get_dir_name()])
                    return word_found
                # print("259")
                pass
            else:
                # deze richting klopte dus niet.
                # print("263")
                word_found = False
                pass

    return False


def get_untouched_letters():
    solution = ""
    for row in range(len(grid)):  # alle rijen door
        for col in range(len(grid[row])):  # alle kolommen door
            if grid[row][col][1] == False: # Letter is dus niet gebruikt
                solution += grid[row][col][0] # is de corresponderende letter
    return solution

def resume(solution, words_not_found,timeStart,timeEnd):
    print()
    print()
    print(bcolors.HEADER,end ="")
    print("***********************************")
    print("**    !!! Puzzle Solved !!!      **")
    print("**                               **")
    print("**".ljust(10) + solution+"**".rjust(20))
    # print(bcolors.OKGREEN, end="")
    print("**                               **")
    print("**                               **")
    print("** Words not found :", words_not_found," **")
    print("** Time taken : ", timeEnd - timeStart ," **")
    print("***********************************")
    print(bcolors.ENDC)


def write_solution_to_file():
    words_found.sort(key=str)
    work_dir = os.getcwd()
    file_name = "woordenJulia2.solution.txt" 
    
    
    
    try:
        file = open((work_dir + "//Puzzels//" + file_name), "wt")
        for word in words_found:
            file.write(str(word)+"\n")
    finally:
        file.close()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    timeStart = timer()                     # start de timer
    create_letters_grid()                   # pak letters en zet ze in xy grid
    create_words_list()                     # pak woorden, sorteer op langste eerst in lijst
    set_MogWaa()                            # geef MogWaa aan de cellen
    create_sorted_value_list()              # mak 1d lijst van het grid, gesorteerd op MogWaa
    solve_puzzle()                          # zoek alle woorden in het grid
    timeEnd = timer()                       # stop de timer
    write_solution_to_file()                # schrijf de gevonden woorden met richting naar txt bestand
    resume(get_untouched_letters(),words_not_found, timeStart,timeEnd)  # basic uitvoer naar de console