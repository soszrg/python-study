# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.backends.openssl import ec

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.exceptions import InvalidSignature

import base64

from openssl_test.pub_key import FOG_ID_PUBLIC_KEY

time1 = time.time()
with open("/Users/sos/zrg/work/v3.1/doc/Fog ID/0/vk.pem", "r") as f:
    vk_pem = f.read()

public_key = serialization.load_pem_public_key(vk_pem, backend=default_backend())

data = str("AAQAAAAAAARanlQDAgEAAwEA")
sign_base = str("MEQCIF+vwoygZIjl8OdE/J3othPhqWLZrh4np4rViZtOkSLlAiBVNrFhgltkJB+aAdIPsUzqXb/rvH1NpNye1qlFbrH7mA==")
# with open("/Users/sos/zrg/work/v3.1/doc/Fog ID/0/fogid.sig", "rb") as f:
#     signature = f.read()
#     sign_base = base64.b64encode(signature)
signature = base64.b64decode(sign_base)

try:
    public_key.verify(
        signature,
        base64.b64decode(data),
        # padding.PKCS1v15(),
        ec.ECDSA(hashes.SHA256())
    )
except InvalidSignature as e:
    print e.message
    print "fail"
else:
    print "success"
    verify_ok = True
