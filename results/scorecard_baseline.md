# Scorecard: baseline_dense

**Generated:** 2026-04-13 14:44
**Config:** baseline_dense

## Average Scores

| Metric | Score |
|--------|-------|
| Faithfulness | 3.80/5 |
| Relevance | 4.10/5 |
| Context Recall | 5.00/5 |
| Completeness | 4.10/5 |

## Per-Question Results

| ID | Category | F | R | Rc | C | Answer Preview |
|---|---|---|---|---|---|---|
| q01 | SLA | 5 | 5 | 5 | 4 | SLA xử lý ticket P1 là 4 giờ cho việc xử lý và khắc phục sau phản hồi ban đầu tr |
| q02 | Refund | 5 | 5 | 5 | 5 | Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm x |
| q03 | Access Control | 5 | 5 | 5 | 5 | Để cấp quyền Level 3, cần có sự phê duyệt của Line Manager, IT Admin và IT Secur |
| q04 | Refund | 5 | 5 | 5 | 5 | Sản phẩm kỹ thuật số không được hoàn tiền, bao gồm các sản phẩm như license key  |
| q05 | IT Helpdesk | 5 | 5 | 5 | 5 | Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, bạn có thể liên |
| q06 | SLA | 5 | 4 | 5 | 5 | Escalation trong sự cố P1 diễn ra tự động lên Senior Engineer nếu không có phản  |
| q07 | Access Control | 1 | 5 | 5 | 4 | Tài liệu liên quan đến Approval Matrix để cấp quyền hệ thống là tài liệu "it/acc |
| q08 | HR Policy | 5 | 5 | 5 | 5 | Nhân viên được làm remote tối đa 2 ngày mỗi tuần sau khi hoàn thành probation pe |
| q09 | Insufficient Context | 1 | 1 | None | 1 | Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này. |
| q10 | Refund | 1 | 1 | 5 | 2 | Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này. |

## Detailed Notes

### [q01] SLA xử lý ticket P1 là bao lâu?

