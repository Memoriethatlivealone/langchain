# 1.模型的初始化
import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

# 读取.env配置文件中的信息；override = True 相关的环境变量要以.env中环境变量优先
load_dotenv(override = True)

model = ChatDeepSeek(
    model="deepseek-v4.1-flash",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    api_base=os.environ["DEEPSEEK_BASE_URL"],  # 缺了立刻 KeyError，而不是静默回落
    temperature=0,
    extra_body={"thinking": {"type": "disabled"}},
)


# 2.定义相关的工具 -体现agent的功能
# ==================== 工具定义 ====================
from langchain_core.tools import tool
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from string import Template

WEEKDAYS = "一二三四五六日"

# 工具数据目录：数据与代码分离，改数据不用改代码
DATA_DIR = Path(__file__).resolve().parent / "data"


def load_data(name: str) -> dict:
    """读取 data/<name>.json 里的工具数据（不缓存，改完文件立即生效）。"""
    path = DATA_DIR / f"{name}.json"
    if not path.is_file():
        raise FileNotFoundError(f"找不到工具数据文件：{path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"工具数据文件不是合法 JSON：{path}（{exc}）") from exc

def build_tool_list(tools) -> str:
    """从真实的 @tool 对象派生清单，杜绝和代码漂移。"""
    return "\n".join(
        f"- `{t.name}`：{t.description.strip().splitlines()[0]}" for t in tools
    )

def render_prompt(template_text: str, **variables: str) -> str:
    """渲染提示词模板；变量缺失时报错，而不是留下未替换的 $xxx。"""
    tpl = Template(template_text)
    missing = [name for name in tpl.get_identifiers() if name not in variables]
    if missing:
        raise ValueError(f"提示词模板缺少变量：{missing}")
    return tpl.substitute(**variables)


@tool
def get_weather(city: str) -> str:
    """获取指定城市的实时天气信息

    支持中国主要城市的天气查询

    Args:
        city: 城市名称，如"北京"、"上海"、"深圳"等

    Returns:
        包含温度、天气状况、空气质量的详细信息

    Examples:
        get_weather("北京") 返回 "多云，15-22℃，空气质量良"
    """
    # 数据源：data/weather_cities.json（将来换真实天气 API，只需改这一段）
    cities = load_data("weather_cities")["cities"]

    entry = cities.get(city)
    if entry is None:
        supported = "、".join(cities)
        return f"抱歉，暂不支持查询{city}的天气信息。当前支持：{supported}"

    return (
        f"{city}:{entry['condition']}，{entry['temp_low']}-{entry['temp_high']}℃"
        f"，空气质量{entry['air']}，湿度 {entry['humidity']}%"
    )


@tool
def calculator(expression: str) -> str:
    """执行数学计算

    支持基本运算符（+、-、*、/、**）和常用数学函数

    Args:
        expression: 数学表达式，可以包含：
            - 基本运算：2 + 3, 10 * 5, 100 / 4
            - 幂运算：2 ** 10
            - 函数：sqrt(16), abs(-5), pow(2, 3)

    Returns:
        计算结果或错误信息

    Examples:
        calculator("2 + 3 * 4") 返回 "14"
        calculator("sqrt(16)") 返回 "4.0"
    """
    try:
        # 安全的数学运算环境
        safe_functions = {
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs,
            "round": round,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expression, {"__builtins__": {}}, safe_functions)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算出错：{str(e)}\n提示：请检查表达式格式，支持的函数有 sqrt, abs, pow, sin, cos, tan, log"


@tool
def get_time_info(query_type: str = "current") -> str:
    """获取时间相关信息

    Args:
        query_type: 查询类型
            - "current": 当前时间
            - "date": 今天日期
            - "tomorrow": 明天日期
            - "yesterday": 昨天日期
            - "weekday": 星期几

    Returns:
        时间信息字符串

    Examples:
        get_time_info("current") 返回 "2025年1月25日 14:30:25"
        get_time_info("weekday") 返回 "星期六"
    """
    now = datetime.now()

    if query_type == "current":
        return now.strftime("当前时间：%Y年%m月%d日 %H:%M:%S")
    elif query_type == "date":
        return now.strftime("今天是：%Y年%m月%d日")
    elif query_type == "tomorrow":
        tomorrow = now + timedelta(days=1)
        return tomorrow.strftime("明天是：%Y年%m月%d日")
    elif query_type == "yesterday":
        yesterday = now - timedelta(days=1)
        return yesterday.strftime("昨天是：%Y年%m月%d日")
    elif query_type == "weekday":
        weekdays = [
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六",
            "星期日",
        ]
        return f"今天是{weekdays[now.weekday()]}"
    else:
        return f"不支持的查询类型：{query_type}。支持：current, date, tomorrow, yesterday, weekday"


@tool
def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
    """货币转换工具
    支持主要货币之间的实时汇率转换

    Args:
        amount: 金额数值
        from_curr: 源货币代码（CNY/USD/EUR/GBP/JPY/HKD）
        to_curr: 目标货币代码（CNY/USD/EUR/GBP/JPY/HKD）

    Returns:
        转换结果

    Examples:
        convert_currency(100, "CNY", "USD") 返回 "100 CNY = 14.00 USD"
    """
    # 数据源：data/currencies.json
    data = load_data("currencies")
    exchange_rates = data["rates"]
    currency_names = data["names"]

    from_curr = from_curr.upper()
    to_curr = to_curr.upper()
    supported = ", ".join(exchange_rates)

    if from_curr not in exchange_rates:
        return f"不支持的源货币：{from_curr}。支持的货币：{supported}"
    if to_curr not in exchange_rates:
        return f"不支持的目标货币：{to_curr}。支持的货币：{supported}"

    # 转换逻辑：先转为 CNY，再转为目标货币
    cny_amount = amount / exchange_rates[from_curr]
    result_amount = cny_amount * exchange_rates[to_curr]

    from_name = currency_names[from_curr]
    to_name = currency_names[to_curr]

    return f"{amount} {from_name}（{from_curr}）= {result_amount:.2f} {to_name}（{to_curr}）"


@tool
def search_info(keyword: str, category: str = "all") -> str:
    """搜索各类信息

    Args:
        keyword: 搜索关键词
        category: 搜索分类
            - "product": 搜索产品
            - "news": 搜索新闻
            - "all": 搜索所有

    Returns:
        搜索结果
    """
    # 数据源：data/catalog.json
    data = load_data("catalog")
    products = data["products"]
    news = data["news"]

    results = []

    if category in ["product", "all"]:
        for key, value in products.items():
            if keyword in key:
                results.append(f"【产品】{key}：{value}")

    if category in ["news", "all"]:
        for key, value in news.items():
            if keyword in key or keyword in value:
                results.append(f"【新闻】{key} 相关：{value}")

    if results:
        return "\n".join(results)
    else:
        return f"未找到关于 '{keyword}' 的{category}信息"


# 3.Agent创建（实例化）
from langchain.agents import create_agent
import re

# 系统提示词文件：与本脚本放在同一目录
PROMPT_FILE = Path(__file__).resolve().parent / "assistant_system_prompt.md"

# 多个 agent 共享的规则片段目录
SHARED_DIR = Path(__file__).resolve().parent / "prompts" / "_shared"

# 模板变量名 -> prompts/_shared/<片段名>.md；新增共享段落时在这里加一行即可
SHARED_FRAGMENTS = {
    "workflow": "tool_workflow",
    "style": "style",
    "uncertainty": "uncertainty",
    "safety": "safety",
}


def load_fragment(name: str) -> str:
    """读取共享规则片段（prompts/_shared/<name>.md）。"""
    path = SHARED_DIR / f"{name}.md"
    if not path.is_file():
        raise FileNotFoundError(f"找不到共享提示词片段：{path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"共享提示词片段内容为空：{path}")
    return text


def assistant_system_prompt(tools, path: Path | str = PROMPT_FILE) -> str:
    """读取外部 Markdown 提示词模板，填充运行时变量后返回。

    文件开头 --- 之间的 YAML 元信息会被去掉；正文里的 $变量 由 render_prompt
    填充，其中 workflow/style/uncertainty/safety 来自 prompts/_shared 共享片段，
    缺变量会立刻报错。create_agent 的 system_prompt 只接受 str 或 SystemMessage，
    所以这里返回 str。

    Args:
        tools: 工具列表，用于从 @tool 定义派生提示词里的工具清单。
        path: 提示词文件路径，默认取脚本同目录下的 assistant_system_prompt.md。

    Returns:
        去掉 frontmatter 并完成变量替换的提示词正文。
    """
    prompt_path = Path(path)
    if not prompt_path.is_file():
        raise FileNotFoundError(f"找不到系统提示词文件：{prompt_path}")

    text = prompt_path.read_text(encoding="utf-8")

    # 去掉文件开头的 YAML frontmatter
    frontmatter = re.match(
        r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", text, re.DOTALL
    )
    if frontmatter:
        text = text[frontmatter.end() :]

    body = text.strip()
    if not body:
        raise ValueError(f"系统提示词文件没有正文内容：{prompt_path}")

    now = datetime.now()
    fragments = {name: load_fragment(f) for name, f in SHARED_FRAGMENTS.items()}
    return render_prompt(
        body,
        tool_list=build_tool_list(tools),
        today=now.strftime("%Y-%m-%d"),
        weekday="星期" + WEEKDAYS[now.weekday()],
        env=os.getenv("APP_ENV", "development"),
        **fragments,
    )


class SmartAssistant:
    """多功能智能助手"""

    def __init__(self):
        # 初始化模型
        self.model = model
        # 工具列表
        self.tools = [
            # 工具
            get_weather,
            calculator,
            get_time_info,
            convert_currency,
            search_info,
        ]
        system_prompt = assistant_system_prompt(self.tools)
        # 系统提示词
        # ✅ 创建 agent
        self.agent = create_agent(
            model=self.model, tools=self.tools, system_prompt=system_prompt
        )

        # 对话历史
        self.messages = []

    def chat(self, user_input: str) -> str:
        """对话接口"""
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})

        # 调用 agent
        result = self.agent.invoke({"messages": self.messages})

        # 更新消息历史
        self.messages = result["messages"]

        # 返回最后一条 AI 消息
        for msg in reversed(self.messages):
            if msg.type == "ai" and msg.content:
                return msg.content

        return "抱歉，我无法处理这个请求。"

    def reset(self):
        """重置对话历史"""
        self.messages = []


