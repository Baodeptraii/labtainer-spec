# labtainer-spec

Bộ skill cho Claude Code để chuẩn hóa, build và kiểm thử Labtainer theo quy trình 10 bước. Một skill điều phối `/labtainer-spec` và 10 skill từng bước, giữ quy trình chi tiết, đầu vào cấu hình rõ ràng và báo cáo DOCX theo mẫu học viện.

**Phiên bản:** 1.0.0 · **Python:** 3.10+ · **License:** [MIT](LICENSE) cho code/hướng dẫn; [NOTICE](NOTICE.md) cho template/logo.

## 1. Cấu trúc

```text
labtainer-spec/
├── README.md                         # Hướng dẫn cho người vận hành
├── CLAUDE.md                         # Chỉ dẫn ngắn cho agent
├── config/run.example.json           # Mẫu đầu vào, không chứa credential
├── docs/architecture.md              # Quyết định cấu trúc và cách chuyển đổi
├── tools/                            # Cài đặt và kiểm tra/đóng gói bản phát hành
└── .claude/skills/
    ├── labtainer-step-01-audit/       # SKILL.md từng bước
    ├── ...                          # Đầy đủ bước 02–09
    ├── labtainer-step-10-review-report/
    └── labtainer-spec/
        ├── SKILL.md                  # Skill điều phối
        ├── references/               # Chuẩn/checklist và hướng dẫn dùng chung
        ├── scripts/                  # Launcher, queue, render, helpers
        ├── assets/                   # Mẫu DOCX và HTML
        ├── templates/report-data.json
        └── tests/                    # Test offline, không chạy lab
```

