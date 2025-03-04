# Configuration file for paths, constants, etc.

CHROMA_PATH = ".chroma"  # Path to store the Chroma database
CACHE_PATH = ".cache"  # Path to store the scrape cache
LOCAL_SOURCES_PATH = "sources"  # Path to the local sources
WEB_URLS = [
    "https://clc.hust.edu.vn/vstep/vstep-la-gi/",
    "https://etc.sgu.edu.vn/gioi-thieu/",
    "https://vi.wikipedia.org/wiki/VSTEP",
    "https://vi.wikipedia.org/wiki/Khung_n%C4%83ng_l%E1%BB%B1c_ngo%E1%BA%A1i_ng%E1%BB%AF_6_b%E1%BA%ADc_d%C3%B9ng_cho_Vi%E1%BB%87t_Nam",
    "https://vstep.edu.vn/VstepQA",
    "https://vstep.edu.vn/danh-sach-cac-truong-su-dung-chung-chi-vstep-trong-tuyen-sinh-dai-hoc",
    "https://vstep.edu.vn/chung-chi-vstep-tu-bac-3-duoc-mien-thi-tot-nghiep-thpt-mon-ngoai-ngu",
    "https://etc.sgu.edu.vn/thong-bao-nhan-chung-chi-tieng-anh-theo-khung-nlnn-6-bac-dung-cho-viet-nam-ky-thi-ngay-21-12-2024/",
    "https://etc.sgu.edu.vn/thong-bao-ve-viec-hoan-ky-thi-tieng-anh-theo-khung-nlnn-6-bac-ngay-11-01-2025/",
]
FORCE_FIRECRAWL_URLS = [
    # "https://thuvienphapluat.vn/van-ban/giao-duc/Thong-tu-01-2014-TT-BGDDT-Khung-nang-luc-ngoai-ngu-6-bac-Viet-Nam-220349.aspx",
]
PROMPT_TEMPLATE = """
Bạn đang đóng vai trò là một nhân viên hỗ trợ giải đáp thắc mắc của mọi người về quy chế thi của cuộc thi tiếng Anh VSTEP. Hãy nhận biết và trả lời cho câu hỏi: "{question}" bằng cách chỉ dựa vào các đoạn thông tin được trích dẫn dưới đây, không sử dụng thông tin nào khác bên ngoài và hãy trả lời thật đầy đủ và chính xác các thông tin bằng cách diễn giải câu hỏi lại một cách tự nhiên nhất bằng tiếng Việt, bỏ đi những từ ngữ không rõ ràng hoặc không cần thiết, không cần nhắc lại và diễn giải câu hỏi, hãy đưa ra câu trả lời một cách trực tiếp, nếu nội dung bên dưới không đủ để trả lời câu hỏi, hãy đưa ra lời từ chối trả lời một cách lịch sự và khéo léo nếu bạn không thể trả lời:

{context}

"""
