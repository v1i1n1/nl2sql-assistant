from fastapi import FastAPI
from pydantic import BaseModel

from nl2sql_pipeline import generate_query
from sql_executor import execute_sql
from answer_formatter import format_answer

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

    question = request.question

    sql, results = generate_query(question)

    columns, rows = execute_sql(sql)

    answer = format_answer(
        question,
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
        ]
    }