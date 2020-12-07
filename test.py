import sys

from crypto.elgamal import decrypt, encrypt, generate_keys

if __name__ == '__main__':
    assert sys.version_info >= (3, 4)
    priv, pub = generate_keys(512)
    MESSAGE = 'My name is Ryan. Here is some french text:  Maître Corbeau, sur un arbre perché.\
        Now some Chinese: 鋈 晛桼桾 枲柊氠 藶藽 歾炂盵 犈犆犅 壾, 軹軦軵 寁崏庲 摮 蟼襛 蝩覤 蜭蜸覟'
    CIPHER = encrypt(pub, MESSAGE)
    DECRYPTED = decrypt(priv, CIPHER)

    comps = ('p', 'g',  'x')
    OUT = '\n'.join(["{} = {}".format(comp, getattr(priv, comp))
                     for comp in comps])
    print(f'Private Key:\n{OUT}\n')

    comps = ('p', 'g',  'h')
    OUT = '\n'.join(['{} = {}'.format(comp, getattr(pub, comp))
                     for comp in comps])
    print(f'Public Key:\n{OUT}\n')

    print(f'message == decrypted: {MESSAGE == DECRYPTED}')
