import os

from dotenv import load_dotenv

from deepeval import evaluate
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import (
    GEval,
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
)

from retrieval import retrieve_documents
from llm_service import generate_sql
from sql_executor import execute_sql
from answer_formatter import format_answer


load_dotenv("../.env")


def run_nl2sql(question: str):

    # -----------------------------
    # 1. Retrieve relevant context
    # -----------------------------

    documents = retrieve_documents(question)

    retrieval_context = [
        content
        for document_id, source, content, distance in documents
    ]

    context = "\n\n".join(retrieval_context)

    # -----------------------------
    # 2. Generate SQL
    # -----------------------------

    sql = generate_sql(
        question,
        context
    )

    # -----------------------------
    # 3. Execute SQL
    # -----------------------------

    columns, rows = execute_sql(sql)

    # -----------------------------
    # 4. Format final answer
    # -----------------------------

    answer = format_answer(
        question,
        columns,
        rows
    )

    return answer, retrieval_context, sql


# ============================================================
# TEST CASES
# ============================================================

test_questions = [
    {
        "question": "Which region generated the highest sales?",
        "expected": (
            "Southeast has the highest value with "
            "6,898,582,484.18."
        )
    },

    {
        "question": "Which region has the most customers?",
        "expected": (
            "Southeast has the highest value with 10,233.00."
        )
    },

    {
        "question": "Which product generated the highest sales?",
        "expected": (
            "Tablets Product 6396 has the highest value with "
            "10,530,209.21."
        )
    },
]


test_cases = []


# ============================================================
# RUN APPLICATION
# ============================================================

for item in test_questions:

    question = item["question"]
    expected_output = item["expected"]

    print("\n" + "=" * 70)
    print("QUESTION")
    print(question)

    try:

        answer, retrieval_context, sql = run_nl2sql(
            question
        )

        print("\nGENERATED SQL")
        print(sql)

        print("\nACTUAL ANSWER")
        print(answer)

        test_case = LLMTestCase(
            input=question,
            actual_output=answer,
            expected_output=expected_output,
            retrieval_context=retrieval_context,
        )

        test_cases.append(test_case)

    except Exception as error:

        print("\nERROR")
        print(error)


# ============================================================
# DEEPEVAL METRICS
# ============================================================

correctness_metric = GEval(
    name="NL2SQL Answer Correctness",
    criteria=(
        "Determine whether the actual answer correctly answers "
        "the user's question according to the expected answer. "
        "Penalize incorrect entities, incorrect calculations, "
        "and unsupported conclusions."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ],
    threshold=0.7,
    model="gpt-4.1-mini",

)


answer_relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,
    model="gpt-4.1-mini",
    include_reason=True,
)


context_relevancy_metric = ContextualRelevancyMetric(
    threshold=0.7,
    model="gpt-4.1-mini",
    include_reason=True,
)


# ============================================================
# RUN EVALUATION
# ============================================================

print("\n")
print("=" * 70)
print("DEEPEVAL EVALUATION")
print("=" * 70)

if not test_cases:

    print("No test cases were created.")

else:

    results = evaluate(
        test_cases=test_cases,
        metrics=[
            correctness_metric,
            answer_relevancy_metric,
            context_relevancy_metric,
        ],
    )

    print("\n")
    print("=" * 70)
    print("DEEPEVAL EVALUATION COMPLETED")
    print("=" * 70)
