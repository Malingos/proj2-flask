"""
Pre-process a syllabus (class schedule) file. 

"""
#import flask
import arrow   # Dates and times
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

base = arrow.now()   # Default, replaced if file has 'begin: ...'
weekNum = 1
def cWeekNum():
    return weekNum

"""def getWeekNum(raw):
    global weekNum
    global base
    field = None
    #content = ""
    entry = {}
    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
#            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2:
            field = parts[0]    
            content = parts[1]
        else:
            raise ValueError ("Big problem getting start date")
        if field == "begin":
           try:
               basee = arrow.get(content)#, "MM/DD/YYYY")
               #basee.format("MM/DD/YYYY")
               #base = arrow.get(base, "MM/DD/YYYY")
               today = arrow.now()
               #today.format("MM/DD/YYYY")
               if basee == today:
                   weekNum = 1
               else:    
                   for index in range(1,70):
                       basee = basee.shift(days=+1)#.format("MM/DD/YYYY")
                       if today.format("MM/DD/YYYY") == basee.format("MM/DD/YYYY"):
                           weekNum = (index % 7) + 1
                           #break
                           return weekNum
           except:
               raise ValueError("Bad Date Format Getting Start")
        else:
            continue
    return weekNum
    #owfiaretval = weekNum
    #return retval"""
def process(raw):
    #global weekNum
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    entry = {}
    cooked = []
    number = -1

    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        if len(line) == 0 or line[0] == "#":#if # is the first character, skip
            log.debug("Skipping")
            continue
        parts = line.split(':')#split lines to before and after ":"
        if len(parts) == 1 and field:#adds additional content to whatever the previously used field is
            entry[field] = entry[field] + line + " " 
            continue
        if len(parts) == 2:#if there are 2 parts, the field is the first part and the content is the second part
            field = parts[0]
            content = parts[1]
        else:#if none of the above are correct there is an issue
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                             "Split into |{}|".format("|".join(parts)))

        if field == "begin":#checking if this is the line with the start date
            try:#begin only triggers once (at least it should only trigger once)
                base = arrow.get(content, "MM/DD/YYYY")#get the date as an object named "base", will need to use this to determine start date and current week, arrow must have a "current date"?
                # base is the "week 1" date, DD = 1, DD + 7 = 2, DD + 14 = 3, DD + 21 = 4, etc
                #now i will make variables for the start date of each week, or find a way to take the difference between 2 dates
                #end = base#arrow.get(base, "MM/DD/YYYY")
                #end = end.shift(weeks=+10)
                #today = arrow.now()
                #today.format("MM/DD/YYYY")
                #if today == base:
                #    weekNum = 1
                #number = -1
                """weeks = [base, base.shift(days=+7), base.shift(days=+14), base.shift(days=+21), base.shift(days=+28), base.shift(days=+35), base.shift(days=+42), base.shift(days=+49), base.shift(days=+56), base.shift(days=+63), base.shift(days=+70)]
                today = arrow.now()
                for i in range(0,9):
                    if weeks[i] <= today <= weeks[i+1]:
                        number = i+1
                if today > weeks[10]:
                    number = 10
                elif today < weeks[0]:
                    number = 0
                #base = arrow.format("MM/DD/YYYY")
                else:
                    raise ValueError("Big error calculating week")
                #for index in range(1,70):
                #    base = base.shift(days=+1)
                #    if today == base:
                #        weekNum = weekNum + (index % 7)
                #        break        
                base = base.format("MM/DD/YYYY")"""
            except:
                raise ValueError("Unable to parse date {}".format(content))#date is incorrectly formatted, should be MM/DD/YYYY
            #now I need to check if either of these weeks is the current week
#            for r in arrow.Arrow.span_range('day',
        elif field == "week":#this is the week number
            if entry:
                cooked.append(entry)
                entry = {}#make entry empty again
            #if content == currentWeekNum:
                #print("Content: " + content)
                #print("Week Number: " + currentWeekNum + "\n")
                #print("Is Current Week?" + currentWeekBool + "\n")
            #    currentWeekBool = True
            entry['topic'] = ""#these are all "classes" in the HTML document
            entry['project'] = ""
            entry['week'] = content#put the week number into the "week" field in the html document
            #entry['isCurrentWeek'] = currentWeekBool
            #currentWeekBool = False
            #if content == weekNum:
            #    entry['bool'] = True
            #else:
            #    entry['bool'] = True
            """if 
            if content == currentWeekNum:
                entry['isCurrentWeek'] = True
            else:
                entry['isCurrentWeek'] = False"""

        elif field == 'topic' or field == 'project':#from if len == 2, set the entry for the field to the content in the html doc
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))
        #entryn = entry + "\n"
	#cookedn = cooked + "\n"
	#fieldn = field + "\n"
	#print("Entry: " + entryn)
        #print("Cooked: " + cookedn)
        #print("Field: " + fiieldn)
    if entry:#appends whatever added stuff to the whole docuemnt
        cooked.append(entry)
	#returns formatted document after it has been looped throughi
    #number = getWeekNum(raw)
    weeks = [base, base.shift(days=+7), base.shift(days=+14), base.shift(days=+21), base.shift(days=+28), base.shift(days=+35), base.shift(days=+42), base.shift(days=+49), base.shift(days=+56), base.shift(days=+63), base.shift(days=+70)]
    today = arrow.now()
    for i in range(0,9):
        if weeks[i] <= today <= weeks[i+1]:
            number = i+1
            return [cooked, i+1]
    if today < weeks[0]:
        number = 0
    else:
        number = 10
    return [cooked, number]


def main():
    f = open("data/schedule.txt")
    parsed = process(f)
    print(parsed)


if __name__ == "__main__":
    main()
