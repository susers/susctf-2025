import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from anyio import Path
import mimetypes

from typing import Optional
import os
import time
import hmac

FLAG = os.environ.get("GZCTF_FLAG") or "susctf{test_flag}"


def get_flag(team_token: Optional[str] = None) -> str:
    return FLAG


record = {}


def check_rate(token: str) -> bool:
    if token in record and time.time() - record[token] < 10:
        return False
    record[token] = time.time()
    return True


def verify_pow(data: str, proof: str, token: str) -> bool:
    print(proof + "|" + data)
    hash = hmac.new(token.encode(), (proof + "|" + data).encode(), "sha512").hexdigest()
    print(hash)
    return hash[:5] == "00000"


mimetypes.init()
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class AnswerModel(BaseModel):
    a1: str
    a2: str


class PowModel(BaseModel):
    answer: AnswerModel
    proof: str
    token: Optional[str] = None


@app.post("/submit")
async def submit(post_data: PowModel):
    if not verify_pow(
        post_data.answer.model_dump_json(), post_data.proof, post_data.token
    ):
        return {"error": "proof不正确"}
    if not check_rate(post_data.token):
        return {"error": "操作过于频繁"}
    user_answer = post_data.answer
    # 答案校验部分
    if len(user_answer.a1) != 10 or len(user_answer.a2) > 25:
        return {"error": "格式不正确"}
    try:
        if user_answer.a1 in [
            "4086274225",
            "4084808671",
            "4089619396",
            "4082608671",
        ] and user_answer.a2 in [
            "Conway Senior High School",
            "Conway High School",
        ]:
            return {"data": get_flag()}
        else:
            return {"error": "回答错误"}
    except:
        return {"error": "内部错误"}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return await Path("index.html").read_text(encoding="utf-8")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
