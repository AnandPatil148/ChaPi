import datetime
import hashlib
import json

class Block():
    
    def __init__(self,index:int, timestamp:str, data:dict, mintedBy:str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.mintedBy = mintedBy
        self.previousHash = "0"
        # Calculate the hash of block
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        return hashlib.sha256( (str(self.index) + self.timestamp + json.dumps(self.data) + self.mintedBy + self.previousHash).encode("utf-8") ).hexdigest()
    
    def to_dict(self):
        return {
            "Index": self.index,
            "Timestamp": self.timestamp,
            "Data": self.data,
            "MintedBy": self.mintedBy,
            "PreviousHash": self.previousHash,
            "Hash": self.hash
            }
        
    @staticmethod
    def to_block(b_dict):
        b = Block(b_dict["Index"], b_dict["Timestamp"], b_dict["Data"], b_dict["MintedBy"])
        b.previousHash = b_dict["PreviousHash"]
        b.hash = b.calculate_hash()
        return b
    
class Blockchain():
    """A blockchain class that contains methods to manage a blockchain."""

    def __init__(self):
        """
        Initialize the blockchain with a genesis block.
        """
        self.chain = [self.create_genesis_block()]

        self.wallets = {}  # Dictionary to store wallet addresses and blockchain identities
    
    def get_chain_length(self):
        """Returns the length of the chain."""
        return len(self.chain)
    
    def create_genesis_block(self):
        """
        Create and return the genesis block of the blockchain.
        """
        
        genesisBlock = Block(0, datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'), data = {
        'TimeStamp': datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'),  #TimeStamp of the message
        'RoomName': 'Lobby',  # Room name from which the client chats from
        'UserID': 'SERVER',  # User ID for tracking user activity
        'Name': 'SERVER', # UserName for the user who is chatting
        'Message': 'GenesisBlock' , # Message to be sent by the user
        }, mintedBy="SELF")
        
        with open('chain.json', 'r+', encoding='utf-8') as f:
            
            file_data = json.load(f)
            
            try: 
                file_data["Blocks"][0]["Index"]
                return genesisBlock
            except:
                file_data["Blocks"].append(genesisBlock.to_dict())
                f.seek(0)
                json.dump(file_data, f, ensure_ascii=False, indent=4)

        return genesisBlock
    
    def create_room_genesis_block(self, roomname, mintedBy):
        roomStartBlock = Block(self.get_chain_length(), datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'), data = {
        'TimeStamp': datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'),  #TimeStamp of the message
        'RoomName': f'{roomname}',  # Room name from which the client chats from
        'UserID': 'SERVER',  # User ID for tracking user activity
        'Name': 'SERVER', # UserName for the user who is chatting
        'Message': 'GenesisBlock' , # Message to be sent by the user
        }, mintedBy=mintedBy)
        
        self.add_block(roomStartBlock, roomBlockOrNot=True)
        
        with open('chain.json', 'r+', encoding='utf-8') as f:
            
            file_data = json.load(f)
            #Check if room genesis block is present or not
            for i in range(self.get_chain_length()):
                if "RoomName" in file_data["Blocks"][i]["Data"]:
                    return None
                else:
                    print("No Room Found")
            
                    file_data["Blocks"].append(roomStartBlock.to_dict())
                    f.seek(0)
                    json.dump(file_data, f, ensure_ascii=False, indent=4)
                    return None

    def get_latest_block(self):
        """
        Return the latest block in the blockchain.
        """
        return self.chain[len(self.chain) - 1]

    def add_block(self, newBlock: Block, roomBlockOrNot: bool):
        """
        Add a new block to the blockchain with the previous hash set to the
        hash of the latest block.
        """
        newBlock.previousHash = self.get_latest_block().hash
        newBlock.hash = newBlock.calculate_hash()
        self.chain.append(newBlock)
        
        if not roomBlockOrNot:
            with open('chain.json', 'r+', encoding='utf-8') as f:

                file_data = json.load(f)

                file_data["Blocks"].append(newBlock.to_dict())
                f.seek(0)
                json.dump(file_data, f, ensure_ascii=False, indent=4)

    def to_dict(self):
        """
        Convert the blockchain into a list of dictionaries for each block.
        """
        chainInfo = []
        for block in self.chain:
            chainInfo.append(block.to_dict())
        return chainInfo

    def is_chain_valid(self):
        """
        Validate the integrity of the blockchain by checking the hash and
        previous hash of each block.
        """
        i = 1
        while (i < len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            # Check if the current block's hash is equal to its calculated hash
            if (currentBlock.hash != currentBlock.calculate_hash()):
                return False

            # Check if the previous hash of the current block is equal to the hash
            # of the previous block
            if (currentBlock.previousHash != previousBlock.hash):
                return False

            i += 1
        
        return True
    
    def get_block(self, nOfBlock, roomname) -> dict:
        blockDict = None
        for i in range(self.get_chain_length()):
            block = self.chain[i]
            if block.data["RoomName"] == roomname:
                blockDict = block.to_dict()
        return blockDict
    
    def load_chain(self,filename):
        try:
            with open(filename, "rb") as f:
                data = json.load(f)
                chain = []
                
                for b_dict in data["Blocks"]:
                    b = Block.to_block(b_dict)
                    chain.append(b)
                self.chain = chain
        except FileNotFoundError:
            print("No existing blockchain found.")
                    
    def load_wallets(self, filename):
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
        
print( json.dumps(GCoin.to_dict(), indent= 4) )
"""       