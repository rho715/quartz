---
title: _. JSON encode decode
tags:
  - json
  - python
---
# encoding vs decoding? 
- 인코딩: 이는 데이터를 다른 형태로 변환하는 과정으로, 주로 데이터 무결성, 보안, 또는 전송 효율성을 보장하기 위해 사용됩니다. 인코딩은 데이터를 쉽게 전송하거나 저장할 수 있는 형태로 변환합니다. 일반적인 예로는 텍스트 데이터를 저장 또는 전송을 위해 바이트로 변환하는 것이 있습니다.

- 디코딩: 이는 인코딩된 데이터를 원래의 형태로 변환하는 과정입니다. 마치 비밀 메시지를 다시 읽을 수 있는 형태로 번역하는 것과 같습니다. 데이터가 전송이나 저장을 위해 인코딩되었고, 우리가 그것을 원래의 형태로 사용할 필요가 있을 때 디코딩이 필요합니다.
## 문제 & 해결 방법
- 가끔 한글을 다루는 코드가 인코딩 된 형태로 반환하여 읽을 수 있게 디코드를 해야하는 경우가 생김 
```python
a = {
"quotes": [
"\uc544\ub2c8\ub2e4.",
"\uc544\ub2c8\ub2e4.",
"\ub17c\ub9ac \ud55c\ub2e4.",
"\ub098\ub294 \uc544\ub2c8\ub2e4 \ubc14\ub784\ub294 \ubc14\ub784 \uc544\ub2c8\ub2e4.",
"\ub108\ub294 \uc544\ub2c8\ub2e4 \uc544\ub2c8\ub2e4\ub97c \ubc14\ub784\ub294 \ubc14\ub784 \uc544\ub2c8\ub2e4."
],
"actors": [
{
"name": "\uc774\ud2b8\ud638",
"character": "\uc601\uc138"
},
{
"name": "\uc774\ub204\uc544",
"character": "\uc774\uc5f0"
},
{
"name": "\ubc15\uc774",
"character": "\uc774\uc7ac"
},
{
"name": "\uc218\uc815",
"character": "\uc57d\uc138"
}
]
}
import json
json_string = json.dumps(a, ensure_ascii=False, indent=2)

# Print the JSON string
print(json_string)
```

## ChatGPT-4 답변 
The text you've provided is encoded using Unicode escape sequences. These sequences are a way to represent non-ASCII characters, especially characters from languages like Korean, in a universally readable format in computing. This type of encoding is often used in data transmission or storage to ensure that special characters are preserved correctly.

Here's a breakdown of what this means in the context of your example:

- **Encoded**: The text is encoded because it uses Unicode escape sequences (like `\uc544\ub2c8\ub2e4`) to represent characters. This is not immediately readable to a human without converting it back to its original form.
    
- **Decoding**: To make this text human-readable (in its original language, which appears to be Korean), it needs to be decoded. Decoding will convert these Unicode escape sequences back into the Korean characters they represent.
    

In summary, the text you've provided is currently in an encoded state. To read it as intended (in Korean), it needs to be decoded.

If you need assistance with decoding this text to see what it says in Korean, I can help with that. Let me know if you'd like me to do so!