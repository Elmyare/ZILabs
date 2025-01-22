from DigitalSignatureLibrary import DigitalSignatureLibrary

DigitalSignatureLibrary = DigitalSignatureLibrary()
data = b"Hello, World!"
signature = DigitalSignatureLibrary.ElGamalSign(data)
print("ElGamal Signature:", signature)
print("ElGamal Signature Check:", DigitalSignatureLibrary.ElGamalSignCheck(data, signature))

signature = DigitalSignatureLibrary.RSASign(data)
print("RSA Signature:", signature)
print("RSA Signature Check:", DigitalSignatureLibrary.RSASignCheck(data, signature))

signature = DigitalSignatureLibrary.GOSTSign(data)
print("GOST Signature:", signature)
print("GOST Signature Check:", DigitalSignatureLibrary.GOSTSignCheck(data, signature))