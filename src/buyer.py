from bitcoinutils.setup import setup
from bitcoinutils.hdwallet import HDWallet


class Buyer:
    def __init__(self, id, mnemonic, basepath = "m/86'/1'/"):

        # id 0 is reserved for the seller
        self.id = id
        
        # id is used to create the derivation path
        self.basepath = basepath+str(id)+"'"+"/0/0"

        self.address, self.pubkey, self.privkey = self.__generateAddress(mnemonic, self.basepath)


    def __generateAddress(self, mnemonic, basepath):
        setup("testnet")
        hdw_from_mnemonic = HDWallet(mnemonic=mnemonic)
        hdw_from_mnemonic.from_path(basepath)
        
        private = hdw_from_mnemonic.get_private_key()
        public = private.get_public_key()
        address = public.get_taproot_address()

        return address, public, private