**Answer:** SLA xử lý ticket P1 là 4 giờ cho việc xử lý và khắc phục sau phản hồi ban đầu trong 15 phút kể từ khi ticket được tạo [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là SLA xử lý ticket P1 được nêu rõ là 4 giờ cho việc xử lý và khắc phục sau phản hồi ban đầu trong 15 phút.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin chính xác về SLA xử lý ticket P1.
- Context Recall (5): Recall=100% (1/1)
- Completeness (4): Câu trả lời thiếu thông tin về SLA phản hồi ban đầu 15 phút, chỉ đề cập đến thời gian xử lý 4 giờ.

### [q02] Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?

**Answer:** Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm xác nhận đơn hàng, nếu đáp ứng đủ các điều kiện quy định [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là thời gian yêu cầu hoàn tiền và điều kiện cần thiết.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin rõ ràng về thời gian khách hàng có thể yêu cầu hoàn tiền.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ thông tin như trong expected answer, không thiếu sót chi tiết nào.

### [q03] Ai phải phê duyệt để cấp quyền Level 3?

**Answer:** Để cấp quyền Level 3, cần có sự phê duyệt của Line Manager, IT Admin và IT Security [2].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là yêu cầu phê duyệt cho Level 3.
- Relevance (5): Câu trả lời đã nêu rõ các bên cần phê duyệt để cấp quyền Level 3, đáp ứng đúng trọng tâm câu hỏi.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ tất cả các điểm quan trọng như trong expected answer.

### [q04] Sản phẩm kỹ thuật số có được hoàn tiền không?

**Answer:** Sản phẩm kỹ thuật số không được hoàn tiền, bao gồm các sản phẩm như license key và subscription, theo quy định ngoại lệ trong chính sách hoàn tiền [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là thông tin về sản phẩm kỹ thuật số không được hoàn tiền.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, giải thích rõ ràng rằng sản phẩm kỹ thuật số không được hoàn tiền và nêu rõ các ví dụ cụ thể.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ thông tin quan trọng và chính xác theo expected answer.

### [q05] Tài khoản bị khóa sau bao nhiêu lần đăng nhập sai?

**Answer:** Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, bạn có thể liên hệ IT Helpdesk hoặc tự reset qua portal SSO [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context đã retrieve.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin chính xác về số lần đăng nhập sai và cách mở khóa tài khoản.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ thông tin quan trọng về số lần đăng nhập sai và cách mở khóa tài khoản.

### [q06] Escalation trong sự cố P1 diễn ra như thế nào?

**Answer:** Escalation trong sự cố P1 diễn ra tự động lên Senior Engineer nếu không có phản hồi trong 10 phút kể từ khi ticket được tạo [2].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, cụ thể là thông tin về escalation tự động trong ticket P1.
- Relevance (4): Câu trả lời đúng trọng tâm và cung cấp thông tin cụ thể về quy trình escalation, nhưng thiếu một số chi tiết phụ như các bước cụ thể hoặc vai trò của các bên liên quan.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ thông tin quan trọng và chính xác như trong expected answer.

### [q07] Approval Matrix để cấp quyền hệ thống là tài liệu nào?

**Answer:** Tài liệu liên quan đến Approval Matrix để cấp quyền hệ thống là tài liệu "it/access-control-sop.md" [1].

- Faithfulness (1): Câu trả lời không có thông tin nào từ context, và đề cập đến một tài liệu không được nhắc đến trong context.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin cụ thể về tài liệu liên quan đến Approval Matrix.
- Context Recall (5): Recall=100% (1/1)
- Completeness (4): Câu trả lời thiếu thông tin về tên cũ của tài liệu và không đề cập rõ ràng đến 'Approval Matrix for System Access', chỉ nêu tên mới mà không giải thích rõ ràng.

### [q08] Nhân viên được làm remote tối đa mấy ngày mỗi tuần?

**Answer:** Nhân viên được làm remote tối đa 2 ngày mỗi tuần sau khi hoàn thành probation period, và lịch remote phải được Team Lead phê duyệt qua HR Portal [1].

- Faithfulness (5): Mọi thông tin trong câu trả lời đều có trong context, bao gồm điều kiện làm remote và yêu cầu phê duyệt.
- Relevance (5): Câu trả lời trực tiếp và đầy đủ, cung cấp thông tin chính xác về số ngày làm remote và điều kiện cần thiết.
- Context Recall (5): Recall=100% (1/1)
- Completeness (5): Câu trả lời bao gồm đầy đủ tất cả thông tin quan trọng như số ngày làm remote tối đa, điều kiện sau probation period và yêu cầu phê duyệt từ Team Lead.

### [q09] ERR-403-AUTH là lỗi gì và cách xử lý?

**Answer:** Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này.

- Faithfulness (1): Câu trả lời không dựa trên bất kỳ thông tin nào trong context và chủ yếu là bịa đặt.
- Relevance (1): Câu trả lời không cung cấp thông tin nào về lỗi ERR-403-AUTH và cách xử lý, do đó không trả lời câu hỏi.
- Context Recall (None): No expected sources (abstain question)
- Completeness (1): Câu trả lời thiếu phần lớn nội dung cốt lõi, không cung cấp thông tin về lỗi ERR-403-AUTH và cách xử lý.

### [q10] Nếu cần hoàn tiền khẩn cấp cho khách hàng VIP, quy trình có khác không?

**Answer:** Không đủ dữ liệu trong tài liệu hiện có để trả lời câu hỏi này.

- Faithfulness (1): Câu trả lời không dựa trên bất kỳ thông tin nào trong context đã retrieve, mà chỉ đơn giản là khẳng định không có dữ liệu.
- Relevance (1): Câu trả lời không cung cấp thông tin nào liên quan đến quy trình hoàn tiền khẩn cấp cho khách hàng VIP, chỉ nói rằng không đủ dữ liệu.
- Context Recall (5): Recall=100% (1/1)
- Completeness (2): Câu trả lời thiếu thông tin quan trọng về chính sách hoàn tiền cho khách hàng VIP và quy trình tiêu chuẩn, chỉ nêu rằng không có đủ dữ liệu mà không cung cấp thông tin cần thiết.

