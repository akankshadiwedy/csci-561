# with sorted children according to days required  : optimization to prune more using alpha beta
import time
from threading import Thread

class Game():
    def __init__(self,shelterBeds,parkingSpace):
        self.spla_limit = parkingSpace
        self.lahsa_limit = shelterBeds
        self.pruning = True
        self.maxLevel = 40

    def terminalTest(self,node):
        return False

    def doPruning(self,spla_count,lahsa_count):
        if spla_count <= 10 and lahsa_count <=10:
            if spla_count <= 9 and lahsa_count <= 9:
                self.pruning = False
            if self.spla_limit <=3 and self.lahsa_limit <=3:
                self.pruning = False
        else:
            if spla_count < 20:
                self.pruning = True
                self.maxLevel = 8
            elif spla_count >= 20 and spla_count < 40:
                self.maxLevel = 6
            elif spla_count > 40 and spla_count <= 70 :
                self.maxLevel = 4
            else:
                self.maxLevel = 2


class Node():
    def __init__(self, applicant_id,requested_days,applicants, level, SChoseList, LChoseList):
        self.applicant_id = applicant_id
        self.requested_days = requested_days
        self.applicants = applicants
        self.spla_applicants = SChoseList
        self.lahsa_applicants = LChoseList
        self.level = level
        self.spla_score = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        self.lahsa_score = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        self.applicants_choosen = []
        self.applicants_not_choosen = []
        for ap in self.applicants:
            if ap['id'] in self.spla_applicants:
                self.applicants_choosen.append(ap)
            elif ap['id'] in self.lahsa_applicants:
                self.applicants_choosen.append(ap)
            else:
                self.applicants_not_choosen.append(ap)

    def nextNodes(self,player):
        next_node_list = []
        for ap in self.applicants_not_choosen:
            flag = False
            if (player == 'spla'):
                if (ap['car'] != 'Y' or ap['dl'] != 'Y' or ap['medCon'] != 'N'):
                    continue
                days_needed = list(ap['reqDays'])
                for x in range(0, 7):
                    if days_needed[x] == '1' and self.spla_score[x + 1] >= g.spla_limit:
                        flag = True
                        break
            else:
                if (ap['sex'] != 'F' or ap['pet'] != 'N' or ap['age'] <= 17):
                    continue
                days_needed = list(ap['reqDays'])
                for x in range(0, 7):
                    if days_needed[x] == '1' and self.lahsa_score[x + 1] >= g.lahsa_limit:
                        flag = True
                        break
            if flag:
                continue
            next_node = Node(ap['id'], ap['reqDays'],self.applicants, self.level + 1, self.spla_applicants, self.lahsa_applicants)
            next_node.applicants_choosen = []
            next_node.applicants_not_choosen = []
            next_node.spla_applicants = []
            next_node.lahsa_applicants = []
            for m in self.spla_applicants:
                next_node.spla_applicants.append(m)
            for m in self.lahsa_applicants:
                next_node.lahsa_applicants.append(m)
            if player == 'spla':
                next_node.spla_applicants.append(next_node.applicant_id)
            else:
                next_node.lahsa_applicants.append(next_node.applicant_id)
            for m in self.applicants_not_choosen:
                next_node.applicants_not_choosen.append(m)
            for m in self.applicants_choosen:
                next_node.applicants_choosen.append(m)
            next_node.applicants_not_choosen.remove(ap)
            next_node.applicants_choosen.append(ap)
            next_node.set_utility()
            next_node_list.append(next_node)
        return next_node_list


    def set_utility(self):
        self.spla_score = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        self.lahsa_score = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        for ap in applicants:
            if ap['id'] in self.spla_applicants:
                days_needed = list(ap['reqDays'])
                for x in range(0, 7):
                    if days_needed[x] == '1':
                        self.spla_score[x + 1] += 1
            elif ap['id'] in self.lahsa_applicants:
                days_needed = ap['reqDays']
                for x in range(0, 7):
                    if days_needed[x] == '1':
                        self.lahsa_score[x + 1] += 1

    def check_available_space(self,player,ap):
        flag = False
        if (player == 'spla'):
            days_needed = list(ap['reqDays'])
            for x in range(0, 7):
                if days_needed[x] == '1' and self.lahsa_score[x + 1] >= g.lahsa_limit:
                    flag = True
                    break
        else:
            days_needed = list(ap['reqDays'])
            for x in range(0, 7):
                if days_needed[x] == '1' and self.spla_score[x + 1] >= g.spla_limit:
                    flag = True
                    break
        if flag:
            return
        else:
            if(player=='spla'):
                days_needed = ap['reqDays']
                for x in range(0, 7):
                    if days_needed[x] == '1':
                        self.lahsa_score[x + 1] += 1
            elif(player=='lahsa'):
                days_needed = ap['reqDays']
                for x in range(0, 7):
                    if days_needed[x] == '1':
                        self.spla_score[x + 1] += 1
        return

    def get_eval(self,node):
        sum_spla = 0
        sum_lahsa = 0
        for v in node.spla_score.values():
            sum_spla += v
        for v in node.lahsa_score.values():
            sum_lahsa += v
        return [sum_spla,sum_lahsa,sum_spla-sum_lahsa]

