from google.adk.tools import FunctionTool
from app.memory.vector_store import guidelines_vector_store
from app.core.logging import get_logger

logger = get_logger(__name__, log_file="logs/app.log")

class GuidelinesTools:
    @staticmethod
    def search_medical_guidelines(query: str) -> str:
        """
        Searches the medical guidelines and document vector store.
        Use this tool whenever the user asks for generic medical facts, preparation instructions for labs, FAQs, or billing code lookup rules.

        Args:
            query: The specific question or topic to search for in the medical guidelines.
            
        Returns:
            A formatted string containing the top relevant search results from the internal medical knowledge base.
        """
        try:
            logger.info(f"Searching medical guidelines for: {query}")
            results = guidelines_vector_store.search(query=query, top_k=3, threshold=0.1) # threshold low for dummy testing
            if not results:
                return "No relevant clinical or general guidelines found for this query."
            
            output = "Found the following relevant guidelines:\n"
            for res in results:
                category = res.get('metadata', {}).get('category', 'unknown')
                output += f"- [{category.upper()}] (Score: {res['score']:.2f}) {res['text']}\n"
            return output
        except Exception as e:
            logger.error(f"Error in vector store search tool: {e}")
            return f"Error retrieving guidelines: {e}"

    def get_tools(self):
        return [
            FunctionTool(self.search_medical_guidelines)
        ]
