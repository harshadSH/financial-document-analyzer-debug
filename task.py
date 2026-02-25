from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import FinancialDocumentTool


# Verification Task
verification = Task(
    description="""
    Verify whether the uploaded document is a financial document.

    Steps:
    - Read the document using the tool
    - Check for financial keywords (revenue, profit, balance sheet, etc.)
    - Determine validity
    """,

    expected_output="""
    {
        "is_financial_document": true or false,
        "reason": "short explanation"
    }
    """,

    agent=verifier,
    tools=[FinancialDocumentTool()],
    async_execution=False
)


# Financial Analysis Task
analyze_financial_document = Task(
    description="""
    Analyze the financial document.

    Steps:
    - Extract key metrics (revenue, profit, expenses)
    - Summarize financial performance
    - Identify trends

    User Query: {query}
    """,

    expected_output="""
    {
        "summary": "",
        "key_metrics": {
            "revenue": "",
            "profit": "",
            "expenses": ""
        },
        "insights": []
    }
    """,

    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
    async_execution=False
)


# Investment Analysis Task
investment_analysis = Task(
    description="""
    Based on the financial analysis:
    - Suggest realistic investment strategies
    - Provide justification based on data
    - Avoid speculation
    """,

    expected_output="""
    {
        "recommendations": [],
        "justification": ""
    }
    """,

    agent=investment_advisor,
    tools=[FinancialDocumentTool()],
    async_execution=False
)


# Risk Assessment Task
risk_assessment = Task(
    description="""
    Identify risks from the financial document:

    - Financial risks
    - Market risks
    - Operational risks
    """,

    expected_output="""
    {
        "risks": [],
        "severity": ""
    }
    """,

    agent=risk_assessor,
    tools=[FinancialDocumentTool()],
    async_execution=False
)