# Labtainer spec

Đây là bộ skill và công cụ dùng lại, không phải workspace chứa kết quả thực hành.

- Skill điều phối: `.claude/skills/labtainer-spec/SKILL.md`; gọi `/labtainer-spec`. Mười skill `labtainer-step-01-*` đến `labtainer-step-10-*` giữ quy trình chi tiết và có thể gọi riêng.
- Đọc `README.md` để thiết lập, `config/run.example.json` để hiểu đầu vào; người dùng chỉ định file cấu hình local của lượt chạy.
- Không gán cứng thông tin kết nối, mã sinh viên, token hoặc đường dẫn của người phát triển. Không đọc/hiển thị credential nếu công việc không cần.
- Chỉ đọc skill của các bước được giao cùng chuẩn/checklist dùng chung. Không thay quy trình chi tiết bằng bản tóm tắt.
- Báo cáo và minh chứng lưu ở workspace local được cấu hình; không sinh DOCX trên VM.
- Không tự chỉnh bộ skill trong lượt kiểm thử. Khi sửa công cụ, chạy test phù hợp và kiểm tra liên kết tài liệu trước khi báo hoàn tất.
