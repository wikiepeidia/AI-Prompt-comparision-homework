import json
from pathlib import Path
from html import escape
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
rows=json.loads((root/"groq-qwen.json").read_text(encoding="utf8"))
source=rows[0]["messages"][0]["content"].split("\n",1)[1]
notes=[
["Giữ đủ độ nghiêng trục, hướng trục và sự đảo mùa sau sáu tháng. Phần mở đầu và câu dài về tháng Sáu khiến đoạn ghi vở còn dài hơn bài đọc.","Đúng hai câu. Câu đầu nêu độ nghiêng, câu sau so sánh độ dài ngày và góc chiếu ở hai bán cầu. Chi tiết về hướng trục đã bị lược.","Giữ đúng phạm vi bài đọc. Mục “Bằng chứng” chủ yếu giải thích cơ chế; một quan sát cụ thể về tháng Sáu sẽ thuyết phục hơn."],
["Giải thích được hai yếu tố: cùng chùm sáng phủ diện tích nhỏ hơn và ngày dài hơn. Ý về khoảng cách xuất hiện ở cả đầu lẫn cuối.","Đèn pin giúp hình dung vệt sáng trải rộng. Cụm “thẳng đứng” dễ khiến người đọc tưởng mọi nơi ở Bắc bán cầu đều có Mặt Trời ngay trên đỉnh đầu vào mùa hè.","Giữ khoảng cách đèn–giấy và chỉ ra mô hình chưa thể hiện độ dài ngày. Cuối bài lại quy sự luân phiên ngày đêm cho trục nghiêng."],
["Tám câu kèm tám đáp án. Đáp án 6 lặp lại kết luận trong ngữ liệu mà chưa giải thích vì sao hai mùa trái ngược là bằng chứng.","Có đủ ba câu theo thứ tự yêu cầu, đáp án ở cuối. Câu vận dụng vẫn xoay quanh đúng tình huống tháng Sáu đã học.","Có câu dự đoán cho tháng Mười Hai, câu hỏi độ nghiêng và câu chẩn đoán nhầm lẫn. Đề hỏi thời tiết nhưng đáp án chấm độ dài ngày và góc chiếu."]]
findings=[
"Để ghi vở, bản hai câu dễ dùng nhất. Hai câu đủ để nối độ nghiêng trục với sự khác biệt giữa hai bán cầu vào tháng Sáu. Bản nâng cao hợp cho bài tập lập luận hơn, nhưng phần ghi “Bằng chứng” sẽ rõ hơn nếu nêu một quan sát cụ thể, chẳng hạn ngày ở Bắc bán cầu dài hơn vào tháng Sáu.",
"Để trả lời miệng vì sao mùa hè ấm hơn, hai ý trong bản cơ bản đã đủ. Để làm thí nghiệm, bản nâng cao chỉ rõ phải giữ khoảng cách đèn–giấy. Khi giảng lại cần sửa một câu: Trái Đất tự quay tạo nên sự luân phiên ngày đêm; độ nghiêng trục góp phần làm độ dài ngày thay đổi theo mùa. Một thí nghiệm mô tả đúng góc chiếu vẫn có thể đi kèm một lời giải thích sai.",
"Bản nâng cao thích hợp nhất để tự chấm vì mỗi đáp án nêu dấu hiệu cần có. Nên sửa “hiện tượng thời tiết” thành “độ dài ngày và góc chiếu” cho khớp với đáp án."]
def tex(s):
    return s.replace("&",r"\&").replace("%",r"\%").replace("#",r"\#").replace("_",r"\_")
