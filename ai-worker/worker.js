// Máy chủ trung gian cho "AI xem ảnh bệnh cây" của Sổ Ruộng.
// Chạy trên Cloudflare Workers (gói miễn phí). Việc duy nhất: giữ khoá Gemini
// ở phía máy chủ — trang web công khai trên GitHub Pages, để khoá trong đó là lộ.
//
// Bí mật cần đặt trong Cloudflare (Settings → Variables and Secrets):
//   GEMINI_API_KEY   khoá tạo ở aistudio.google.com  (kiểu Secret, KHÔNG để trong code)
// Biến tuỳ chọn:
//   GEMINI_MODEL     bỏ trống = tự dò mô hình "flash" mới nhất (Google hay đổi tên)
//   CHO_PHEP_ORIGIN  danh sách trang được gọi, cách nhau dấu phẩy
//
// AI chỉ GỢI Ý khả năng + lý do nhìn thấy. Không kê thuốc — thuốc do app lấy từ
// danh mục Thông tư, người dùng tự xác nhận bệnh trước.

const ORIGIN_MAC_DINH = [
  "https://nguyenduc2k62-commits.github.io",
  "http://127.0.0.1:8000",
  "http://localhost:8000",
];
const MUC_CHAC = ["cao", "vua", "thap"];
const GOC_API = "https://generativelanguage.googleapis.com/v1beta";
const MO_HINH_MAC_DINH = "gemini-flash-latest";
let moHinhDaDo = null; // nhớ trong lúc Worker còn chạy, đỡ phải dò lại

