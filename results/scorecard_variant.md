# Scorecard: variant_hybrid_rerank

**Generated:** 2026-04-13 14:46
**Config:** variant_hybrid_rerank

## Average Scores

| Metric | Score |
|--------|-------|
| Faithfulness | 4.20/5 |
| Relevance | 3.80/5 |
| Context Recall | 5.00/5 |
| Completeness | 3.80/5 |

## Per-Question Results

| ID | Category | F | R | Rc | C | Answer Preview |
|---|---|---|---|---|---|---|
| q01 | SLA | 5 | 5 | 5 | 5 | SLA xử lý ticket P1 là 15 phút cho phản hồi ban đầu và 4 giờ cho xử lý và khắc p |
| q02 | Refund | 5 | 5 | 5 | 5 | Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm x |
| q03 | Access Control | 5 | 5 | 5 | 5 | Để cấp quyền Level 3, cần có sự phê duyệt của Line Manager, IT Admin và IT Secur |
| q04 | Refund | 5 | 5 | 5 | 5 | Sản phẩm kỹ thuật số không được hoàn tiền. Các sản phẩm thuộc danh mục hàng kỹ t |
| q05 | IT Helpdesk | 5 | 5 | 5 | 5 | Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, bạn có thể liên |
| q06 | SLA | 5 | 5 | 5 | 4 | Escalation trong sự cố P1 diễn ra như sau:  1. Nếu không có phản hồi trong 10 ph |
| q07 | Access Control | 1 | 1 | 5 | 1 | Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này. |
| q08 | HR Policy | 5 | 5 | 5 | 5 | Nhân viên được làm remote tối đa 2 ngày mỗi tuần sau khi đã qua probation period |
| q09 | Insufficient Context | 5 | 1 | None | 1 | Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này. |
| q10 | Refund | 1 | 1 | 5 | 2 | Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này. |

## Detailed Notes

### [q01] SLA xử lý ticket P1 là bao lâu?

