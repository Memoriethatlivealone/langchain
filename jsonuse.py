import json

d1 = {
    "name": "langchainapi.py",
    "url": "https://example.com/langchainapi.py",
    "study": "尚硅谷Python学习",
}
s = json.dumps(d1, ensure_ascii=False)  # json对象
# print(s)
d2 = [
    {
        "name": "langchainapi.py",
        "url": "https://example.com/langchainapi.py",
        "study": "黑马程序员Python学习",
    },
    {
        "name": "langchainapi.py",
        "url": "https://example.com/langchainapi.py",
        "study": "尚硅谷Python学习",
    },
    {
        "name": "langchainapi.py",
        "url": "https://example.com/langchainapi.py",
        "study": "李冬冬Python学习",
    }
]
json_str = json.dumps(d2, ensure_ascii=False)  # json数组
print(json_str)