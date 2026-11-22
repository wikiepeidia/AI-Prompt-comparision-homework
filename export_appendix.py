"""Export saved Groq answers."""
import json
from html import escape
from pathlib import Path



from playwright.sync_api import sync_playwright


def write_appendix(root, rows):
    sections = []
    for index, row in enumerate(rows, 1):
        response = row["response"]
        answer = response["choices"][0]["message"]["content"]
        sections.append(
            f'<section><small>Pham Ha Linh · 26090224 · SIS VNU</small>'
            f'<h2>Lượt {index} · {escape(row["task"])} · {escape(row["level"])}</h2>'
            f'<small>{escape(response["id"])} · {escape(response["model"])}</small>'
            f'<h3>Prompt</h3><p>{escape(row["messages"][1]["content"])}</p>'
            f'<h3>Phản hồi nguyên văn</h3><pre>{escape(answer)}</pre></section>'
        )
    css = """
    @page {size:A4;margin:17mm} body {font:12pt/1.32 'Times New Roman';color:#172629}
    pre {font:inherit;white-space:pre-wrap;overflow-wrap:anywhere}
    section {break-before:page} h3 {break-after:avoid} small {color:#365155}
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        page = browser.new_page()
        page.set_content(f'<meta charset=utf-8><style>{css}</style><section><h1>Phụ lục · Đối chiếu với GPT-OSS-120B</h1><p>Chín lượt này dùng cùng prompt và nhiệt độ 0,2 như Qwen trong báo cáo chính. GPT-OSS dùng mức suy luận thấp, Qwen dùng mặc định. Mỗi prompt chỉ được chạy một lần trên mỗi mô hình.</p><p>Với bản tóm tắt nâng cao, GPT-OSS đưa thêm quan trắc ở Melbourne và Buenos Aires, còn Qwen giữ đúng phạm vi bài đọc. Với đề ôn nâng cao, GPT-OSS hiểu “câu nhớ” thành mẹo ghi nhớ; Qwen đặt một câu hỏi để học sinh tự trả lời.</p><p>Chỉ dẫn chung</p><pre>{escape(rows[0]["messages"][0]["content"])}</pre><p>Mỗi lượt bên dưới giữ nguyên văn bản và ký hiệu Markdown do mô hình trả về.</p></section>' + "".join(sections))
        assert page.locator("section pre").all_text_contents()[1:] == [
            r["response"]["choices"][0]["message"]["content"].replace("\r\n", "\n") for r in rows
        ]
        page.pdf(path=str(root/"phu-luc.pdf"),prefer_css_page_size=True)
        browser.close()


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    records = json.loads((root/"groq-results.json").read_text(encoding="utf8"))
    assert len(records) == 9 and all(r["model"] == "openai/gpt-oss-120b" for r in records)
    write_appendix(root, records)
