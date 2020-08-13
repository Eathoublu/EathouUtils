# coding:utf8
import time
import copy
import pandas as pd

class Experimenter:
    def __init__(self, verbose, log_filename='explog_{}.log'):
        self.statistic = []
        self.verbose = verbose
        self.log_filename = log_filename

    def statistic_to_csv(self):
        k = [i for i in self.statistic[0]]
        data = []

        for record in self.statistic:
            sub_data = [record[i] for i in k]
            data.append(sub_data)
        df = pd.DataFrame(data)
        df.columns = k
        df.to_csv(self.log_filename.format(time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()+8*60*60))))

    @staticmethod
    def arg_factory(args, scope):
        def inc(idx):
            scope_arg_index[idx] += 1
            if scope_arg_index[idx] >= scope_arg_length[idx]:
                scope_arg_index[idx] = 0
                if idx != scope_arg_num-1:
                    inc(idx+1)
                    return 0
                else:
                    return 0
            else:
                return 0

        scope_arg_length = [len(scope[i]) for i in scope]
        scope_arg_index = [0 for _ in scope]
        scope_arg_num = len(scope)
        while True:
            _tmp_args = copy.deepcopy(args)
            _idx = 0
            for ar in scope:
                _tmp_args[ar] = scope[ar][scope_arg_index[_idx]]
                _idx += 1
            yield _tmp_args
            FLAG = False
            for _i in range(scope_arg_num):
                if scope_arg_length[_i] - 1 > scope_arg_index[_i]:
                    FLAG = True
            if not FLAG:
                break
            inc(0)

    def run(self, execute_func, args={}, args_scope={}): # args中，需要尝试的args，留空，放入args_scope中
        for k in args:
            if k is None:
                assert k in args_scope, '{} 参数未被传入!!!'.format(k)
        get_next_args = lambda x : x.next()
        arg_fac = self.arg_factory(args, args_scope)
        while True:
            try:
                current_args = get_next_args(arg_fac)
                if self.verbose:
                    print(current_args)
                res = execute_func(**current_args)
                assert isinstance(res, dict), 'func result must be dict!'
                for k in current_args:
                    if k in res:
                        res['_'+k+'_'] = current_args[k]
                    else:
                        res[k] = current_args[k]
                self.statistic.append(res)
                if self.verbose:
                    print('-'*150)
                    print('-' * 150)
                    print('完成一个任务。')

            except:
                if self.verbose:
                    print('所有参数被执行完毕，任务结束～')
                break
        self.statistic_to_csv()

if __name__ == '__main__':
    def func(a, b, c):
        return {'a+b':a+b, 'a+c': a+c}

    exp = Experimenter(verbose=False)
    exp.run(execute_func=func, args={'a': 1, 'b':None, 'c':None}, args_scope={'b':[1, 2, 3], 'c':[4, 5, 6]})
