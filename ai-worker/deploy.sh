#!/usr/bin/env bash
# Đưa Worker lên Cloudflare:  bash ai-worker/deploy.sh
# Cần file ai-worker/.cf-token chứa API token Cloudflare (mẫu "Edit Cloudflare Workers",
# tài khoản nguyenduc2k62). File đó bị .gitignore chặn — KHÔNG đưa lên GitHub.
# Không dùng `wrangler login` vì trên Windows nó hay lỗi và chỉ chờ 2 phút.
set -e
cd "$(dirname "$0")"
TOK=$(python -c "import re;t=open('.cf-token',encoding='utf-8-sig').read();m=re.findall(r'[A-Za-z0-9_\-]{30,}',t);print(m[0] if m else '')")
if [ ${#TOK} -lt 30 ]; then echo "Thiếu mã trong ai-worker/.cf-token"; exit 1; fi
export CLOUDFLARE_API_TOKEN="$TOK" CLOUDFLARE_ACCOUNT_ID="e406c13306f30dda67f06338ffd3757e"
# Che mã nếu wrangler lỡ in ra trong thông báo lỗi
npx -y wrangler@latest deploy 2>&1 | sed -E 's/cf[a-z]*_[A-Za-z0-9_-]{20,}/***/g' | grep -v -i telemetry
