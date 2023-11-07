def parse(self, commands: str) -> bool:
    temp = commands.split(" ")
    if temp.size() <= 3:
        if temp[0] != "not":
            if temp[1] == "and":
                return occupancy[temp[0]] and occupancy[temp[2]]
            elif temp[1] == "or":
                return occupancy[temp[0]] or  occupancy[temp[2]]
            else :
                return occupancy[temp[0]]

    parenth = 0
    thislist = []

    for j in range(len(temp)):
        for i in temp[j]:
            if i == "(":
                parenth += 1
                if parenth == 1:
                    temp[j] = temp[j][i:]
            if i == ")":
                parenth -= 1
                if parenth == 0:
                    temp[j] = temp[j][:i]
                    thislist.append(temp[j])
        if parenth > 0:
            thislist.append(temp[j])

    if len(thislist) > 0:
        instr = " ".join(thislist)
        logic = parse(self, instr)




