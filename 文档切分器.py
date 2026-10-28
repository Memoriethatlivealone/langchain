#1、CharacterTextSplitter：Split by character
#1字符串文本的分割
from langchain_text_splitters import CharacterTextSplitter
text = """
Langchain是一个用于开发由语言模型驱动的应用程序的框架的。它提供了一套工具和抽象,让开发者能够更容易地构建复杂地应用程序。
"""
# 定义字符分割器
splitter = CharacterTextSplitter(
    chunk_size = 20,   # 每块大小，默认值为4000
    chunk_overlap = 5, # 块与块之间地重复字符数
    # length_function = len,
    separator = "" # 设置为空字符串时，表示禁用分隔符优先
)
# 分割文本
texts = splitter.split_text(text)
# for i, chunk in enumerate(texts):
#     print(f"块{i + 1}:长度:{len(chunk)}")
#     print(chunk)
#     print("-" * 50)

#2# 指定分隔符
# 1.导入相关依赖
from langchain_text_splitters import CharacterTextSplitter
# 2.定义要分割的文本
text = "这是一个示例文本啊:我们将使用CharacterTextSplitter将其分割成小块:分割基于字符数。"
# text = """
# LangChain 是一个用于开发由语言模型。驱动的应用程序的框架的。它提供了一套工具和抽象。使开发者能够更容易地构建复杂的应用程序。
# """
# 3.定义分割器实例
text_splitter = CharacterTextSplitter(
    chunk_size=30,   # 每个块的最大字符数
    chunk_overlap=5, # 块之间的重叠字符数
    separator=":",  # 按标点符号分割优先（注意）
)
# 4.开始分割
chunks = text_splitter.split_text(text)
# 5.打印效果
# for  i,chunk in enumerate(chunks):
#     print(f"块 {i + 1}:长度：{len(chunk)}")
#     print(chunk)
#     print("-"*50)

#2RecursiveCharacterTextSplitter：最常用
 # 1.导入相关依赖
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 2.定义RecursiveCharacterTextSplitter分割器对象
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=0,
    add_start_index=True,
)

 # 3.定义拆分的内容
text="LangChain框架特性\n\n多模型集成(GPT/Claude)\n记忆管理功能\n链式调用设计。文档分析场景示例:需要处理PDF/Word等格式。"

 # 4.拆分器分割
paragraphs = text_splitter.split_text(text)
# for i,chunk in enumerate(paragraphs):
#     print(f"块{i + 1},长度：{len(chunk)}")
#     print(chunk)
#     print('-' * 50)


# 1.导入相关依赖
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 2.定义RecursiveCharacterTextSplitter分割器对象
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=0,
    add_start_index=True,
)

# 3.定义分割的内容
# text="LangChain框架特性\n\n多模型集成(GPT/Claude)\n记忆管理功能\n链式调用设计。文档分析场景示例：需要处理PDF/Word等格式。"

list=["LangChain框架特性\n\n多模型集成(GPT/Claude)\n记忆管理功能\n链式调用设计。文档分析场景示例：需要处理PDF/Word等格式。"]

# 4.分割器分割
# create_documents()：形参是字符串列表，返回值是Document的列表
paragraphs = text_splitter.create_documents(list)


# for para in paragraphs:
#     print(para)
#     print('-------')

# 1.导入相关依赖
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 2.打开.txt文件
with open("asset/01-langchain-utf-8.txt", encoding="utf-8") as f:
    state_of_the_union = f.read()  #返回的是字符串

# 3.定义RecursiveCharacterTextSplitter（递归字符分割器）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=20,
    #chunk_overlap=0,
    length_function=len
)

# 4.分割文本
texts = text_splitter.create_documents([state_of_the_union])

# 5.打印分割文本
# for text in texts:
#     print(f"🔥{text.page_content}")

#3、TokenTextSplitter/CharacterTextSplitter：Split by tokens
# 1.导入相关依赖
from langchain_text_splitters import TokenTextSplitter

# 2.初始化 TokenTextSplitter
text_splitter = TokenTextSplitter(
    chunk_size=33,  # 最大 token 数为 33
    chunk_overlap=0, # 重叠 token 数为 0
    # model_name="gpt-4", # 选择 GPT-4 模型的编码器
    encoding_name="cl100k_base",  # 使用 OpenAI 的编码器,将文本转换为 token 序列
)
# 3.定义文本
text = "人工智能是一个强大的开发框架。它支持多种语言模型和工具链。人工智能是指通过计算机程序模拟人类智能的一门科学。自20世纪50年代诞生以来，人工智能经历了多次起伏。"

# 4.开始切割
texts = text_splitter.split_text(text)

# 打印分割结果
print(f"原始文本被分割成了 {len(texts)} 个块:")
for i, chunk in enumerate(texts):
    print(f"块 {i+1}: 长度：{len(chunk)} 内容：{chunk}")
    print("-" * 50)
#文档切割