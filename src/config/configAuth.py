import repackage
repackage.up()

from hashlib import md5


def crypMD5(senha):

     crypt = md5(senha.encode())
     return crypt.hexdigest()

    