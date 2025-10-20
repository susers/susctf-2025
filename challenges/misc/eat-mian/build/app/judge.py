import subprocess
from typing import Tuple
import re


FLAG = open("/flag").read()


def compile(code: str) -> Tuple[bool, str]:
    with (
        open("temp/temp.c", "wb") as f,
        open("static/template.h", "rb") as template_file,
    ):
        template = template_file.read()
        code_bytes = code.replace("\r", "").encode("utf-8", errors="ignore")
        data = (
            template.replace(b"{{ code }}", code_bytes)
            .replace(b"int", b"eat")
            .replace(b"main", b"mian")
        )
        f.write(data)
        f.close()
    try:
        result = subprocess.check_output(
            [*"/usr/local/bin/qemu-x86_64 /usr/bin/gcc -o temp/code".split(" "), f.name],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        return False, e.output.decode("utf-8", errors="ignore")
    return True, result.decode("utf-8", errors="ignore")


def run() -> Tuple[bool, str, str]:
    try:
        result = subprocess.check_output(["/usr/local/bin/qemu-x86_64", "temp/code"])
        ret = result.decode("utf-8", errors="ignore")
        if not re.match(r"I eat \d+ cups of mian! wwwww", ret):
            ret = "不许看"
            return False, "输出错误", ret
        return True, f"答案正确！ {FLAG}", ret

    except subprocess.CalledProcessError as e:
        return False, "运行失败", e.output.decode("utf-8", errors="ignore")