doc=r"""\documentclass[12pt,a4paper]{article}
\usepackage[margin=2.1cm]{geometry}
\usepackage{fontspec,graphicx,tabularx,array,url}
\setmainfont{Times New Roman}
\setlength{\parindent}{0pt}\setlength{\parskip}{7pt}
\begin{document}
{\large SIS VNU}\hfill Pham Ha Linh · MSSV 26090224

\section*{Viết prompt để học về các mùa trên Trái Đất}
Cùng đọc một đoạn về các mùa, học sinh có thể muốn ghi vài dòng vào vở, hiểu vì sao nắng hè làm mặt đất ấm hơn, hoặc tự kiểm tra trước buổi học. Ba việc ấy cần ba kiểu câu trả lời. Chẳng hạn, ghi sẵn con số 23,5° có ích cho một bản tóm tắt, nhưng lại làm lộ đáp án của câu hỏi về độ nghiêng trục Trái Đất.

\subsection*{Đoạn đọc dùng cho cả chín lượt}
\begin{quote}""" +tex(source)+r"""\end{quote} Đối chiếu nội dung thiên văn với NASA và National Weather Service~\cite{nasa,nws}.
\subsection*{Cách thử và đối chiếu}
Chín prompt được gửi riêng cho Qwen3.8-27B qua Groq~\cite{groq}, với tham số nhiệt độ 0,2 và thiết lập suy luận mặc định. Mỗi lượt dùng cùng đoạn đọc, cùng chỉ dẫn trả lời bằng tiếng Việt và không có lịch sử hội thoại. Mỗi prompt được chạy một lần. Có thể đối chiếu các bảng với chín câu trả lời nguyên văn trong tệp dữ liệu đính kèm~\cite{log}.

Với bản tóm tắt, tiêu chí chính là giữ đúng quan hệ giữa các ý và có thể lần lại chi tiết trong đoạn đọc. Với lời giải thích, tiêu chí là học sinh hiểu được cơ chế hoặc tự làm được phép so sánh. Với câu hỏi ôn tập, phép thử đơn giản là che phần đáp án đi và xem còn câu hỏi nào để làm.

\subsection*{Điều có thể áp dụng ngay}
Với bài tóm tắt, có thể yêu cầu trích một câu trong đoạn đọc rồi kiểm tra xem câu ấy có thật ở đó. Với thí nghiệm đèn pin, nên nói rõ phải giữ nguyên khoảng cách nào khi thay đổi góc chiếu. Với đề ôn tập, nên thử che đáp án và làm câu đầu tiên. Các nhận xét dưới đây dựa trên các lượt đã lưu. Vì mỗi lần sửa prompt thường đổi cả vai trò, độ dài và dạng bài, một lượt thử chưa đủ để tách riêng tác dụng của từng thay đổi.
"""
assert len(rows)==9
with sync_playwright() as pw:
    browser=pw.chromium.launch(channel="msedge")
    page=browser.new_page(viewport={"width":1050,"height":340},device_scale_factor=1.5)
    for i in range(3):
        group=rows[i*3:i*3+3]
        doc+=r"\newpage\section*{"+tex(group[0]["task"])+"}\n"
        doc+=r"\small\begin{tabularx}{\linewidth}{@{}p{1.55cm}XX@{}}\hline Mức & Prompt đã gửi & Kết quả quan sát \\ \hline "
        for r,note in zip(group,notes[i]):
            assert r["response"]["choices"][0]["finish_reason"]=="stop"
            doc+=" & ".join(map(tex,[r["level"],r["messages"][1]["content"],note]))+r" \\[4pt] "
        doc+=r"\hline\end{tabularx}\normalsize\subsection*{Chọn phiên bản nào?}"+findings[i]
        sample=group[2]
        reply=sample["response"]
        content=reply["choices"][0]["message"]["content"]
        snippet=next(line for line in content.splitlines() if ["**Bằng chứng:**","cùng một khoảng cách","Một học sinh cho rằng"][i] in line)
        # Capture the actual lookup in the saved response, including the matching line.
        page.set_content('<main style="font:19px Times New Roman;padding:14px"><b>Tra cứu nhật ký Groq · '+escape(sample["task"])+'</b><p><label>Tìm trong phản hồi <input id="query"></label></p><small>'+escape(reply["id"])+'</small><p>'+escape(sample["messages"][1]["content"])+'</p><output></output></main>')
        page.locator("#query").fill(["**Bằng chứng:**","cùng một khoảng cách","Một học sinh cho rằng"][i])
        page.evaluate("""answer => {
            const needle = document.querySelector('input').value;
            document.querySelector('output').textContent = answer.split('\\n').find(line => line.includes(needle));
        }""", content)
        assert page.locator("output").text_content().strip() == snippet.strip()
        fname=f"groq-{i+1}.png"
        page.locator("main").screenshot(path=str(root/"minh-chung"/fname))
        doc+=r"\par\includegraphics[width=\linewidth]{minh-chung/"+fname+r"}\par{\small Hình "+str(i+1)+". Trích nhật ký phản hồi nâng cao, kèm mã yêu cầu để đối chiếu với dữ liệu gốc.}\n"
    browser.close()
(root/"bao-cao.tex").write_text(doc+r"\small\renewcommand{\refname}{Tài liệu tham khảo}\bibliographystyle{unsrt}\bibliography{bibilographic}\end{document}",encoding="utf8")
