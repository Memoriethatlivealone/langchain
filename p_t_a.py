from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import dotenv
dotenv.load_dotenv()

@tool
def search_papers(keyword: str) -> str:
    """根据关键词检索论文库中的论文。
    当用户询问特定研究主题、论文名称或论文信息时使用。
    keyword: 要检索的关键词。
    """
    # 模拟检索结果，后续可以替换为 MySQL 或 RAG。
    mock_data = {
        "人脸表情识别": [
            "轻量化 CNN 人脸表情识别研究",
            "基于注意力机制的表情分类方法",
        ],
        "目标检测": [
            "面向实时场景的轻量化目标检测方法",
        ],
    }
    for key, papers in mock_data.items():
        if key in keyword:
            return "\n".join(papers)
    return "未检索到匹配论文。"


@tool
def calculate_metric(
    true_positive: int,
    false_positive: int,
    false_negative: int,
) -> str:
    """根据 TP、FP、FN 计算 Precision 和 Recall。
    TP: 真正例数量。
    FP: 假正例数量。
    FN: 假负例数量。
    """
    if min(true_positive, false_positive, false_negative) < 0:
        return "计算失败：输入数量不能为负数。"
    precision_denominator = true_positive + false_positive
    recall_denominator = true_positive + false_negative
    precision = true_positive / precision_denominator if precision_denominator else 0.0
    recall = true_positive / recall_denominator if recall_denominator else 0.0
    return f"Precision={precision:.4f}, " f"Recall={recall:.4f}"


model = ChatOpenAI(
    model="deepseek-v4.1-flash",
    temperature=0,
)
agent = create_agent(
    model=model,
    tools=[search_papers, calculate_metric],
    system_prompt="""
    你是一个计算机视觉研究助手。
    规则：
    1. 用户查询特定论文时，优先使用 search_papers。
    2. 用户要求计算 Precision 或 Recall 时，使用 calculate_metric。
    3. 解释概念时，可以直接回答。
    4. 不要把模拟检索结果说成真实的完整论文数据库。
    5. 工具没有返回的数据，不要编造。
    6. 最终使用中文回答。
    """,
)
while True:
    question = input("请输入问题（输入 exit 退出）：").strip()
    if question.lower() == "exit":
        break
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print("\nAgent 回答：")
    print(result["messages"][-1].content)
    print()