**Answer:** SLA xử lý ticket P1 là 15 phút cho phản hồi ban đầu và 4 giờ cho xử lý và khắc phục [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là thời gian phản hồi ban đầu và thời gian xử lý và khắc phục của ticket P1.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin chính xác về SLA xử lý ticket P1.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ tất cả các điểm quan trọng về SLA xử lý ticket P1, không thiếu thông tin nào.

### [q02] Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?

**Answer:** Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm xác nhận đơn hàng [1], [3].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có xuất phát từ context, cụ thể là thời gian yêu cầu hoàn tiền được nêu rõ trong tài liệu.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin chính xác về thời gian khách hàng có thể yêu cầu hoàn tiền.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ thông tin như trong expected answer, không thiếu sót chi tiết nào.

### [q03] Ai phải phê duyệt để cấp quyền Level 3?

**Answer:** Để cấp quyền Level 3, cần có sự phê duyệt của Line Manager, IT Admin và IT Security [2].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là yêu cầu phê duyệt cho Level 3.
- Relevance (5): Câu trả lời đã nêu rõ các bên cần phê duyệt để cấp quyền Level 3, đáp ứng đầy đủ yêu cầu của câu hỏi.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ tất cả các điểm quan trọng như trong expected answer.

### [q04] Sản phẩm kỹ thuật số có được hoàn tiền không?

**Answer:** Sản phẩm kỹ thuật số không được hoàn tiền. Các sản phẩm thuộc danh mục hàng kỹ thuật số như license key và subscription nằm trong danh sách ngoại lệ không được hoàn tiền [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là thông tin về sản phẩm kỹ thuật số không được hoàn tiền và các ví dụ cụ thể như license key và subscription.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, giải thích rõ ràng rằng sản phẩm kỹ thuật số không được hoàn tiền và cung cấp thông tin về các loại sản phẩm cụ thể nằm trong danh sách ngoại lệ.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ thông tin quan trọng và chính xác như trong expected answer.

### [q05] Tài khoản bị khóa sau bao nhiêu lần đăng nhập sai?

**Answer:** Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, bạn có thể liên hệ IT Helpdesk hoặc tự reset qua portal SSO [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là thông tin về việc tài khoản bị khóa sau 5 lần đăng nhập sai và cách mở khóa.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin chính xác về số lần đăng nhập sai và cách mở khóa tài khoản.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ thông tin quan trọng, đúng với expected answer.

### [q06] Escalation trong sự cố P1 diễn ra như thế nào?

**Answer:** Escalation trong sự cố P1 diễn ra như sau:

1. Nếu không có phản hồi trong 10 phút kể từ khi ticket được tạo, ticket sẽ tự động escalate lên Senior Engineer.
2. On-call IT Admin có thể cấp quyền tạm thời (tối đa 24 giờ) để khắc phục sự cố sau khi được Tech Lead phê duyệt bằng lời. 
3. Sau 24 giờ, phải có ticket chính thức hoặc quyền sẽ bị thu hồi tự động. 
4. Tất cả quyền tạm thời phải được ghi log vào hệ thống Security Audit [1][2].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có xuất phát từ tài liệu retrieved, không có chi tiết nào không có trong context.
- Relevance (5): Câu trả lời giải quyết đúng trọng tâm câu hỏi về quy trình escalation trong sự cố P1, cung cấp đầy đủ các bước và điều kiện liên quan.
- Context Recall (5): Recall=100% (1/1)
- Completeness (4): Câu trả lời thiếu một chi tiết nhỏ là không đề cập đến việc ticket P1 tự động escalate lên Senior Engineer, mà chỉ nói về việc không có phản hồi trong 10 phút.

### [q07] Approval Matrix để cấp quyền hệ thống là tài liệu nào?

**Answer:** Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này.

- Faithfulness (1): Câu trả lời không dựa trên thông tin nào từ context, mà chỉ khẳng định rằng không có dữ liệu, điều này không phản ánh nội dung của tài liệu đã retrieve.
- Relevance (1): Câu trả lời không cung cấp thông tin nào liên quan đến câu hỏi về Approval Matrix, do đó không trả lời được câu hỏi.
- Context Recall (5): Recall=100% (1/1)
- Completeness (1): Câu trả lời thiếu phần lớn nội dung cốt lõi, không đề cập đến tên tài liệu cụ thể và thông tin quan trọng về tên mới của tài liệu.

### [q08] Nhân viên được làm remote tối đa mấy ngày mỗi tuần?

**Answer:** Nhân viên được làm remote tối đa 2 ngày mỗi tuần sau khi đã qua probation period, và lịch remote phải được Team Lead phê duyệt qua HR Portal [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là điều kiện làm remote và yêu cầu phê duyệt.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin chính xác về số ngày làm remote và điều kiện cần thiết.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ tất cả thông tin quan trọng từ expected answer, không thiếu sót chi tiết nào.

### [q09] ERR-403-AUTH là lỗi gì và cách xử lý?

**Answer:** Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này.

- Faithfulness (5): Câu trả lời hoàn toàn chính xác vì nó phản ánh đúng tình trạng của thông tin trong context, không có thông tin nào được thêm vào từ kiến thức của mô hình.
- Relevance (1): Câu trả lời không cung cấp thông tin nào về lỗi ERR-403-AUTH và cách xử lý, hoàn toàn không trả lời câu hỏi.
- Context Recall (None): No expected sources (abstain question)
- Completeness (1): Câu trả lời thiếu phần lớn nội dung cốt lõi, không cung cấp thông tin về lỗi ERR-403-AUTH và cách xử lý.

### [q10] Nếu cần hoàn tiền khẩn cấp cho khách hàng VIP, quy trình có khác không?

**Answer:** Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này.

- Faithfulness (1): Câu trả lời không dựa trên bất kỳ thông tin nào trong context, chủ yếu bịa đặt.
- Relevance (1): Câu trả lời không giải quyết câu hỏi về quy trình hoàn tiền khẩn cấp cho khách hàng VIP, mà chỉ nói rằng không có đủ dữ liệu.
- Context Recall (5): Recall=100% (1/1)
- Completeness (2): Câu trả lời thiếu thông tin quan trọng về chính sách hoàn tiền cho khách hàng VIP và quy trình tiêu chuẩn, chỉ nêu rằng không có đủ dữ liệu mà không cung cấp thông tin cần thiết.

