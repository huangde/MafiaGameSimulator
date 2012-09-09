# a simulator for mafia game
# required parameters:
#     n_player: total number of players at the beginning of the game
#     n_killer: initial killer number
#     n_police: initial police number
#     n_game:   number of games being played

# strategy:
#     killer:randomly kill
#     police:randomly identify killer
#     voting:all people randomly vote before police find out killer
#     if killer is known, he will be voted out immediatly,remain killer will
#     have higher posibility kill a police in the next round
#     nobody can vote for himself

# ending condition:
#     all killer being voted out,police win
#     all police being killed, killer win
# DONE:   1) consider draw game
        # 2) posibility change of police being killed
        # 3) police check all civlians and game is not end
# CANCEL:   4) police publish checklist after dead/vote out
#(NOTE: not matter who expose checklist, either police,cilivian or
#     killer, it decrease the voting rate of people in the list,all
#     other people's voting number increase at the same rate,unless
#     the guy in the known list is in fact a killer)
# CANCEL: 5) a new posibility algorithm focus on killer number
        #    (NOTE: current posibility model is better)
         # 6)adding a godfather,he is a killer but cannot be recognize
         # by police(please read godfather.py)

from random import randint

def game():
    n_killer=2
    n_player=8
    n_police=2
    game_end=False
    player_ID=range(n_player)
    policeID=range(n_police)
    checklist=[]
    w=0.9 #chance vote for other peoples
          #for police and killer,this ratio is the chance
          #not vote for self's partner
    for i in policeID:
        checklist.append(i)
    print '***********game begin***************'
    while (not game_end):
        # if game is not end
        # killers can not kill themselves
        ###################################
        # killer is killing
        killers=[player_ID.pop() for i in range(n_killer)]
        killed=randint(0,len(player_ID)-1)
        print player_ID[killed],'is killed'
        # one guy is radomly killed
        if player_ID[killed] in policeID:
            # police being killed
            n_police-=1
        if n_police==0:
            # all police being killed
            game_end=True
            killer_win=True
            break
        if player_ID[killed] in checklist:
            checklist.pop(checklist.index(player_ID[killed]))
        player_ID.pop(killed)
        [player_ID.append(killers[i]) for i in range(len(killers))]
        ###################################
        # police checking
        check=randint(0,len(player_ID)-1)
        # donot check the same guy twice
        while player_ID[check] in checklist:
            check=randint(0,len(player_ID)-1)
        print 'the police check',player_ID[check] 
        if player_ID[check] in killers:
            find_killer=True
        else:
            find_killer=False
            checklist.append(player_ID[check])
        # police check all cilivan and only one killer left
        if not find_killer:
            if  len(checklist)==len(player_ID)-1:
                find_killer=True
                check=(set(player_ID)-set(checklist)).pop()
                check=player_ID.index(check)
        ###################################
        if find_killer:
            # find killer,not need to vote
            print player_ID[check],'is a killer,and is voted out'
            n_killer-=1
            if n_killer==0:
                game_end=True
                killer_win=False
                break
            # checklist.pop(checklist.index(player_ID[check]))
            player_ID.pop(check)
        else:
            #calculate the chance of being vote out
            nc=len(player_ID)-n_police-n_killer #number of cilivian
            nil=len(checklist) #number of people alive and be checked
            nt=len(player_ID) #number of people alive
            vote=[0 for i in range(nt)]
            vc=w/(nt-1) #average vote from one cilivian
            vs=1.0-w    #average vote from self/one partner
            vk=w/(nt-n_killer) #average vote from one killer
            vp=w/(nt-nil)      #average vote from one police
            for i in range(nt):
                #cilivian & police
                if player_ID[i] in checklist:
                    vote[i]=vc*(nc-1)+vs+vs*n_police/nil+vk*n_killer
                else:
                    vote[i]=vc*(nc-1)+vs+vp*n_police+vk*n_killer
                #update police
                if player_ID[i] in policeID:
                    vote[i]=vc*nc+vs*n_police/nil+vk*n_killer
                if player_ID[i] in killers:
                    vote[i]=vc*nc+vs+vp*n_police
            # voting
            # evenly voting
            # voted=randint(0,len(player_ID)-1)
            # vote base on the posibility array
            voted=WheelSelect(vote)
            print player_ID[voted],'is voted out'
            if player_ID[voted] in policeID:
                #police being voted out
                n_police-=1
            if n_police==0:
                game_end=True
                killer_win=True
                break
            if player_ID[voted] in killers:
                #killer being voted out
                n_killer-=1
            if n_killer==0:
                game_end=True
                killer_win=False
                break
            if player_ID[voted] in checklist:
                checklist.pop(checklist.index(player_ID[voted]))
            player_ID.pop(voted)
        # print  player_ID,n_killer,n_police,checklist,vote,sum(vote)
    return killer_win

def WheelSelect(vote):
    #select one person to vote out base one the posibility array
    tmp=[]
    n_throw=1 #throw number=1 give pretty close answer
               # as n_throw=1000, while n=10 overestimate
               # interesting
    for throws in range(n_throw):
        i=randint(0,len(vote)-1)
        beta=2*max(vote)+i
        while beta>vote[i]:
            beta-=vote[i]
            i=(i+1)%len(vote)
        tmp.append(i)
    i=max(set(tmp),key=tmp.count)
    return i


if __name__ == '__main__':
    hands=10000
    killer_win=0
    for i in range(hands):
        result=game()
        if result:
            killer_win+=1
    print killer_win,hands
        
        
    
