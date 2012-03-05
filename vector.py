from misc import Failure

class Vector(object):
    
    def __init__(self, arg):
      """ 
      This is the ctor for the Vector object. It allows
      for either an integer or sequence argument. 
      Right now, it only recognizes tuple and list sequences.

      For sanity sake, it uses a list as its internal data structure. 
      """
      if isinstance(arg, (int, long)):
        if arg < 0:
          raise ValueError('A vector can not have a negative length.')
        else:
          self.list = [0.0 for x in range(arg)]
      elif isinstance(arg, (tuple, list)):
        self.list = [x for x in arg]
      else:
        raise TypeError('A vector must be instanciated with a length or sequence.')

    def __repr__(self):
      """
      This function returns the string representation of Vector.
      It merely stringifies the internal list. 
      """
      return 'Vector(' + str(self.list) + ')'

    def __iter__(self):
      """
      This function returns the iterator of the internal list object. 
      """
      return self.list.__iter__()

    def __len__(self):
      """
      This function returns the lenght of the internal list object.
      """
      return len(self.list)

    def __add__(self, other):
      """
      This function adds to vectors. If the other argument is not a vector, then
      the function uses the Vector ctor to create a vector and perform the + operation.
      
      If other is a vector, then it iterates over both lists, adding the values at matching
      inidices. The resulting value is a new Vector. 
      """
      if isinstance(other, (list, tuple)):
        return self + Vector(other)
      else:
        tmp = []
        for i, o in enumerate(other):
          tmp.append(self.list[i] + o)
        return Vector(tmp)

    def __radd__(self, other):
      """
      This function is available for circumstance where a non Vector type is 
      added to a Vector. It merely exposed the functionality of __add__.
      """
      return self.__add__(other)

    def dot(self, other):
      """
      This function performs the dot product on two vectors or sequences. 
      The return value is a new Vector.
      """
      a = self.list
      b = other if isinstance(other, (tuple, list)) else other.list
      product = 0
      for i in range(len(a)):
        product += a[i] * b[i]
      return product  

    def __getitem__(self, key):
      """ 
      This function exposes slicing and retrieval from the internal list.
      """
      if isinstance(key, int) and key >= len(self.list):
        raise IndexError('Index of vector out of bounds.')
      elif isinstance(key, slice):
        return self.list[key.start:key.stop:key.step]
      else:
        return self.list[key]

    def __setitem__(self, key, value):
      """ 
      This function allows setting of the internal list.
      """
      if isinstance(key, slice):
        self.list[key.start:key.stop:key.step] = value
      else:
        self.list[key] = value

    def __eq__(self, other):
      """ 
      This function compares two Vectors for equality. If something other than
      a Vector is compared to a Vector, then the result will always be false.
      Otherwise, each ordinal value is compared is compared within each respective 
      intern list.
      """
      if not isinstance(other, Vector):
        return False
      
      for i, s in enumerate(self.list):
        if s != other[i]:
          return False
        return True
    
    def __ne__(self, other):
      """ 
      Not equal is the impelementing by notting the result of __eq__.
      """
      return not self.__eq__(other)

    def __gt__(self, other):
      """ 
      This function determines whether one Vector is greater than another Vector.
      If clones the internal lists of each Vector, then sorts them. It proceeds by
      then comparing each ordinal value. If a value is found to be greater than the
      other, it immediately return True. If none are found to be greater than, then
      the function returns False.
      """
      slist = self.list[:]
      olist = other if isinstance(other, (tuple, list)) else other.list[:]
      slist.sort()
      olist.sort()
      slist = [ x for x in reversed(slist)]
      olist = [ x for x in reversed(olist)]

      for i, s in enumerate(slist):
        if s > olist[i]:
          return True

      return False

    def __ge__(self, other):
      """
      This function is very similar to __gt__; however, instead of attempting to
      find a sorted value greater than other's it instead attempts to find a value
      less than other's to return False.
      """
      slist = self.list[:]
      olist = other if isinstance(other, (tuple, list)) else other.list[:]
      slist.sort()
      olist.sort()
      slist = [ x for x in reversed(slist)]
      olist = [ x for x in reversed(olist)]

      for i, s in enumerate(slist):
        if s < olist[i]:
          return False

      return True

    def __lt__(self, other):
      """
      Less than is implemented as NOT EQ AND NOT GE.
      """
      return not self.__gt__(other) and not self.__ge__(other)

    def __le__(self, other):
      """ 
      Less than equal is implemented as NOT GE AND NOT EQ
      """
      return not self.__ge__(other) and not self.__eq__(other)

