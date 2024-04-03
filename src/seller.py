from bitcoinutils.setup import setup
from bitcoinutils.hdwallet import HDWallet


class seller:
    def __init__(self, mnemonic, basepath = "m/86'/1'/0'/0/0"):
        
        self.id = 0
        self.basepath = basepath
        self.address, self.pubkey, self.privkey = __generateAddress(mnemonic, basepath)


    def __generateAddress(mnemonic, basepath):
        setup("testnet")
        hdw_from_mnemonic = HDWallet(mnemonic=mnemonic)
        hdw_from_mnemonic.from_path(basepath)
        
        private = hdw_from_mnemonic.get_private_key()
        public = private.get_public_key()
        address = public.get_taproot_address()

        return address, public, private