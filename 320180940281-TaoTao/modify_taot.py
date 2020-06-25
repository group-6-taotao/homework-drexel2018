#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:28:14 2020

@author: wangfeng
"""

#!/usr/bin/env python3

# -*- coding: utf-8 -*-

'''format:    
python filename version number cumulative or not.

example :python modify_taot.py v4.4 10 --c=c

'''

import re, sys
from argparse import ArgumentParser
from subprocess import Popen, DEVNULL, PIPE


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
        if argument.accumulated == "c":
            accumulated = 1
        else:
            accumulated = 0
            print("Clarifu the meaning of %s" % argument.accumulated)
            sys.exit(-1)
        self.login(accumulated, rev_range)

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

    def login(self, accumulated, a_range):
        # setup and fill in the table
        print("#sublevel commits %s stable fixes" % self.a)
        print("time of lv is wrong") #tag for R data.frame
        a1 = self.a
    
        '''
        The reference time of v4.1 and v4.4 is used as the reference datum
         Fix this problem to get the time in bash from git!
         hofrat @ Debian: ~/git/linux-stable $ git log -1 --pretty = format: "%ct" v4.4
         1452466892
        '''

        for lasting in range(1,a_range+1):
            a2 = self.a + "." + str(lasting)
            bash_cnt = "git rev-list --pretty=format:\"%ai\" " + a1 + "..." + a2
            bash_tag = "git log -1 --pretty=format:\"%ct\" " + a2
            #show the result of bashcnt
            bash_a_list = Popen(bash_cnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            #show the result of list
            commit_cnt = self.get_commit_cnt(bash_a_list)# catch it

            if accumulated == 0:

                a1 = a2
            if commit_cnt:
                bash_tag_date = Popen(bash_tag, stdout=PIPE, stderr=DEVNULL, shell=True)#catch
                days = self.get_tag_days(bash_tag_date, self.basetime) # catch data
                print("%d %d %d" % (lasting,days,commit_cnt))
                """
                self.collect.append((sl,days,commit_cnt))
                collect them into list
                """
            else:
                break

if __name__ == "__main__":
    login = Taot_result()