Tên `labtainer-spec` dùng kebab-case, trùng tên thư mục và trường `name`. Skill là một thư mục có `SKILL.md`, hỗ trợ `references/`, `scripts/`, `assets/` theo [Agent Skills specification](https://agentskills.io/specification). Claude Code nhận project skill trong `.claude/skills/` và gọi bằng `/labtainer-spec` theo [tài liệu Claude Code](https://code.claude.com/docs/en/skills). Chi tiết quyết định: [architecture.md](docs/architecture.md).

## Cài đặt nhanh

1. Tải ZIP từ GitHub Release hoặc clone repository này, mở terminal tại thư mục labtainer-spec.
2. Kiểm tra `python --version`, `ssh -V` và Claude Code đã cài. Tạo báo cáo không cần dependency Python ngoài.
3. Chạy `python tools/release.py check`; sao chép config mẫu thành config/run.local.json và điền theo mục 3.
4. Cấp mật khẩu qua biến môi trường, xác minh host key theo mục 4. Khởi động `claude` từ cùng terminal.
5. Gọi `/labtainer-spec` hoặc step cụ thể bên dưới.

Để cài toàn bộ skills vào project Claude Code khác:

```powershell
python tools/install.py --target '<đường dẫn project của bạn>'
```

Installer giữ CLAUDE.md/settings hiện có, từ chối file xung đột và cho phép chạy lại nếu nội dung giống nhau. Khởi động lại Claude Code tại project đích. Không cài riêng một step: scripts/template nằm ở coordinator. Clone/giải nén là cách đơn giản nhất khi chưa có project.

### Skill từng bước

| Lệnh | Công việc |
|---|---|
| `/labtainer-spec` | Điều phối phạm vi được giao |
| `/labtainer-step-01-audit` | Audit bài gốc, nhận xét và minh chứng |
| `/labtainer-step-02-scenario-cybok` | Tổng hợp lỗi, CyBOK, câu hỏi |
| `/labtainer-step-03-html-guide` | Biên soạn HTML hiệu chỉnh |
| `/labtainer-step-04-tech-report` | Báo cáo và kế hoạch kỹ thuật |
| `/labtainer-step-05-prep-rename` | Source gốc, đổi tên và cấu hình |
| `/labtainer-step-06-rebuild-test` | Sửa logic, rebuild, kiểm thử |
| `/labtainer-step-07-publish-imodule` | Đóng gói, phát hành, cập nhật URL |
| `/labtainer-step-08-connect-test` | Kết nối tester, chuẩn bị công cụ |
| `/labtainer-step-09-execute-html` | Tải gói và thực hành lại bản hiệu chỉnh |
| `/labtainer-step-10-review-report` | Sinh DOCX theo mẫu học viện |

Kiểm thử URL/HTML đã có không cần bước 1–7. Thực nghiệm vẫn cần VM, desktop, quyền và đầu vào hợp lệ; bộ skill không cung cấp VM hoặc tài khoản cá nhân.

## 2. Ba nơi cần phân biệt

| Nơi | Chức năng |
|---|---|
| Project `labtainer-spec` trên máy thật | Claude Code, skill, công cụ, mẫu; mở Claude Code tại đây |
| Workspace lượt kiểm thử trên máy thật | HTML staging, manifest, ảnh/log/.lab, báo cáo; đặt trong `workspaces/<run-id>` hoặc đường dẫn ngoài project |
| Host Labtainer qua SSH | Tải imodule, chạy bài/container/GUI, checkwork, stoplab, tạo minh chứng |

“Kết nối workspace” không phải SSH vào thư mục. Agent mở project local, đọc file cấu hình trỏ đến workspace local, rồi SSH tới **host** được cấu hình. Báo cáo sinh trên máy thật, không cần cài Claude Code hay renderer DOCX trên VM.

Không có host/user/password/mã sinh viên thật mặc định. Người nhận phải điền cấu hình của mình. Đừng sao chép cấu hình local, Git worktrees hoặc hồ sơ thực nghiệm của người khác vào bundle bàn giao.

## 3. Chuẩn bị đầu vào

Đối với bước 8–10 cần:

- HTML hướng dẫn đã hiệu chỉnh và các tài nguyên tương đối (ảnh/CSS nếu có).
- URL imodule đúng bản cần chạy; nhận URL bất kỳ được giao, ưu tiên ptitdseclab khi lựa chọn, không giới hạn ptit2026.
- IP/hostname, cổng, user SSH; mật khẩu trong môi trường tiến trình và file known_hosts đã xác minh.
- Mã sinh viên; workspace; nơi lưu báo cáo; thông tin bìa nếu có.

Không cần source ZIP hoặc làm bước 1–7 để kiểm thử gói đã có. Không yêu cầu snapshot sạch/VM độc lập. Nếu chỉ có URL, agent tìm hướng dẫn trong nguồn/gói; thiếu thì báo phần còn thiếu, không tự bịa nhiệm vụ.

Từ terminal **PowerShell**, tại project:

```powershell
Copy-Item -LiteralPath 'config/run.example.json' -Destination 'config/run.local.json'
```

Sửa `run.local.json`:

| Trường | Cách điền |
|---|---|
| source_html | Đường dẫn đến HTML thật; không trỏ vào template |
| imodule_url | URL gói được giao; không đặt user/password/token trong URL |
| connection.host / username / port | Host tester, user, cổng SSH |
| connection.password_env | Tên biến chứa mật khẩu, ví dụ `LABTAINER_SSH_PASSWORD`; không phải giá trị mật khẩu |
| connection.known_hosts | Đường dẫn file fingerprint server đã xác minh |
| student_id | Mã sinh viên cần nhập tại prompt |
| workspace | Thư mục lượt; mode retest nên dùng tên/run-id mới |
| report_directory | Thư mục nhận DOCX; nên dùng workspace/report để khớp helper |
| mode | review / retest / resume |
| steps | `[8, 9, 10]` cho kiểm thử và báo cáo; chọn bước khác khi được giao |

Mọi đường dẫn tương đối tính từ **thư mục file config**, vì vậy `../workspaces/run-01` là project/workspaces/run-01. Có thể dùng đường dẫn tuyệt đối; trong JSON Windows dùng `/` hoặc escape `\\`. Tiêu đề terminal và thư mục framework có thể để trống để agent xác minh. Không sửa SKILL.md để thay cấu hình.

## 4. Kết nối và password

Máy thật cần Python 3.10+ và SSH. Backend mật khẩu dùng Paramiko; bộ queue/render chỉ dùng thư viện chuẩn. Kiểm tra công cụ hiện có trước khi cài. Có thể dùng uv cấp dependency cho đúng lệnh, không cài trên container.

Xác minh fingerprint với host Labtainer rồi kết nối tương tác một lần bằng OpenSSH để ghi known_hosts. Không tắt host key checking. File này xác thực máy chủ, không phải private key để đăng nhập. Backend mật khẩu không cần SSH key/AES.

Đặt mật khẩu trong phiên PowerShell mà không ghi literal vào lịch sử:

```powershell
$securePassword = Read-Host 'SSH password' -AsSecureString
$env:LABTAINER_SSH_PASSWORD = [System.Net.NetworkCredential]::new('', $securePassword).Password
$skill = Join-Path (Get-Location) '.claude/skills/labtainer-spec'
python "$skill/scripts/run_config.py" 'config/run.local.json' --check
```

`--check` xác minh trường/đường dẫn và biến password tồn tại; **không** thử kết nối SSH, không chứng minh mật khẩu đúng. Hostname, known_hosts và HTML phải đã được điền. Nếu kiểm tra đạt, chạy lệnh quan sát desktop:

```powershell
uv run --with paramiko python "$skill/scripts/run_config.py" 'config/run.local.json' -- python -m helpers.cli vm-list-windows
```

Nếu Python hiện tại đã có Paramiko, bỏ `uv run --with paramiko`. Launcher truyền cấu hình chỉ cho subprocess và không in password. Sau khi xác minh cửa sổ, điền `connection.student_window`; không đoán tiêu đề theo VM mẫu.

Khởi động `claude` từ cùng phiên terminal để agent kế thừa biến password. Nếu dùng ứng dụng IDE khởi chạy từ nơi khác, cấp biến môi trường cho tiến trình đó; biến ở terminal cũ không tự xuất hiện trong agent mới. Kết thúc phiên thì xóa biến:

```powershell
Remove-Item Env:LABTAINER_SSH_PASSWORD
```

Agent được tự chuẩn bị công cụ kết nối/chụp/truyền trên host trước thực hành. Sau khi bài chạy, không cài thêm trên host/container. Nếu đang tiếp tục bài dở thiếu công cụ, lưu checkpoint và nêu nhánh bị chặn.

## 5. Giao việc cho Claude Code

Mở project này trong Claude Code, nhập:

```text
/labtainer-spec
Đọc config/run.local.json và thực hiện các steps đã khai báo. Dùng đúng host,
HTML, URL và đường dẫn của lượt này. Tải bản imodule được giao, thực hành lại
toàn bộ HTML hiệu chỉnh, chụp/xem ảnh mới từng bước, checkwork, stoplab và thu .lab.
Sinh DOCX trên máy thật theo mẫu học viện vào report_directory. Giữ kết quả cũ.
Tiếp tục đến khi hoàn tất hoặc có BLOCKED thực tế; bàn giao đường dẫn và bằng chứng.
```

`/labtainer-spec` là chỉ dẫn agent, không tự chạy workflow chỉ bằng một file JSON. Agent phải đọc references theo phạm vi và dùng tool thực tế. Lệnh cần quyền runtime vẫn theo thiết lập Claude Code; bundle không vô hiệu hóa các kiểm soát đó.

Các cách dùng khác:

- Chuẩn hóa: yêu cầu bước 1–4, cung cấp hướng dẫn/source gốc và nơi nhận HTML/tài liệu.
- Build: yêu cầu 5–7, cung cấp source, host build và registry/repo được phép; không lấy host tester làm host build mặc định.
- Chỉ báo cáo: steps `[10]`, giao manifest/run-dir đã có; không cần mật khẩu SSH và không tự thực hành lại.
- Kiểm thử lại: mode `retest`, workspace mới; không bị SKIP vì báo cáo lượt trước đã tồn tại.
- Tiếp tục: mode `resume`, workspace và checkpoint đúng lượt; agent kiểm tra hash và trạng thái VM trước thao tác.

## 6. Workspace và sản phẩm

```text
workspaces/run-01/
├── html/<nhóm>/<lab>.html
└── report/
    ├── <nhóm>/<lab>.docx
    └── _work/<nhóm>/<lab>/<run-id>/
        ├── report-data.json
        ├── evidence/*.png
        ├── artifacts/...
        └── draft.docx                 # chỉ khi có bản nháp
```

Agent staging HTML nguyên byte và ghi hash. Helper không tự tải file đầu vào hoặc sinh bằng chứng. Có thể dùng local:

```powershell
$workspace = 'workspaces/run-01'
python "$skill/scripts/workspace_queue.py" scan --workspace "$workspace"
python "$skill/scripts/workspace_queue.py" prepare 'html/group/lab.html' --workspace "$workspace"
# Điền manifest bằng thực nghiệm trước khi render:
python "$skill/scripts/render_report.py" "$manifest" --workspace "$workspace"
```

`$manifest` lấy từ kết quả prepare, không phải file schema trống. `report_directory` khác mặc định được agent xử lý bằng sao chép DOCX sau kiểm tra, không đổi mapping của renderer hoặc ghi đè đích.

PASS cần các bước đạt có ảnh, checkwork đủ Y và .lab thật. FAIL là bài có lỗi được chứng minh nhưng báo cáo đã hoàn tất. BLOCKED chỉ lưu checkpoint/nháp; chưa chạy không phải N/A. Chụp GUI đúng cửa sổ, không thay ảnh bằng stdout, không ép grader Y. Không tự nộp SecLab hay suy AC.

Mẫu học viện nằm ở `assets/report-template.docx`. Giữ bìa/logo/styles/lề/footer; mục lục helper chưa tính số trang tự động. Kiểm tra bố cục bằng Word/LibreOffice nếu có; nêu rõ giới hạn nếu chỉ kiểm tra cấu trúc.

## 7. Kiểm tra và bàn giao bộ skill

```powershell
python -B -m unittest discover -s "$skill/tests" -v
```

Test chạy offline bằng fixture, không kết nối VM, không tạo bằng chứng học tập thật. Kết quả kiểm tra cấu trúc/đóng gói: [verification.md](docs/verification.md).

Tạo ZIP theo allowlist và file SHA-256:

```powershell
python tools/release.py build
```

Đầu ra: dist/labtainer-spec-1.0.0.zip và file .sha256. Không gửi cấu hình local, password, workspace thực nghiệm, .git hoặc worktrees. Khi fork để phát hành, chạy kiểm tra trước push/tag. Xem [release checklist](docs/releasing.md).

## Đóng góp và giấy phép

- Contributors: [lucastran05](https://github.com/lucastran05), [re3on](https://github.com/re3on).
- [CONTRIBUTING.md](CONTRIBUTING.md): thay đổi quy trình mà không mất chi tiết thực thi.
- [LICENSE](LICENSE): MIT cho code/hướng dẫn. Template/logo có quyền riêng theo [NOTICE.md](NOTICE.md).
- [CHANGELOG.md](CHANGELOG.md): thay đổi theo phiên bản.
