import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from time import sleep
from dotenv import load_dotenv

root = Path(__file__).resolve().parent
load_dotenv(root / ".env")
key = os.environ["GROQ_API"]
model = "qwen/qwen3.8-27b"
data = json.loads((root / "thu-nghiem.json").read_text(encoding="utf-8-sig"))
out = root / "groq-qwen.json"
records = json.loads(out.read_text(encoding="utf-8")) if out.exists() else []
for task in data["tasks"]:
    for level, prompt in task["runs"]:
        messages = [{"role":"system","content":"Trả lời bằng tiếng Việt. Ngữ liệu dùng chung:\n" + data["source"]},{"role":"user","content":prompt}]
        if any(r["messages"] == messages and r["model"] == model for r in records):
            continue
        payload = dict(model=model, messages=messages, temperature=0.2, max_tokens=2400)
        req = Request("https://api.groq.com/openai/v1/chat/completions", json.dumps(payload).encode(), {"Authorization":"Bearer "+key,"Content-Type":"application/json","User-Agent":"school-prompt-study/1.0"})
        for attempt in range(4):
            try:
                with urlopen(req,timeout=90) as res:
                    response = json.load(res)
                break
            except HTTPError as err:
                print(err.read().decode(errors="replace").replace(key,"[redacted]")[:1200])
                if err.code != 429 or attempt == 3:
                    raise
                sleep(float(err.headers.get("Retry-After","30")))
        records.append(dict(task=task["title"],level=level,**payload,response=response))
        tmp = out.with_suffix(".tmp")
        tmp.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
        tmp.replace(out)
        print(len(records),response["id"],flush=True)

