from misc import Failure

class profiled(object):
    def __init__(self,f):
        self.__count=0
        self.__f=f
        self.__name__=f.__name__
    def __call__(self,*args,**dargs):
        self.__count+=1
        return self.__f(*args,**dargs)
    def count(self):
        return self.__count
    def reset(self):
        self.__count=0

class traced(object):
    def __init__(self, f):
      """
      This is the ctor for the traced a decorator.
      It defines the field next_line as an empty string. 
      next_line is used to build up the progressive ASCII characters
      that make up the outline. 
      """
      self.__name__ = f.__name__
      self.f = f
      self.next_line = ''

    def __call__(self, *args, **kwargs):
      """
      This function implements the behavior of the traced decorator.
      Most of the logic builds up the out string which will be printed
      after the function has returned. next_line is the beginning of out.
      This function prints name parameters differently for clarity sake.
      """
      out = self.next_line + ',- ' + self.__name__
      
      if len(args) == 1:
        out += '(' + str(args[0]) + ')'
      elif len(args) > 1:
        out += str(args)
      else:
        out += '('
        for i, key in enumerate(kwargs):
          out += str(key) + '=' + str(kwargs[key])
          if i != len(kwargs) - 1:
            out += ', '
        out += ')'

      print out

      self.next_line += '| '

      derp = ''

      if len(args) > 0:
        derp = self.f(*args)
      elif len(kwargs) > 0:
        derp = self.f(**kwargs)
 
      # slice next_line to regress the outline down
      # to the final return value
      self.next_line = self.next_line[2:] 
      print self.next_line + '`- ' + str(derp)
      if len(self.next_line) == 0:
        print derp
      return derp

class memoized(object):
    mem = { }
    def __init__(self, f):
        """
        This is the ctor for the memoized decorator.
        It assigns memoized's __name__ to the the function's and stores the function.
        """
        self.__name__ = f.__name__
        self.f = f

    def __call__(self, *args, **kwargs):
      """
      This function uses *args and **kwargs to create a unique key for the function call.
      First a check is made to the internal dictionary for this key, if it exists, then
      the stored value is immediately returned. Otherwise, the internal function f is called
      using the whichever arguments are avaiable. The results are stored in the dictionary
      for later use.
      """
      key = (self.__name__, str(args), str(kwargs))
      if self.mem.has_key(key) == True:
        return self.mem[key]
      else:
        out = ''
        if len(args) > 0:
          out = self.f(*args)
        elif len(kwargs) > 0:
          out = self.f(**kwargs)
        self.mem[key] = out
        return out


# run some examples.  The output from this is in decorators.out
def run_examples():
    for f,a in [(fib_t,(7,)),
                (fib_mt,(7,)),
                (fib_tm,(7,)),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp.reset,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (even_t,(6,)),
                (quicksort_t,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (change_t,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                ]:
        print "RUNNING %s(%s):" % (f.__name__,", ".join([repr(x) for x in a]))
        rv=f(*a)
        print "RETURNED %s" % repr(rv)

@traced
def fib_t(x):
    if x<=1:
        return 1
    else:
        return fib_t(x-1)+fib_t(x-2)

@traced
@memoized
def fib_mt(x):
    if x<=1:
        return 1
    else:
        return fib_mt(x-1)+fib_mt(x-2)

@memoized
@traced
def fib_tm(x):
    if x<=1:
        return 1
    else:
        return fib_tm(x-1)+fib_tm(x-2)

@profiled
@memoized
def fib_mp(x):
    if x<=1:
        return 1
    else:
        return fib_mp(x-1)+fib_mp(x-2)

@traced
def even_t(x):
    if x==0:
        return True
    else:
        return odd_t(x-1)

@traced
def odd_t(x):
    if x==0:
        return False
    else:
        return even_t(x-1)

@traced
def quicksort_t(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_t([x for x in l[1:] if x<pivot])
    right=quicksort_t([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

@traced
@memoized
def quicksort_mt(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_mt([x for x in l[1:] if x<pivot])
    right=quicksort_mt([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

class ChangeException(Exception):
    pass

@traced
def change_t(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_t(l[1:],a)
    else:
        try:
            return [l[0]]+change_t(l,a-l[0])
        except ChangeException:
            return change_t(l[1:],a)

@traced
@memoized
def change_mt(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_mt(l[1:],a)
    else:
        try:
            return [l[0]]+change_mt(l,a-l[0])
        except ChangeException:
            return change_mt(l[1:],a)


