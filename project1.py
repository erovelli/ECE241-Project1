"""
Evan Rovelli
UMass ECE 241 - Advanced Programming
Project #1   Fall 2021
project1.py - Sorting and Searching

"""
import time
import random

"""
Tree Node class 
"""
class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


"""
Stock class for stock objects
"""
class Stock:
    """
    Constructor to initialize the stock object
    """

    def __init__(self, sname, symbol, val, prices):
        self.sname = sname   # stock name
        self.symbol = symbol # stock symbol
        self.val = val       # stock value
        self.prices = prices # end day stock prices

    """
    return the stock information as a string, including name, symbol, 
    market value, and the price on the last day (2021-02-01). 
    For example, the string of the first stock should be returned as: 
    “name: Exxon Mobil Corporation; symbol: XOM; val: 384845.80; price:44.84”. 
    """
    def __str__(self):
        stock_string = "name: %s; symbol: %s; val: %s; price:%s" % (self.sname, self.symbol, self.val, self.prices[-1])
        return stock_string


"""
StockLibrary class to mange stock objects
"""
class StockLibrary:
    """
    Constructor to initialize the StockLibrary
    """

    def __init__(self):
        self.stockList = []   # stock list
        self.size = 0         # stock list size
        self.isSorted = False # is stock list sorted
        self.bst = None       # stock list BST root node

    """
    The loadData method takes the file name of the input dataset,
    and stores the data of stocks into the library. 
    Make sure the order of the stocks is the same as the one in the input file. 
    """
    def loadData(self, filename: str):
        file = open(filename, 'r') #open csv
        lines = file.readlines()
        file.close() #close csv
        for ln in lines:
            if ln == lines[0]: #skip header line
                continue
            else: #format line to object
                sname, symbol, val, *prices = ln.split('|')
                self.stockList.append(Stock(sname, symbol, float(val), prices))

        self.size = len(self.stockList) # sets stock list size from loaded data

    """
    The linearSearch method searches the stocks based on sname or symbol.
    It takes two arguments as the string for search and an attribute field 
    that we want to search (“name” or “symbol”). 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def linearSearch(self, query: str, attribute: str):
        if attribute == "name": # if searching by stock name
            for stock in self.stockList:
                if stock.sname == query:
                    return stock
                    break
                elif stock == self.stockList[-1]: # if stock reaches last item and isn't the query, returns not found
                    return "Stock not found"

        elif attribute == "symbol": # if searching by stock symbol
            for stock in self.stockList:
                if stock.symbol == query:
                    return stock
                    break
                elif stock == self.stockList[-1]: # if stock reaches last item and isn't the query, returns not found
                    return "Stock not found"

    """
    Sort the stockList using QuickSort algorithm based on the stock symbol.
    The sorted array should be stored in the same stockList.
    Remember to change the isSorted variable after sorted
    """
    def quickSort(self):
        self.quickSortHelper(0, len(self.stockList) - 1) # formats recursive function quickSortHelper
        self.isSorted = True

    def quickSortHelper(self, first, last):
        if first < last:
            splitpoint = self.partition(first, last)

            ### iterates new steps
            self.quickSortHelper(first, splitpoint - 1)
            self.quickSortHelper(splitpoint + 1, last)

    def partition(self, first, last):
        pivotvalue = self.stockList[first].symbol # reference value

        leftmark = first + 1
        rightmark = last

        done = False
        while not done: # compares marks to pivot value

            while leftmark <= rightmark and self.stockList[leftmark].symbol <= pivotvalue:
                leftmark = leftmark + 1

            while self.stockList[rightmark].symbol >= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True
            else: # swaps left and right marks
                temp = self.stockList[leftmark]
                self.stockList[leftmark] = self.stockList[rightmark]
                self.stockList[rightmark] = temp

        ### swaps left and right marks
        temp = self.stockList[first]
        self.stockList[first] = self.stockList[rightmark]
        self.stockList[rightmark] = temp

        return rightmark

    """
    build a balanced BST of the stocks based on the symbol. 
    Store the root of the BST as attribute bst, which is a TreeNode type.
    """
    def buildBST(self):
        if self.isSorted is not True: # sorts data if not already already sorted
            self.quickSort()
            self.buildBST()

        slist = self.stockList
        self.bst = self.buildBSTHelper(slist)

    ### creates left and right children until only leafs are avaiable, then returns root node
    def buildBSTHelper(self, slist):
        if not slist:
            return None
        else:
            mid = len(slist) // 2
            node = TreeNode(slist[mid].symbol, slist[mid])
            node.leftChild = self.buildBSTHelper(slist[:mid])
            node.rightChild = self.buildBSTHelper(slist[mid + 1:])
            return node

    """
    Search a stock based on the symbol attribute. 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def searchBST(self, query):
        res = self._searchBST(query, self.bst)
        if res:
            return res.payload
        else:
            return "Stock not found"

    def _searchBST(self, query, currentNode):
        if not currentNode: # called node is from leaf
            return None
        elif currentNode.key == query: # check for query
            return currentNode
        elif query < currentNode.key: # repeats function for left child if query is less than current node
            return self._searchBST(query, currentNode.leftChild)
        else: # repeats function for right child if query is greater than current node
            return self._searchBST(query, currentNode.rightChild)


