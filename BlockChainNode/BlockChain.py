import datetime
import hashlib
import json

class Block():
    
    def __init__(self,index:int, timestamp:str, data:dict):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = "0"
        # Calculate the hash of block
        self.hash = self.calculateHash()
        
    def calculateHash(self):
        return hashlib.sha256( (str(self.index) + self.previousHash + self.timestamp + json.dumps(self.data)).encode("utf-8") ).hexdigest()
    
    def toDict(self):
        return {
            "Index": self.index,
            "Timestamp": self.timestamp,
            "Data": self.data,
            "PreviousHash": self.previousHash,
            "Hash": self.hash
            }
    
class Blockchain():
    """A blockchain class that contains methods to manage a blockchain."""

    def __init__(self):
        """
        Initialize the blockchain with a genesis block.
        """
        self.chain = [self.createGenesisBlock(), self.createStartBlock('Test')]
        self.wallets = {}  # Dictionary to store wallet addresses and blockchain identities
        
    def createGenesisBlock(self):
        """
        Create and return the genesis block of the blockchain.
        """
        
        return Block(0, datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'), data = {
        'TimeStamp': datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'),  #TimeStamp of the message
        'RoomName': 'Lobby',  # Room name from which the client chats from
        'UserID': 'SERVER',  # User ID for tracking user activity
        'Name': 'SERVER', # UserName for the user who is chatting
        'Message': 'GenesisBlock' , # Message to be sent by the user
        })
    
    def createStartBlock(self,roomname):
        return Block(0, datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'), data = {
        'TimeStamp': datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'),  #TimeStamp of the message
        'RoomName': f'{roomname}',  # Room name from which the client chats from
        'UserID': 'SERVER',  # User ID for tracking user activity
        'Name': 'SERVER', # UserName for the user who is chatting
        'Message': 'GenesisBlock' , # Message to be sent by the user
        })

    def getLatestBlock(self):
        """
        Return the latest block in the blockchain.
        """
        return self.chain[len(self.chain) - 1]

    def addBlock(self, newBlock: Block):
        """
        Add a new block to the blockchain with the previous hash set to the
        hash of the latest block.
        """
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)

    def toDict(self):
        """
        Convert the blockchain into a list of dictionaries for each block.
        """
        chainInfo = []
        for block in self.chain:
            chainInfo.append(block.toDict())
        return chainInfo

    def isChainValid(self):
        """
        Validate the integrity of the blockchain by checking the hash and
        previous hash of each block.
        """
        i = 1
        while (i < len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            # Check if the current block's hash is equal to its calculated hash
            if (currentBlock.hash != currentBlock.calculateHash()):
                return False

            # Check if the previous hash of the current block is equal to the hash
            # of the previous block
            if (currentBlock.previousHash != previousBlock.hash):
                return False

            i += 1
        
        return True
    
    def getBlock(self, nOfBlock, roomname) -> dict:
        blockDict = None
        for i in range(len(self.chain)):
            block = self.chain[i]
            if block.data["RoomName"] == roomname:
                blockDict = block.toDict()
            
        return blockDict
    
    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                self.wallets = json.load(file)
        except FileNotFoundError:
            # File not found, initialize with an empty dictionary
            self.wallets = {}

    def save_data(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.wallets, file)

    def register_wallet(self, wallet_address, blockchain_identity):
        # Register a new wallet address with its associated blockchain identity
        self.wallets[wallet_address] = blockchain_identity
        self.save_data('wallets.json')

    def get_blockchain_identity(self, wallet_address):
        # Retrieve the blockchain identity associated with a wallet address
        return self.wallets.get(wallet_address)
        
 
 
"""
GCoin = Blockchain()
GCoin.addBlock(Block(len(GCoin.chain), "02/01/2024", {"amount" : 4}))
GCoin.addBlock(Block(len(GCoin.chain), "03/01/2024", {"amount" : 10}))

print(f"Is BlockChain Valid: {GCoin.isChainValid()}")

GCoin.chain[2].data = {"amount" : 100000}

print(f"Is BlockChain Valid: {GCoin.isChainValid()}")
        
print( json.dumps(GCoin.toDict(), indent= 4) )
"""       