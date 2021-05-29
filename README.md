# 19-Blockchain-with-Python
Homework 19
# Sending transaction with Python:
ac = priv_key_to_account(BTCTEST, coins['btctest'][2]['private])
ad = coins['btctest'][1]['adress']
send_tx(BTCTEST, ac, ad, 0.0001)

# Sending ether with Python:
ac = priv_key_to_account(ETH, coins['eth'][2]['privkey])
ad = coins['eth'][1]['address']
send_tx(eth, ac, ad, 50)