# WRITE YOUR OWN TEST UNDER THIS IF YOU NEED
if __name__ == '__main__':
    stockLib = StockLibrary()
    testSymbol = 'GE'
    testName = 'General Electric Company'

    print("\n-------load dataset-------")
    stockLib.loadData("stock_database.csv")
    print(stockLib.size)

    print("\n-------linear search-------")
    print(stockLib.linearSearch(testSymbol, "symbol"))
    print(stockLib.linearSearch(testName, "name"))

    print("\n-------quick sort-------")
    print(stockLib.isSorted)
    stockLib.quickSort()
    print(stockLib.isSorted)

    print("\n-------build BST-------")
    t3 = time.time()
    stockLib.buildBST()
    bstbuild = time.time() - t3
    print(stockLib.bst.payload)

    print("\n---------search BST---------")
    print(stockLib.searchBST(testSymbol))

    print("\nQuestion 7-9:")
    random.seed(1)
    stockList2 = []
    for i in range(100): # creates list of 100 random stocks
        stockList2.append(stockLib.stockList[random.randint(0, len(stockLib.stockList))].symbol)

    lsearchList = []
    t1 = time.time() # begin linear search time trial
    for j in stockList2: # linear search test
        lsearchList.append(stockLib.linearSearch(j, "symbol"))
    lsearch = (time.time() - t1) / 100 # linear search average

    bsearchList = []
    t2 = time.time() # begin binary search time trial
    for k in stockList2: # binary search test
        bsearchList.append(stockLib.searchBST(j))
    bsearch = (time.time() - t2) / 100 # binary search average

    print("build bst", bstbuild)
    print("linear search average", lsearch)
    print("build search average", bsearch)

    print("\nQuestion 10:")
    slen = 0
    cmp = None
    for d in stockLib.stockList:
        if len(d.sname) > slen:
            slen = len(d.sname)
            cmp = d

    print(cmp) # longest stock name
    print(cmp.prices) # prices for graphing

    print("\nQuestion 11:")
    deltHigh = (float(stockLib.stockList[0].prices[-1]) / float(stockLib.stockList[0].prices[-1]) - 1) * 100 #initial change reference
    deltLow = deltHigh
    deltHighStock = None
    deltLowStock = None
    for v in stockLib.stockList:
        vi = float(v.prices[0]) # starting stock price
        vf = float(v.prices[-1]) # end stock price

        if (vf / vi - 1) * 100 > deltHigh:
            deltHigh = (vf / vi - 1) * 100
            deltHighStock = v
        elif (vf / vi - 1) * 100 < deltLow:
            deltLow = (vf / vi - 1) * 100
            deltLowStock = v

    print("Greatest positive change {0}% by {1}".format(round(deltHigh, 2), deltHighStock))
    print("Greatest negative change {0}% by {1}".format(round(deltLow, 2), deltLowStock))

