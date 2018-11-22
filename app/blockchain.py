import hashlib
import json

class Block:
    def __init__(self,index,timestamp,data,previousHash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.hash = ""

    def calculateHash(self):
        hash = str(self.index) + str(self.previousHash)+str(self.timestamp)+str(self.data)
        return hashlib.sha256(hash)
    
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.chain += [self.createBlock()]

    def createBlock(self):
        return Block(0,"01/01/2017","1","0")

    def getLastBlock(self):
        return self.chain[len(self.chain)-1]

    def addBlock(self,newBlock):
        newBlock.previousHash = self.getLastBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.insert(len(self.chain),newBlock)


block = Blockchain()

block.addBlock(Block(1,"01/01/2018",4,""))
block.addBlock(Block(2,"01/01/2018",10,""))

print (block)