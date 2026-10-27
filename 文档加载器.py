from langchain_community.document_loaders import TextLoader
loader = TextLoader(file_path="asset/01-langchain-utf-8.txt", encoding="utf-8")
docs = loader.load()
# print("1")
# print(docs)
# print("2")
# print(docs[0])
# print("3")
# print(type(docs[0]))
# print("4")
# print(docs[0].metadata)
# print("5")
# print(docs[0].page_content)

# 2加载CSV文件
from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(file_path="asset/02-load.csv")
docs = loader.load()
# print(docs)


# 3加载JSON
from langchain_community.document_loaders import JSONLoader
from rich import print as rprint
json_loader = JSONLoader(
    file_path="asset/03-load.json", jq_schema=".messages[].content"
)
docs = json_loader.load()
# print(docs)


# 4加载pdf
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(
    # 文件路径
    # file_path = "../asset/load/04-sample.pdf",
    file_path="https://arxiv.org/pdf/alg-geom/9202012",
    # 提取模式
    #  plain 提取文本，默认值
    #  layout 布局感知提取模式，通常会通过插入大量的空格、换行符，来模拟原本档中的多栏、缩进和间距（使用场景：学术论文、多栏报刊杂志、带有左右分栏的合同）
    extraction_mode="plain",
)
docs=loader.load()
#print(docs)

# 5.加载word

# 6.加载Markdown
from langchain_unstructured import UnstructuredLoader
from pprint import pprint
loader = UnstructuredLoader(
    file_path="asset/06-load.md",
    # 加载模式:
    #   single 返回单个Document对象
    #   elements 按标题等元素切分文档
    mode="single",
    # 解析策略：
    #   "fast"（快速模式），它会以最快的速度提取文本，不进行复杂的版面分析
    #   "hi_res" 高分辨率模式
    strategy="fast",
)
docs=loader.load()
print(len(docs))
pprint(docs)
