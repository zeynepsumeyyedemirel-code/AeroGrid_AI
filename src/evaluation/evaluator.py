import time
import logging


logger = logging.getLogger("AeroGrid_Evaluation")


class RAGEvaluator:

    def __init__(self):
        self.metrics = {}


    def evaluate_retrieval(self, retrieved_docs, expected_keywords):
        """
        Evaluate whether retrieved documents contain expected information.
        """

        start_time = time.time()

        combined_context = " ".join(
            [
                doc.get("content", "")
                for doc in retrieved_docs
            ]
        ).lower()


        matched_keywords = [
            keyword
            for keyword in expected_keywords
            if keyword.lower() in combined_context
        ]


        relevance_score = (
            len(matched_keywords) /
            len(expected_keywords)
            if expected_keywords
            else 0
        )


        self.metrics["context_relevance"] = round(
            relevance_score * 100,
            2
        )

        self.metrics["retrieval_latency"] = round(
            time.time() - start_time,
            3
        )


        return self.metrics



    def evaluate_answer(self, answer: str):
        """
        Basic answer quality checks.
        """

        self.metrics["answer_length"] = len(answer)

        self.metrics["has_source_reference"] = (
            "source" in answer.lower()
            or "[source:" in answer.lower()
        )

        self.metrics["empty_answer"] = (
            len(answer.strip()) == 0
        )


        return self.metrics