#class ends


def set_domain(applicants):
    for ap in applicants:
        if (ap['car'] == 'Y' and ap['dl'] == 'Y' and ap['medCon'] == 'N'):
            spla_domain.append(ap['id'])
        if(ap['sex'] == 'F' and ap['pet'] == 'N' and ap['age'] > 17):
            lahsa_domain.append(ap['id'])
    #print len(spla_domain),spla_domain
    #print len(lahsa_domain),lahsa_domain
    g.doPruning(len(spla_domain),len(lahsa_domain))

def sort_next_nodes(next_nodes_list):
    if next_nodes_list:
        new_list = []
        common_nodes = {}
        not_common_nodes = {}
        for n in next_nodes_list:
            if n.applicant_id in spla_domain and n.applicant_id in lahsa_domain:
                common_nodes[n.applicant_id] = n.requested_days.count('1')
            else:
                not_common_nodes[n.applicant_id] = n.requested_days.count('1')
        common_nodes = sorted(sorted(common_nodes.items(), key=lambda k: k[0]), key=lambda k: k[1], reverse=True)
        not_common_nodes = sorted(sorted(not_common_nodes.items(), key=lambda k: k[0]), key=lambda k: k[1],
                                  reverse=True)
        for k in common_nodes:
            new_list.append((item for item in next_nodes_list if item.applicant_id == k[0]).next())
        for k in not_common_nodes:
            new_list.append((item for item in next_nodes_list if item.applicant_id == k[0]).next())
        return new_list
    else:
        return []


def alpha_beta_cutoff(node):
    return p_min_value(node,-float('inf'),float('inf'))

def p_max_value(node,alpha,beta):
    actions = node.nextNodes('spla')
    actions = sort_next_nodes(actions)
    path = None
    value = [-float('inf'),-float('inf'),-float('inf')]
    if node.level+1 == g.maxLevel:
        return node.get_eval(node),[]
    if g.terminalTest(node) or len(actions) == 0:
        if len(node.applicants_not_choosen) != 0:
            for ap in node.applicants_not_choosen:
                if ap['id'] in lahsa_domain:
                    node.check_available_space('spla',ap)
        return node.get_eval(node), []
    for a in actions:
        new_value,new_path = p_min_value(a,alpha,beta)
        if new_value[2] > value[2]:
            value = new_value
            path = new_path
            path.insert(0,a.spla_applicants[-1])
        if value[2] >= beta:
            return value,path
        alpha = max(alpha,value[2])
    return value,path

def p_min_value(node,alpha,beta):
    actions = node.nextNodes('lahsa')
    actions = sort_next_nodes(actions)
    path = None
    value = [-float('inf'), -float('inf'), float('inf')]
    if node.level+1 == g.maxLevel:
        return node.get_eval(node),[]
    if g.terminalTest(node) or len(actions) == 0:
        if len(node.applicants_not_choosen) != 0:
            for ap in node.applicants_not_choosen:
                if ap['id'] in spla_domain:
                    node.check_available_space('lahsa',ap)
        return node.get_eval(node), []
    for a in actions:
        new_value, new_path = p_max_value(a,alpha,beta)
        if new_value[2] < value[2]:
            value = new_value
            path = new_path
            path.insert(0,a.lahsa_applicants[-1])
        if value[2] <= alpha:
            return value,path
        beta = min(beta,value[2])
    return value, path


# Smaller test cases where no pruning is needed
def maximax(node):
    return min_value(node)

