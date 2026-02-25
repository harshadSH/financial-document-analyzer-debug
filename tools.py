# ==============================
# Imports
# ==============================
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader


# Financial Document Tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = (
        "Reads and extracts text from a financial PDF document. "
        "Input should be the file path."
    )

    def _run(self, path: str = "data/sample.pdf") -> str:
        try:
            if not os.path.exists(path):
                return f"Error: File not found at path {path}"

            loader = PyPDFLoader(path)
            docs = loader.load()

            full_report = ""

            for data in docs:
                content = data.page_content.strip()

                # Clean formatting
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")

                full_report += content + "\n"

            return full_report if full_report else "No content found in document."

        except Exception as e:
            return f"Error reading document: {str(e)}"


# Investment Tool (Optional)
class InvestmentTool(BaseTool):
    name: str = "Investment Analyzer"
    description: str = "Analyzes financial document text and provides investment insights."

    def _run(self, financial_document_data: str) -> str:
        # Basic cleaning
        processed_data = " ".join(financial_document_data.split())

        return (
            "Basic Investment Insight:\n"
            "- Review revenue trends\n"
            "- Check profit margins\n"
            "- Evaluate debt levels\n"
            "(Advanced logic can be added here)"
        )


# Risk Tool (Optional)
class RiskTool(BaseTool):
    name: str = "Risk Analyzer"
    description: str = "Analyzes financial risks from document data."

    def _run(self, financial_document_data: str) -> str:
        return (
            "Basic Risk Assessment:\n"
            "- Market risk\n"
            "- Financial risk\n"
            "- Operational risk\n"
            "(Advanced logic can be added here)"
        )