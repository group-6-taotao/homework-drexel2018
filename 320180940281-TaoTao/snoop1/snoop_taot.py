#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:27:36 2020

@author: wangfeng
"""

'''format:    

example :python snoop_taot.py v4.4 10 --c=c

'''
"""
Author:Tao_Tao
ID:320180940281
email:1968719597@qq.com
github:group-6-taotao
"""

import re, sys
from argparse import ArgumentParser
from subprocess import Popen, DEVNULL, PIPE
import matplotlib.pyplot as plt


class Modify(BaseException):
    def __str__(self):
        error = 'The argument is wrong.'
        return error

class Taot_result(object):
    def __init__(self):
        # Set the arguments required for the class.
        analyse = ArgumentParser(description="analyse")
        analyse.add_argument('revision', help='The number of versions')
        analyse.add_argument('rev_range', type=str, help='The number of sublevels')
        analyse.add_argument('-c', '--cumulative', type=str, help='Whether accumulated.')
        argument = analyse.parse_args()
        self.basetime = 1452466892
        #Passing arguments to the analysis
        self.rev = argument.revision
        try:
            rev_range = int(argument.rev_range)
        except (ValueError, UnboundLocalError):
            err = '-r should be integer.'
            print(err)
        if argument.cumulative == "c":
            cumulative = 1
        else:
            cumulative = 0
            print("Clarifu the meaning of %s" % argument.cumulative)
            sys.exit(-1)
        self.login(cumulative, rev_range)

    def get_commit_cnt(self, bash):
        try:
            num_0 = bash.communicate()[0]
            if num_0 == 0:
               raise Modify
        except Modify as err:
            print(err)
            sys.exit(2)
            # when the number we need does not exist -> 0
        else:
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(num_0))
            return len(cnt)

    def get_tag_days(self,bash, base):
       try:
           miao = bash.communicate()[0]
           SecPerHour = 3600
           if miao == 0:
               raise Modify
       except Modify as err:
           print(err)
           sys.exit(2)
       return (int(miao)-base)//SecPerHour

    def login(self, cumulative, rev_range):
        # setup and fill in the table
        print("#sublevel commits %s stable fixes" % self.rev)
        print("time of lv is wrong") #tag for R data.frame
        rev1 = self.rev
    
        
#The reference time of v4.1 and v4.4 is used as the reference datum
#Fix this problem to get the time in bash from git!
#hofrat @ Debian: ~/git/linux-stable $ git log -1 --pretty = format: "%ct" v4.4
#1452466892

        self.sub,self.release_days,self.points =[],[],[]
        for lasting in range(1, rev_range+1):
            rev2 = self.rev + "." + str(lasting)
            bash_cnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            bash_tag = "git log -1 --pretty=format:\"%ct\" " + rev2
            #show the result of bashcnt
            bash_a_list = Popen(bash_cnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            #show the result of list
            cnt = self.get_commit_cnt(bash_a_list)# catch it

            if cumulative == 0:

                rev1 = rev2
            if cnt:
                bash_tag_date = Popen(bash_tag, stdout=PIPE, stderr=DEVNULL, shell=True)#catch
                days = self.get_tag_days(bash_tag_date, self.basetime) # catch data
                print("%d %d %d" % (lasting,days,cnt))
                self.sub.append(lasting) 
                self.release_days.append(days) 
                self.points.append(cnt)
                """
                self.collect.append((lasting,days,commit_cnt))
                collect them into list
                """
            else:
                break
    def visible(self):
        self.points = [self.points[0]]+[self.points[i]-self.points[i-1]  for i in range(1,len(self.points))]
        print(self.sub,self.points)
        plt.plot(self.sub,self.points,linestyle = 'solid') 
        plt.title("changement of fixes over sublevel") 
        plt.xlabel("times of fix commits") 
        plt.ylabel("release of kernel stable") 
        plt.savefig("graph1 4.4.png")
        plt.show()
        
        plt.scatter(self.sub,self.points,c ='red') 
        plt.title("changement of fixes over sublevel") 
        plt.xlabel("times of fix commits") 
        plt.ylabel("release of kernel stable") 
        plt.savefig("gragh2 4.4.png") 
        plt.show()
        
        plt.bar(self.sub,self.points) 
        plt.title("changement of fixes over sublevel") 
        plt.xlabel("times fix commits") 
        plt.ylabel("release of kernel stable") 
        plt.savefig("gragh3 4.4.png")
        plt.show()

 
if __name__ == "__main__":
    login1 = Taot_result()
    login1.visible()