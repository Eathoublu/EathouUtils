# coding:utf8
# HouseKeeper
# Author: Eathoublu_YixiaoLAN
import threading
import time

class HTask:
    def __init__(self):
        pass

    def start(self):
        try:
            self.run()
        except Exception as e:
            print('[ERROR]Thread Error: {}'.format(e))

    def run(self):
        raise NotImplementedError


class HouseKeeper(object):

    def __init__(self, starttime=00, endtime=00, timepermin=30, log='log.txt', stdlog=False):
        if starttime>25 or starttime<0:
            raise Exception('RangeError', 'Start time only accept 0-24 hour.')
        if endtime>25 or endtime<0:
            raise Exception('RangeError', 'End time only accept 0-24 hour.')
        self.__start_time = starttime
        self.__end_time = endtime
        self.__time_per_min = timepermin
        self.__task_list = []
        self.__task_flag = []
        self.__log_file = open(log, 'a')
        self.__std_log = stdlog
        self.__time_to_start = False
        self.__act_time = 60. / self.__time_per_min
        if self.__act_time < 1.:
            self.__act_time = 1
        self.__act_time = int(self.__act_time)
        self.__log("Start from: {} to: {} . Act every {} seconds.".format(self.__start_time, self.__end_time, self.__act_time))


    def add_task(self, task):
        if isinstance(task, HTask):
            self.__task_list.append(task)
            self.__task_flag.append(False)
        else:
            raise Exception('Not suitable object!')

    @staticmethod
    def __get_time(format="%Y-%m-%d %H:%M:%S"):
        return time.strftime(format, time.gmtime(time.time()+8*60*60))

    def __log(self, msg, msg_type='INFO'):
        log_string = '[{}][{}]: {}\n'.format(self.__get_time(), msg_type, msg)
        self.__log_file.write(log_string)
        if self.__std_log:
            print(log_string)

    def __see_times_come(self):
        if self.__start_time < self.__end_time:
            if int(self.__get_time("%H")) >= int(self.__start_time) and int(self.__get_time("%H")) <= int(self.__end_time):
                self.__time_to_start = True
                return False
            else:
                self.__start_time = False
                return True
        if self.__start_time == self.__end_time:
            self.__time_to_start = True
            return True
        if self.__start_time > self.__end_time:
            if int(self.__get_time("%H")) >= int(self.__start_time) and int(self.__get_time("%H")) <= int(self.__end_time):
                self.__time_to_start = True
                return True
            else:
                self.__time_to_start = False
                return False

    def __begin_task(self):
        self.__task_flag = [False for _ in self.__task_flag]
        __task_thread = [threading.Thread(target=i.start) for i in self.__task_list]
        for t in __task_thread:
            try:
                t.setDaemon(False)
            except:
                pass
        for t in __task_thread:
            try:
                t.start()
            except:
                pass
        time.sleep(0.5)


    def __act_now(self):
        if int(self.__get_time("%S")) % self.__act_time == 0:
            return True
        return False

    def start(self):
        while True:
            if self.__see_times_come():
                if self.__act_now():
                    self.__log("All tasks starts.")
                    self.__begin_task()
                    self.__log("All tasks finished.")
            else:
                time.sleep(0.5)



# Example Code:
class Task1(HTask):
    def __init__(self):
        HTask.__init__(self)
        pass
    def run(self):
        print('This is task 1')
        time.sleep(1)
        print('this is task 1-2')

class Task2(HTask):
    def __init__(self):
        HTask.__init__(self)
        pass
    def run(self):
        print('This is task 2')
        time.sleep(1)
        print('this is task 2-2')

class Task3(HTask):
    def __init__(self):
        HTask.__init__(self)
        pass
    def run(self):
        print('This is task 3')
        time.sleep(1)
        print('this is task 3-2')

def __test():
    house_keeper = HouseKeeper(00, 00, timepermin=15, stdlog=True)
    house_keeper.add_task(Task1())
    house_keeper.add_task(Task2())
    house_keeper.add_task(Task3())
    house_keeper.start()

if __name__ == '__main__':

    __test()

