// Lấy danh sách mô hình "flash" xem được ảnh, phiên bản cao nhất đứng đầu.
async function dsMoHinh(khoa) {
  try {
    const r = await fetch(`${GOC_API}/models?pageSize=200`, { headers: { "x-goog-api-key": khoa } });
    if (!r.ok) return null;
    const j = await r.json();
    const ds = (j.models || [])
      .filter((x) => (x.supportedGenerationMethods || []).includes("generateContent"))
      .map((x) => String(x.name || "").replace(/^models\//, ""))
      .filter((n) => /flash/.test(n) && !/(image|tts|audio|live|embedding|thinking|exp|preview|lite)/.test(n));
    const so = (n) => (n.match(/(\d+(?:\.\d+)?)/) || [0, 0])[1] * 1;
    ds.sort((a, b) => so(b) - so(a) || a.length - b.length);
    return ds;
  } catch {
    return [];
  }
}
async function doMoHinh(khoa) {
  const ds = await dsMoHinh(khoa);
  return ds.length ? ds[0] : null;
}
const ngu = (ms) => new Promise((r) => setTimeout(r, ms));
const ANH_TOI_DA = 2_500_000; // byte của chuỗi base64, ~1.8 MB ảnh

function tra(json, status, origin) {
  const h = { "content-type": "application/json; charset=utf-8" };
  if (origin) {
    h["access-control-allow-origin"] = origin;
    h["vary"] = "Origin";
  }
  return new Response(JSON.stringify(json), { status, headers: h });
}

function cat(s, n) {
  return typeof s === "string" ? s.trim().slice(0, n) : "";
}

function taoLoiNhac(cay, boPhan, ungVien) {
  const ds = ungVien.length
    ? "Danh sách dịch hại có thuốc đăng ký cho cây này theo danh mục Việt Nam (chỉ để đối chiếu tên):\n- " + ungVien.join("\n- ")
    : "Không có danh sách đối chiếu.";
  return [
    "Bạn là cán bộ bảo vệ thực vật ở Việt Nam, đang xem ẢNH do nông dân chụp.",
    cay ? `Nông dân nói đây là cây: ${cay}.` : "Nông dân chưa nói đây là cây gì — hãy tự nhận diện cây.",
    boPhan ? `Bộ phận nông dân chọn: ${boPhan}.` : "",
    "",
    "Việc cần làm: chỉ dựa vào những gì NHÌN THẤY trong ảnh, đưa tối đa 3 khả năng về bệnh / sâu hại / rối loạn dinh dưỡng.",
    "Quy tắc:",
    "- Mô tả đúng dấu hiệu nhìn thấy (màu, hình dạng vết, vị trí trên cây). Không bịa dấu hiệu không có trong ảnh.",
    "- Nếu ảnh mờ, quá xa, không phải cây, hoặc không thấy vết bệnh rõ: nói thẳng trong canhBao, có thể trả ungVien rỗng.",
    "- Nếu tên trong danh sách đối chiếu khớp khả năng của bạn, chép NGUYÊN VĂN tên đó vào khopDanhMuc; không khớp thì để null.",
    "- mucChac chỉ được là \"cao\", \"vua\" hoặc \"thap\". Đừng ghi phần trăm.",
    "- KHÔNG kê thuốc, KHÔNG ghi liều lượng.",
    "- Viết tiếng Việt có dấu, ngắn gọn, dễ hiểu với nông dân.",
    "",
    ds,
    "",
    "Trả về DUY NHẤT một JSON đúng dạng:",
    '{"laCay":true,"cayNhinThay":"tên cây","moTaTrieuChung":"...","ungVien":[{"ten":"...","khopDanhMuc":null,"lyDo":"...","mucChac":"vua"}],"canhBao":""}',
  ].filter((x) => x !== null).join("\n");
}

function docJson(text) {
  const t = String(text || "").replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "").trim();
  return JSON.parse(t);
}

function lamSach(kq, ungVien) {
  const ds = Array.isArray(kq.ungVien) ? kq.ungVien.slice(0, 3) : [];
  return {
    laCay: kq.laCay !== false,
    cayNhinThay: cat(kq.cayNhinThay, 60),
    moTaTrieuChung: cat(kq.moTaTrieuChung, 400),
    canhBao: cat(kq.canhBao, 200),
    ungVien: ds
      .map((u) => ({
        ten: cat(u && u.ten, 80),
        // Chỉ giữ tên đối chiếu nếu đúng là một tên trong danh mục đã gửi
        khopDanhMuc: u && typeof u.khopDanhMuc === "string" && ungVien.includes(u.khopDanhMuc) ? u.khopDanhMuc : null,
        lyDo: cat(u && u.lyDo, 300),
        mucChac: MUC_CHAC.includes(u && u.mucChac) ? u.mucChac : "thap",
      }))
      .filter((u) => u.ten),
  };
}

export default {
  async fetch(req, env) {
    const choPhep = env.CHO_PHEP_ORIGIN
      ? env.CHO_PHEP_ORIGIN.split(",").map((s) => s.trim()).filter(Boolean)
      : ORIGIN_MAC_DINH;
    const origin = req.headers.get("Origin") || "";
    const hopLe = choPhep.includes(origin) ? origin : "";

    if (req.method === "OPTIONS") {
      if (!hopLe) return new Response(null, { status: 403 });
      return new Response(null, {
        status: 204,
        headers: {
          "access-control-allow-origin": hopLe,
          "access-control-allow-methods": "POST, OPTIONS",
          "access-control-allow-headers": "content-type",
          "access-control-max-age": "86400",
          "vary": "Origin",
        },
      });
    }

    const url = new URL(req.url);
    if (url.pathname !== "/chan-doan" || req.method !== "POST") {
      return tra({ loi: "Không có đường dẫn này" }, 404, hopLe);
    }
    // Chặn trang lạ gọi từ trình duyệt. (Công cụ ngoài trình duyệt vẫn giả được
    // Origin — khi dùng thật cần thêm giới hạn lượt theo IP.)
    if (!hopLe) return tra({ loi: "Trang này không được phép gọi" }, 403, "");
    if (!env.GEMINI_API_KEY) return tra({ loi: "Máy chủ chưa đặt khoá GEMINI_API_KEY" }, 500, hopLe);

    const dai = parseInt(req.headers.get("content-length") || "0", 10);
    if (dai > ANH_TOI_DA + 50_000) return tra({ loi: "Ảnh quá lớn" }, 413, hopLe);

    let vao;
    try {
      vao = await req.json();
    } catch {
      return tra({ loi: "Dữ liệu gửi lên không đọc được" }, 400, hopLe);
    }
    const m = /^data:(image\/(?:jpeg|png|webp));base64,([A-Za-z0-9+/=]+)$/.exec(String(vao.anh || ""));
    if (!m) return tra({ loi: "Thiếu ảnh hoặc sai định dạng (cần JPEG/PNG/WEBP)" }, 400, hopLe);
    if (m[2].length > ANH_TOI_DA) return tra({ loi: "Ảnh quá lớn" }, 413, hopLe);
    const cay = cat(vao.cay, 60);
    const boPhan = cat(vao.boPhan, 30);
    const ungVien = Array.isArray(vao.ungVien)
      ? vao.ungVien.filter((x) => typeof x === "string" && x.length <= 120).slice(0, 300)
      : [];

    const noiDung = JSON.stringify({
      contents: [{
        role: "user",
        parts: [
          { text: taoLoiNhac(cay, boPhan, ungVien) },
          { inline_data: { mime_type: m[1], data: m[2] } },
        ],
      }],
      generationConfig: { responseMimeType: "application/json", temperature: 0.2 },
    });
    const goi = (ten) => fetch(`${GOC_API}/models/${encodeURIComponent(ten)}:generateContent`, {
      method: "POST",
      headers: { "content-type": "application/json", "x-goog-api-key": env.GEMINI_API_KEY },
      body: noiDung,
    });

    let model = env.GEMINI_MODEL || moHinhDaDo || MO_HINH_MAC_DINH;
    let r;
    try {
      r = await goi(model);
      // Google hay ngừng tên mô hình cũ (404). Hỏi danh sách mô hình khoá này dùng được,
      // chọn bản "flash" mới nhất, gửi lại một lần.
      if (r.status === 404 && !env.GEMINI_MODEL) {
        const moi = await doMoHinh(env.GEMINI_API_KEY);
        if (moi && moi !== model) {
          model = moi;
          moHinhDaDo = moi;
          r = await goi(model);
        }
      }
      // Quá tải tạm thời (503/500): chờ chút thử lại, rồi thử một mô hình flash khác.
      if (r.status === 503 || r.status === 500) {
        await ngu(1200);
        r = await goi(model);
      }
      if ((r.status === 503 || r.status === 500) && !env.GEMINI_MODEL) {
        const ds = (await dsMoHinh(env.GEMINI_API_KEY)).filter((x) => x !== model);
        for (const ten of ds.slice(0, 2)) {
          const r2 = await goi(ten);
          if (r2.ok || (r2.status !== 503 && r2.status !== 500 && r2.status !== 404)) { r = r2; model = ten; break; }
        }
      }
    } catch {
      return tra({ loi: "Không kết nối được tới Gemini" }, 502, hopLe);
    }
    if (r.status === 503 || r.status === 500) return tra({ loi: "AI đang quá tải — thử lại sau ít phút", model }, 503, hopLe);
    if (r.status === 429) return tra({ loi: "Hết lượt miễn phí của AI lúc này — thử lại sau ít phút hoặc ngày mai" }, 429, hopLe);
    if (!r.ok) {
      // Chuyển kèm lý do Google đưa ra (vd "API key not valid") — câu này không chứa khoá.
      let lyDo = "";
      try {
        const e = await r.json();
        lyDo = cat(e && e.error && (e.error.message || e.error.status), 200);
      } catch {}
      console.log("Gemini loi", r.status, model, lyDo);
      return tra({ loi: "Gemini báo lỗi " + r.status + (lyDo ? ": " + lyDo : ""), model }, 502, hopLe);
    }

    let kq;
    try {
      const j = await r.json();
      const text = j && j.candidates && j.candidates[0] && j.candidates[0].content
        && j.candidates[0].content.parts && j.candidates[0].content.parts.map((p) => p.text || "").join("");
      kq = lamSach(docJson(text), ungVien);
    } catch {
      return tra({ loi: "AI trả lời không đúng dạng — thử lại" }, 502, hopLe);
    }
    return tra({ ...kq, model }, 200, hopLe);
  },
};
