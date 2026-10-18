# Kiến trúc bộ skill

## Coordinator và mười step skill

labtainer-spec là tên dự án và skill điều phối. Mỗi bước giữ SKILL.md riêng, tên dạng labtainer-step-01-audit. Tên thư mục trùng trường name, dùng chữ thường và dấu gạch nối. Mỗi step gọi được trực tiếp; coordinator chọn step theo phạm vi.

Các step giữ quy trình chi tiết gốc. Không thay chúng bằng bản tóm tắt vì có thể mất điều kiện thực thi. Chuẩn/checklist, scripts và assets dùng chung nằm trong coordinator để tránh sai khác bản sao.

Cấu trúc theo [Agent Skills](https://agentskills.io/specification) và [Claude Code skills](https://code.claude.com/docs/en/skills). README hướng dẫn người vận hành, CLAUDE.md định tuyến agent; không thêm quyền bỏ qua kiểm soát runtime.

## Dữ liệu

| Loại | Vị trí | Có trong bản phát hành |
|---|---|---|
| Skill, code, test, tài liệu | Repository | Có |
| Template/logo | assets/ | Có, quyền riêng tại NOTICE.md |
| Host/user/mã sinh viên/đường dẫn | config/*.local.json | Không |
| Password/token | Biến môi trường hoặc credential store | Không |
| HTML/ảnh/log/.lab/DOCX thực tế | Workspace từng lượt | Không |

Package tạo theo allowlist, không chứa history, worktree hay cấu hình cá nhân. .gitignore không tự xóa bí mật đã commit.

## Cài đặt

Clone/giải nén repository thành project Claude Code, điền cấu hình và chuẩn bị VM. Installer tùy chọn sao chép cả 11 skill sang project khác, giữ liên kết tương đối; không ghi đè CLAUDE.md/settings hoặc file khác nội dung. Không cài riêng một step mà thiếu coordinator.

## Giới hạn

JSON là đầu vào cho agent và launcher, không phải engine tự giải bài. Helpers không chứng minh ảnh thật hoặc mục tiêu học tập đạt. Các VM/desktop khác nhau vẫn cần xác minh; không hứa chạy lab khi chưa có SSH, credential và HTML thật.