# 4.主程序--执行测试
# ==================== 主程序 ====================


def main():
    assistant = SmartAssistant()
    print("=" * 40)
    print("🤖 多功能智能助手（LangChain 1.2）")
    print("=" * 40)
    print("\n我可以帮你：")
    print("  🌤️  查询天气")
    print("  🔢 数学计算")
    print("  ⏰ 时间查询")
    print("  💱 货币转换")
    print("  🔍 信息搜索")
    print("\n输入 'quit' 退出，输入 'reset' 重置对话\n")
    # demos = [
    #     "北京今天天气怎么样？",
    #     "帮我算一下 (25 + 17) * 3",
    #     "现在几点了？",
    #     "100 美元等于多少人民币？"
    # ]
    #
    # for demo in demos:
    #     print(f"👤 {demo}")
    #     response = assistant.chat(demo)
    #     print(f"🤖 {response}\n")
    #
    # # 重置对话
    # assistant.reset()
    # 交互模式
    print("=" * 40)
    print("💬 进入交互模式")
    print("=" * 40)

    while True:
        user_input = input("\n👤 你: ")
        if user_input.lower() == "quit":
            print("再见！👋")
            break
        if user_input.lower() == "reset":
            assistant.reset()
            print("✅ 对话已重置")
            continue

        if not user_input.strip():
            continue
        # 调用助手
        response = assistant.chat(user_input)
        print(f"🤖 助手: {response}")


if __name__ == "__main__":
    main()
#mac#mac