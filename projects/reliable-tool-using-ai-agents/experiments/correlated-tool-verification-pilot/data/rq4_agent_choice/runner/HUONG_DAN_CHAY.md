# Hướng dẫn chạy thí nghiệm RQ4 trên máy RTX 4060

Thời gian ước tính khoảng 1–2 giờ, phần lớn là chờ máy chạy. Máy cần Windows hoặc Linux, GPU NVIDIA 8 GB và Python 3.9 trở lên. Không cần cài thêm thư viện Python nào.

## 1. Chép thư mục này sang máy mượn

Chép **cả thư mục `runner/`**, gồm `run_rq4.py`, `items.jsonl` và file hướng dẫn này. Không sửa `items.jsonl`: script kiểm tra SHA-256 của file và sẽ từ chối chạy nếu file bị thay đổi.

## 2. Cài Ollama và tải 2 model

1. Tải Ollama từ trang chính thức <https://ollama.com/download> rồi cài đặt.
2. Mở terminal (PowerShell trên Windows) và tải 2 model, mỗi model khoảng 5 GB:

```
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull llama3.1:8b-instruct-q4_K_M
```

3. Kiểm tra Ollama đang chạy: mở <http://localhost:11434> trên trình duyệt, thấy dòng "Ollama is running" là được.

## 3. Chạy thử (không cần model)

```
python run_rq4.py --dry-run --model fake --out fake.jsonl
```

Lệnh này phải in ra `1008/1008 done`. Sau khi chạy thử xong, xóa file `fake.jsonl`.

## 4. Chạy thật, lần lượt từng model

```
python run_rq4.py --model qwen2.5:7b-instruct-q4_K_M --out results_qwen.jsonl
python run_rq4.py --model llama3.1:8b-instruct-q4_K_M --out results_llama.jsonl
```

- Mỗi model chạy 1.008 câu hỏi, mất khoảng 20–40 phút.
- **Nếu bị ngắt giữa chừng**, chạy lại đúng lệnh đó: script sẽ chạy tiếp từ chỗ dừng.
- **Trong lúc chạy, không đổi model hay cài đặt của Ollama.**

## 5. Mang kết quả về

Chép `results_qwen.jsonl` và `results_llama.jsonl` về máy của anh rồi gửi cho Claude. Đừng mở và sửa hai file này.

## Nếu gặp lỗi

- **`Connection refused`:** Ollama chưa chạy. Mở ứng dụng Ollama, hoặc chạy `ollama serve`.
- **`model not found`:** tên model trong lệnh chưa đúng với tên đã `pull`. Kiểm tra bằng `ollama list`.
- **Lỗi khác:** chụp màn hình thông báo lỗi gửi Claude, không tự sửa script.
