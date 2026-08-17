from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from retrieval import retrieve_documents
from llm_service import generate_sql
from sql_executor import validate_sql, execute_sql
from answer_formatter import format_answer


class NL2SQLState(TypedDict, total=False):
    question: str
    context: str
    sql: str
    columns: list
    rows: list
    answer: str


def retrieve_node(state: NL2SQLState):

    question = state["question"]

    documents = retrieve_documents(question)

    context_parts = []

    for document_id, source, content, distance in documents:

        context_parts.append(
            f"Source: {source}\n"
            f"Content:\n{content}\n"
            f"Similarity distance: {distance:.6f}"
        )

    context = "\n\n" + ("\n\n" + "=" * 60 + "\n\n").join(
        context_parts
    )

    return {
        "context": context
    }


def generate_sql_node(state: NL2SQLState):

    sql = generate_sql(
        state["question"],
        state["context"]
    )

    return {
        "sql": sql
    }


def validate_sql_node(state: NL2SQLState):

    validate_sql(state["sql"])

    return {}


def execute_sql_node(state: NL2SQLState):

    columns, rows = execute_sql(
        state["sql"]
    )

    return {
        "columns": columns,
        "rows": rows
    }


def format_answer_node(state: NL2SQLState):

    answer = format_answer(
        state["question"],
        state["columns"],
        state["rows"]
    )

    return {
        "answer": answer
    }


# --------------------------------------------------
# BUILD LANGGRAPH WORKFLOW
# --------------------------------------------------

workflow = StateGraph(NL2SQLState)

workflow.add_node(
    "retrieve",
    retrieve_node
)

workflow.add_node(
    "generate_sql",
    generate_sql_node
)

workflow.add_node(
    "validate_sql",
    validate_sql_node
)

workflow.add_node(
    "execute_sql",
    execute_sql_node
)

workflow.add_node(
    "format_answer",
    format_answer_node
)


# Workflow edges

workflow.add_edge(
    START,
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "generate_sql"
)

workflow.add_edge(
    "generate_sql",
    "validate_sql"
)

workflow.add_edge(
    "validate_sql",
    "execute_sql"
)

workflow.add_edge(
    "execute_sql",
    "format_answer"
)

workflow.add_edge(
    "format_answer",
    END
)


# Compile graph

nl2sql_graph = workflow.compile()


def run_agentic_pipeline(question: str):

    result = nl2sql_graph.invoke(
        {
            "question": question
        }
    )

    return result


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    question = "Which region generated the highest sales?"

    print("\nLANGGRAPH NL2SQL PIPELINE")
    print("=" * 60)

    result = run_agentic_pipeline(question)

    print("\nQUESTION")
    print(result["question"])

    print("\nGENERATED SQL")
    print(result["sql"])

    print("\nRESULT")
    print(result["columns"])
    print(result["rows"])

    print("\nFINAL ANSWER")
    print(result["answer"])

    print("\nLANGGRAPH EXECUTION COMPLETED")