def max_value(node):
    actions = node.nextNodes('spla')
    actions = sort_next_nodes(actions)
    path = None
    if node.level+1 == g.maxLevel:
        return node.get_eval(node),[]
    if g.terminalTest(node) or len(actions) == 0:
        if len(node.applicants_not_choosen) != 0:
            for ap in node.applicants_not_choosen:
                if ap['id'] in lahsa_domain:
                    node.check_available_space('spla',ap)
        return node.get_eval(node), []
    value = [-float('inf'),-float('inf')]
    for a in actions:
        new_value,new_path = min_value(a)
        if new_value[0] > value[0]:
            value = new_value
            path = new_path
            path.insert(0,a.spla_applicants[-1])
    return value,path

def min_value(node):
    actions = node.nextNodes('lahsa')
    actions = sort_next_nodes(actions)
    path = None
    if node.level+1 == g.maxLevel:
        return node.get_eval(node),[]
    if g.terminalTest(node) or len(actions) == 0:
        if len(node.applicants_not_choosen) != 0:
            for ap in node.applicants_not_choosen:
                if ap['id'] in spla_domain:
                    node.check_available_space('lahsa',ap)
        return node.get_eval(node), []
    value = [-float('inf'),-float('inf')]
    for a in actions:
        new_value, new_path = max_value(a)
        if new_value[1] > value[1]:
            value = new_value
            path = new_path
            path.insert(0,a.lahsa_applicants[-1])
    return value, path


def findNextMove(node):
    global sol
    global bestID
    global bestEff
    global best_reqDays
    firstChoice = node.nextNodes("spla")
    firstChoice = sort_next_nodes(firstChoice)
    for fc in firstChoice:
        if g.pruning:
            #print "Pruning it"
            v = alpha_beta_cutoff(fc)
            sol[fc.applicant_id] = v
        else:
            #print "No Pruning"
            v = maximax(fc)
            sol[fc.applicant_id] = v
        if v[0][0] > bestEff:
            bestID = fc.applicant_id
            bestEff = v[0][0]
            best_reqDays = fc.requested_days.count('1')
        elif v[0][0] == bestEff:
            if int(fc.applicant_id) < int(bestID):
                bestID = fc.applicant_id
                bestEff = v[0][0]
                best_reqDays = fc.requested_days.count('1')
        #print fc.applicant_id, " : ", v[0], v[1]
    #print bestID,best_reqDays,bestEff


lines = [line.rstrip() for line in open("input.txt")]
shelterBeds = 0
parkingSpace = 0
LChoseCount = 0
SChoseCount = 0
applicantCount = 0
LChoseList = []
SChoseList = []
applicantData = []
lineCount = 0
d = {}
spla_domain = []
lahsa_domain = []
start = time.time()
for line in lines:
    lineCount += 1
    if(lineCount == 1):
        shelterBeds = int(line)
    elif(lineCount == 2):
        parkingSpace = int(line)
    elif(lineCount == 3):
        LChoseCount = int(line)
        Ldata = 4+LChoseCount
    elif(lineCount >= 4 and lineCount < Ldata):
        LChoseList.append(line)
    elif(lineCount == Ldata):
        SChoseCount = int(line)
        Sdata = lineCount+SChoseCount+1
    elif(lineCount >= Ldata+1 and lineCount < Sdata):
        SChoseList.append(line)
    elif(lineCount == Sdata):
        applicantCount = int(line)
    else:
        applicantData.append(line)

applicants = []
for i in range(len(applicantData)):
    temp = applicantData[i]
    d['id'] = temp[:5]
    d['sex'] = temp[5:6]
    d['age'] = int(temp[6:9])
    d['pet'] = temp[9:10]
    d['medCon'] = temp[10:11]
    d['car'] = temp[11:12]
    d['dl'] = temp[12:13]
    d['reqDays'] = temp[13:]
    #if d['age'] <= 100 and d['age'] > 0:
    applicants.append(d.copy())

g = Game(shelterBeds,parkingSpace)
node = Node('0000R','0000000',applicants,0,SChoseList,LChoseList)
node.set_utility()
set_domain(applicants)

sol = {}
bestID = None
bestEff = -float('inf')
best_reqDays = 0

import threading

class Solution(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

    def _stop(self):
        if self.isAlive():
            Thread._Thread__stop(self)

it = Solution(findNextMove,node)
it.start()
it.join(175)
if it.isAlive():
    it._stop()
    myOutput = open("output.txt", "w+")
    if bestID != None:
        myOutput.write(bestID)
    else:
        myOutput.write('00000')
    #print time.time() - start
else:
    myOutput = open("output.txt", "w+")
    if bestID != None:
        myOutput.write(bestID)
    else:
        myOutput.write('00000')
    #print time.time() - start
