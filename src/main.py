
from buyer import *
from bitcoinutils.setup import setup
from bitcoinutils.hdwallet import HDWallet



def main():
    setup("testnet")

    mnemonic = "bla bla bla bla bla bla bla bla bla bla bla bla"
    
    buyer1 = buyer(1, mnemonic)
    buyer2 = buyer(2, mnemonic)
    buyer3 = buyer(3, mnemonic)

    seller = seller(mnemonic)

    # Buyer addresses
    print("Buyer addresses:")
    print(buyer1.address.to_string())
    print(buyer2.address.to_string())
    print(buyer3.address.to_string())


    # Buyer UTXO to lock
    # [txid, output]
    buyer1_utxo = ["cfa027718ca18ec6a758126703d3222a9179f510d6fc11894b919981bdb3d498",3]
    buyer2_utxo = ["cfa027718ca18ec6a758126703d3222a9179f510d6fc11894b919981bdb3d498",1]
    buyer3_utxo = ["cfa027718ca18ec6a758126703d3222a9179f510d6fc11894b919981bdb3d498",2]

    # Create tx input from tx id of the buyers utxo
    buyer1_txin = TxInput(buyer1_utxo[0], buyer1_utxo[1])
    buyer2_txin = TxInput(buyer2_utxo[0], buyer2_utxo[1])
    buyer3_txin = TxInput(buyer3_utxo[0], buyer3_utxo[1])

    # Amounts from the input
    buyer1_funds = 0.001
    buyer2_funds = 0.001
    buyer3_funds = 0.001

    amount1 = to_satoshis(buyer1_funds)
    amount2 = to_satoshis(buyer2_funds)
    amount3 = to_satoshis(buyer3_funds)
    amounts = [amount1, amount2, amount3]

    # script pubkeys for signing the inputs
    script_pubkey1 = buyer1.address.to_script_pub_key()
    script_pubkey2 = buyer2.address.to_script_pub_key()
    script_pubkey3 = buyer3.address.to_script_pub_key()

    utxos_script_pubkeys = [script_pubkey1, script_pubkey2, script_pubkey3]


    # Create the locking script output
    locking_script = Script([
        buyer1.address.to_x_only_hex(),
        buyer2.address.to_x_only_hex(),
        buyer3.address.to_x_only_hex(),
        seller.address.to_x_only_hex(),
        "OP_CHECKMULTISIG"
    ])

    # how should I do this?
    # example not clear? https://github.com/karask/python-bitcoin-utils/blob/master/examples/send_to_p2tr_with_single_script.py#L84
    locking_taproot_address = ....get_taproot_address([[locking_script]])

    fee = 0.00000200
    locked_funds = to_satoshis(buyer1_funds + buyer2_funds + buyer3_funds - fee)
    locking_txout = TxOutput(locked_funds, locking_taproot_address.to_script_pub_key())

    locking_transaction = Transaction([buyer1_txin, buyer2_txin, buyer3_txin], [locking_txout], has_segwit=True)
    
    print("\nRaw transaction:\n" + locking_transaction.serialize())




if __name__ == "__main__":
    main()