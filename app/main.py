from fastapi import FastAPI
from pydantic import BaseModel

from nl2sql_pipeline import generate_query
from sql_executor import execute_sql
from answer_formatter import format_answer
from cache_service import get_cached_result, save_cached_result

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse




app = FastAPI(
    title="NL2SQL Assistant",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory="../static"),
    name="static"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return FileResponse("../static/index.html")


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    # --------------------------------
    # CACHE CHECK
    # --------------------------------

    cached_result = get_cached_result(question)

    if cached_result:

        return {
            "question": question,
            "sql": cached_result["sql"],
            "answer": cached_result["answer"],
            "columns": cached_result["columns"],
            "rows": cached_result["rows"],
            "cache_hit": True,
            "cache_status": "CACHE HIT"
        }

    # --------------------------------
    # NL2SQL PIPELINE
    # --------------------------------

    sql, results = generate_query(question)

    columns, rows = execute_sql(sql)

    answer = format_answer(
        question,
        columns,
        rows
    )

    # --------------------------------
    # SAVE RESULT TO CACHE
    # --------------------------------

    save_cached_result(
        question,
        sql,
        answer,
        columns,
        rows
    )

    return {
        "question": question,
        "sql": sql,
        "answer": answer,
        "columns": columns,
        "rows": [
            list(row)
            for row in rows
        ],
        "cache_hit": False,
        "cache_status": "CACHE MISS"
    }