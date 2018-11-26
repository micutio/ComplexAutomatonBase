"""
Statistics module, for providing statistics about the user authored simulations
as well as the underlying engine.
"""

import time
import cab.util.logging as cab_log

def timedmethod(method):
    """
    Decorator for methods. Enables timing of the method execution.
    Taken from https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
    Example execution:
        @timedmethod
        def get_all_employee_details(**kwargs):
            print 'employee details'
        
        logtime_data = {}
        employees = Employee.get_all_employee_details(log_time=logtime_data)
    """
    def timed(*args, **kw):
        t_start = time.time()
        result = method(*args, **kw)
        t_end = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((t_end - t_start) * 1000)
        else:
            cab_log.debug('method time [{0}] : {1} ms'.format(method.__name__, (t_end - t_start) * 1000))

        return result
    return timed
