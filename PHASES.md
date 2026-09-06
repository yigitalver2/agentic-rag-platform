# PHASES.md — Agentic RAG Platformu Uygulama Planı

> Bu dosya **sıra** dosyasıdır. Bir faz bitmeden sonrakine geçilmez.
> Süre değil, **Definition of Done** ölçüsü geçerlidir.
> Kurallar için `CLAUDE.md`, kapsam için `docs/PRD.md`.

---

## Nasıl okunur

Her faz şu bölümlerden oluşur:

- **Amaç** — bu faz bittiğinde sistemin kazandığı yetenek
- **Öğrenilecek kavramlar** — bu fazın asıl ürünü
- **Adımlar** — Claude Code'a tek tek verilecek birimler
- **Definition of Done** — ölçülebilir bitiş kriteri
- **Kendini test et** — cevaplayamıyorsam faz bitmemiştir
- **Yaygın tuzaklar** — bu fazda insanların düştüğü hatalar
- **Bu fazda YAPMAYACAKLARIMIZ** — scope creep freni

### Neden PRD'nin 8 haftalık takvimini kullanmıyoruz

PRD'deki takvim, bu teknolojileri zaten bilen birinin uygulama hızıdır. Öğrenme modunda
her adım *anlaşılana* kadar sürer. Bu yüzden burada süre yok, kapı (gate) var.
Kabaca eşleme: PRD Hafta 1 ≈ Faz 1, Hafta 2 ≈ Faz 2, Hafta 3 ≈ Faz 3-4, Hafta 4 ≈ Faz 5,
Hafta 5 ≈ Faz 6, Hafta 6 ≈ Faz 7-8, Hafta 7 ≈ Faz 9, Hafta 8 ≈ Faz 10.

### Eval dataset uyarısı (projenin gizli maliyet merkezi)

PRD 200 soruluk, manuel doğrulanmış bir dataset istiyor. Bu tek başına günlerce sürer ve
projeyi Faz 3'te kilitleyebilir. Bu yüzden dataset **kademeli** büyütülür:

| Sürüm | Adet | Ne zaman | Amaç |
|---|---|---|---|
| eval-v0.1 | 40 | Faz 3 | Harness'ı çalıştırmak, ilk baseline |
| eval-v0.5 | 100 | Faz 5 sonu | Agent ve router kararlarını ayırt etmek |
| eval-v1.0 | 200 | Faz 10 öncesi | Release/holdout kararları |

40 soru istatistiksel olarak gürültülüdür — bunu bilerek kullanıyoruz. İlk amaç
"doğru sayıyı bulmak" değil, **ölçüm makinesini kurmak.**

---

## Faz 0 — Zemin ve kavram haritası

**Amaç:** Repo, ortam ve temel altyapı ayakta; kod yazmadan önce sistemin zihinsel haritası net.

**Öğrenilecek kavramlar:** monorepo/paket ayrımı, dependency management (uv/poetry),
`pydantic-settings` ile config, docker compose ile local servis orkestrasyonu, 12-factor config,
neden `.env` sırları koda girmez.

**Adımlar**

- **0.1** Repo iskeleti + `pyproject.toml` + uv/poetry seçimi
- **0.2** `ruff` + `mypy/pyright` + `pytest` konfigürasyonu; boş bir test'in geçtiğini görmek
- **0.3** `Settings` sınıfı (`pydantic-settings`), `.env.example`, config'in nasıl yüklendiğini izlemek
- **0.4** `docker-compose.yml`: PostgreSQL (+pgvector) ve Redis; bağlantı sağlık kontrolü
- **0.5** FastAPI iskeleti: `/health/live`, `/health/ready` — ikisinin farkı ve neden ayrı oldukları
- **0.6** Alembic kurulumu ve ilk boş migration

**Definition of Done**
- `uv run pytest` yeşil, `ruff check` ve type check temiz
- `docker compose up` sonrası `/health/ready` DB ve Redis'i gerçekten kontrol ediyor
- `alembic upgrade head` çalışıyor

**Kendini test et**
1. `/health/live` ile `/health/ready` arasındaki fark nedir, hangisi ECS'e ne söyler?
2. Config değeri hangi sırayla çözülür (default → .env → environment)?
3. pgvector nedir, PostgreSQL'e ne ekliyor?

**Yaygın tuzaklar:** her şeyi tek `main.py`'de başlatmak; `.env`'i commit'lemek;
health check'i sadece `return {"ok": true}` yapmak (ECS bunu yanlış yorumlar).

**YAPMAYACAKLARIMIZ:** LLM çağrısı, PDF, frontend, AWS.

---

## Faz 1 — Provider abstraction + local LLM

**Amaç:** Ollama, OpenAI ve Anthropic'in **aynı arayüz** arkasından çağrılabilmesi ve
her çağrının ölçülmesi.

Bu faz neden ilk? Çünkü sonraki her şey (retrieval grading, agent node'ları, eval judge'ı, router)
LLM çağrısı yapar. Abstraction sonradan eklenirse, o zamana kadar yazılmış her yer değişir.

**Öğrenilecek kavramlar:** `Protocol` / structural typing, adapter pattern, structured output
(JSON schema ile zorlanmış çıktı), tool calling mekaniği, quantization (Q4 ne demek),
token/context window, TTFT vs total latency, cold vs warm load, KV cache.

**Adımlar**

- **1.1** Ollama kurulumu, `qwen3.5:4b` ve `9b` çekilmesi; ham `curl` ile ilk çağrı — HTTP seviyesinde ne gidiyor?
- **1.2** `LLMRequest` / `LLMResult` Pydantic modelleri + `LLMProvider` Protocol tanımı
- **1.3** `OllamaProvider.generate()` — streaming ve non-streaming
- **1.4** `generate_structured()` — JSON schema ile çıktı zorlama; schema invalid olduğunda ne yapıyoruz
- **1.5** `call_tools()` — tool schema, tool call parsing, argüman doğrulama
- **1.6** `OpenAIProvider` ve `AnthropicProvider` — **logical slot** mantığı (`OPENAI_FAST` vs exact model ID)
- **1.7** Benchmark collector: Ollama'nın `total_duration`, `load_duration`, `prompt_eval_count`,
  `eval_count` alanlarını + cloud `usage` alanlarını normalize eden tek bir `ModelCall` kaydı
- **1.8** Cost hesaplayıcı: config'ten fiyat tablosu, çağrı başına maliyet
- **1.9** `FakeProvider` — deterministik test provider'ı (CI bunu kullanacak)
- **1.10** İlk mini benchmark: 4B vs 9B, aynı 10 prompt, cold/warm ayrımı, sonuç tablosu

**Definition of Done**
- Aynı test dosyası üç provider'la da geçiyor (`FakeProvider` dahil)
- Kodun hiçbir yerinde `import openai` iş mantığının içinde geçmiyor
- Her çağrı `ModelCall` kaydı üretiyor: provider, exact model id, tokens, latency, cost
- `evals/reports/` altında ilk local inference tablosu var (cold load, TTFT, tok/s, peak memory)

**Kendini test et**
1. `Protocol` ile abstract base class arasındaki fark ne, neden Protocol seçtik?
2. Q4 quantization neyi kaybettiriyor, karşılığında ne kazandırıyor?
3. Structured output "prompt'ta JSON iste" ile aynı şey mi? Değilse mekanik fark ne?
4. Cold ve warm latency'yi ayrı raporlamazsak benchmark'ta ne yanlış görünür?
5. Model ID'yi hard-code etseydik, 3 ay sonra hangi somut sorun çıkardı?

**Yaygın tuzaklar:** provider farklarını (Anthropic'in `system` parametresi, OpenAI'ın
`response_format`'ı) abstraction'a sızdırmak; latency'yi wall-clock ölçüp cold load'ı içine katmak;
tool argümanını schema doğrulamadan kullanmak.

**YAPMAYACAKLARIMIZ:** retrieval, PDF, router (router Faz 6). Şu an sadece "aynı arayüz + ölçüm".

---

## Faz 2 — Ingestion + baseline RAG (dense-only)

**Amaç:** PDF yükle → parse → chunk → embed → index → **kaynak göstererek** cevapla.
En basit, en dürüst RAG.

**Öğrenilecek kavramlar:** PDF'in aslında ne olduğu (metin değil, konumlandırılmış glyph'ler),
reading order problemi, chunking stratejileri ve overlap'in amacı, embedding uzayı, cosine similarity,
ANN index (HNSW/IVF) vs exact search, checksum ile idempotency, citation'ın chunk metadata'sına bağımlılığı.

**Adımlar**

- **2.1** Veri modeli: `collections`, `documents`, `chunks` tabloları + Alembic migration
- **2.2** Upload endpoint: SHA-256 checksum, MIME/type validation, S3 yerine local storage adapter
- **2.3** Parser adapter arayüzü + native text parser (PyMuPDF); sayfa numarası korunması
- **2.4** Türkçe karakter testi: İ, ı, Ğ, ğ, Ş, ş, Ö, ö, Ç, ç round-trip
- **2.5** Chunking: recursive token-based + overlap; `chunk_size`/`overlap` **config parametresi** olarak
- **2.6** Chunk metadata: `document_id`, `page_start/end`, `section_title`, `chunk_index`, `checksum`, `language`, `parser_version`
- **2.7** Embedding provider (Ollama embedding modeli) + embedding cache
- **2.8** pgvector index + dense retrieval sorgusu; `top_k` config'te
- **2.9** Context packer v0: token budget'a göre chunk seçimi
- **2.10** Answer node: prompt + citation formatı; her iddia hangi chunk'a dayanıyor
- **2.11** `/v1/chat/query` endpoint'i: answer + citations + trace_id + latency + usage
- **2.12** Basit "abstain": context yoksa uydurma, "kaynaklarda bulunamadı" de

**Definition of Done**
- 3 farklı PDF (born-digital, çok sütunlu, Türkçe) yüklenip indekslendi
- Bir soruya kaynaklı cevap dönüyor; citation gerçekten doğru sayfayı gösteriyor (elle doğruladım)
- Aynı dosya ikinci kez yüklendiğinde checksum ile parse/embed atlanıyor
- Belgede olmayan bir soruda sistem abstain ediyor

**Kendini test et**
1. Chunk overlap olmasaydı hangi somut soru tipinde hata alırdık?
2. Embedding modelini değiştirirsem mevcut index'e ne olur? Neden?
3. Cosine similarity yüksek ama cevap alakasız olabilir mi? Nasıl?
4. Citation'ı chunk_id yerine sayfa numarasına bağlasaydık ne kaybederdik?

**Yaygın tuzaklar:** chunk metadata'sını eksik bırakıp Faz 3'te eval yazamamak;
embedding'i senkron request içinde yapıp timeout yemek; chunk boyutunu koda gömmek.

**YAPMAYACAKLARIMIZ:** OCR, tablo parsing, sparse retrieval, reranker, agent. Hepsi sonra.

---

## Faz 3 — Eval dataset v0.1 + retrieval eval harness

**Amaç:** "İyi görünüyor" yerine **sayı**. Bu fazdan sonra hiçbir değişiklik ölçülmeden kabul edilmez.

Bu proje aslında burada başlıyor. Faz 2'ye kadar yaptığımız şey herkesin yaptığı "chat with PDF".
Fark buradan itibaren oluşuyor.

**Öğrenilecek kavramlar:** ground truth, relevance judgment, Recall@K, Precision@K, MRR,
DCG/nDCG (log2 discount neden var), Hit Rate, dev/holdout/challenge split mantığı,
overfitting to the test set, dataset versioning (semver), evidence span vs chunk id bağımlılığı.

**Adımlar**

- **3.1** Dataset schema (PRD 12.3) + `evals/datasets/eval-v0.1.json` iskeleti
- **3.2** 40 soruyu **ben** yazarım: 10 factoid, 8 single-doc reasoning, 8 multi-doc karşılaştırma,
  6 multi-hop, 5 no-answer, 3 tablo/sayısal. Her biri için evidence span'ı elle doğrularım.
  → Claude Code burada soru **taslağı** önerebilir ama ground truth'u otomatik kabul etmez.
- **3.3** Split: dev 24 / holdout 10 / challenge 6. Holdout'a tuning sırasında bakılmaz.
- **3.4** Metrik implementasyonları (saf fonksiyon, unit testli): Recall@K, Precision@K, MRR, nDCG@K, HitRate@K
- **3.5** Eval runner: dataset + retrieval config → sonuç; `experiment_id`, `git_sha`, `dataset_version`, `config_hash` ile artifact
- **3.6** İlk baseline ölçümü: R0 (dense-only). Sayıyı `evals/reports/`'a yaz.
- **3.7** Chunk size / overlap sweep: en az 3 kombinasyon, aynı dataset. Sonucu tabloya dök.
- **3.8** Baseline diff aracı: iki experiment'i karşılaştıran CLI çıktısı

**Definition of Done**
- `eval-v0.1` 40 soruyla mevcut, evidence span'ları manuel doğrulanmış
- Metriklerin unit testleri var (elle hesapladığım küçük örneklerle)
- R0 baseline sayıları kayıtlı — **PRD'deki hedeflerle karşılaştırıldı, hedefler değiştirilmedi**
- Chunk config sweep sonucu bir tabloda

**Kendini test et**
1. nDCG'de logaritmik discount neden var? Olmasaydı ne yanlış giderdi?
2. Recall@10 = 1.0 ama nDCG@10 = 0.4 olabilir mi? Bu ne anlama gelir?
3. Challenge set'i tuning'de kullanırsam ne kaybederim — somut olarak?
4. Chunking değiştiğinde `relevant_chunk_ids` neden bozulur, çözümü ne?

**Yaygın tuzaklar:** soruları sistemin zaten cevapladığı şeylerden seçmek (dataset'i kolaylaştırmak);
ground truth'u LLM'e yazdırıp doğrulamamak; baseline'ı kaydetmeyip sonra "daha iyi oldu" diyememek.

**YAPMAYACAKLARIMIZ:** generation eval (Faz 5), LLM-as-judge (Faz 5), agent eval (Faz 6).
Şimdilik sadece **retrieval** ölçülüyor.

---

## Faz 4 — Hybrid retrieval + fusion + reranker

**Amaç:** Faz 3'teki baseline'ı **ölçülebilir şekilde** yenmek. R0 → R1 → R2 → R3.

**Öğrenilecek kavramlar:** lexical/sparse retrieval (BM25, TF-IDF, IDF sezgisi),
dense ve sparse'ın birbirini nerede tamamladığı, skor ölçeklerinin karşılaştırılamazlığı,
rank-based fusion (RRF formülü ve `k` sabiti), normalized fusion,
cross-encoder vs bi-encoder farkı, latency-kalite trade-off'u, deduplication.

**Adımlar**

- **4.1** R1: PostgreSQL full-text search veya BM25 implementasyonu; Türkçe stemming sorunu
- **4.2** R1 ölçümü — dense'in kaçırdığı hangi soruları yakaladı? Örnekleri incele.
- **4.3** R2: Reciprocal Rank Fusion; `k` parametresinin etkisi; alternatif olarak min-max normalize fusion
- **4.4** Deduplication: near-duplicate chunk temizliği
- **4.5** R2 ölçümü + R0/R1 ile diff
- **4.6** R3: cross-encoder reranker (Top-20 → Top-5); latency maliyeti ölçülür
- **4.7** R3 ölçümü; nDCG deltası ve p95 latency artışı birlikte raporlanır
- **4.8** Context packer v1: source coverage, doküman çeşitliliği, sayfa komşuluğu
- **4.9** Retrieval debug kaydı: raw score, fused score, rerank score, final rank
- **4.10** Karar: hangi profil default olacak

**Definition of Done**
- R0-R3 dört konfigürasyon da aynı dataset üzerinde ölçüldü, tek tabloda
- Her adımın **latency maliyeti** de tabloda (kalite tek başına yeterli değil)
- Default retrieval profili gerekçeli olarak seçildi ve kayda geçirildi
- Bir sorgunun retrieval debug çıktısını okuyup neden o sıralamayı aldığını açıklayabiliyorum

**Kendini test et**
1. RRF neden ham skorları toplamaktan daha güvenli?
2. Cross-encoder neden bi-encoder'dan yavaş ama daha iyi?
3. Reranker Recall@10'u değiştirir mi? nDCG@10'u değiştirir mi? Neden farklı?
4. Hybrid her zaman dense'ten iyi mi? Hangi soru tipinde kötüleşebilir?

**Yaygın tuzaklar:** dense ve sparse skorlarını doğrudan toplamak; reranker'ı Top-100'e uygulayıp
latency'yi patlatmak; iyileşmeyi tek örnekle ("bak bu soru düzeldi") ilan etmek.

**YAPMAYACAKLARIMIZ:** query rewrite ve decomposition — onlar agent katmanı (Faz 5).

---

## Faz 5 — Agentic orchestration (LangGraph)

**Amaç:** Tek atışlık RAG'den, kendi çıktısını değerlendiren ve gerektiğinde tekrar deneyen
**kontrollü** bir akışa geçmek.

**Öğrenilecek kavramlar:** explicit state machine vs serbest agent loop, LangGraph node/edge/
conditional edge, state reducer, bounded loop ve neden şart olduğu, context grading,
query rewrite, decomposition, groundedness verification, abstain politikası,
neden ham chain-of-thought kullanıcıya gösterilmez.

**Adımlar**

- **5.1** Graph state modeli (PRD 9.1): `query_original`, `subqueries`, `retrieval_results`,
  `context_quality`, `route`, `answer_draft`, `citations`, `verification`, `trace_id`, `loop_count`
- **5.2** Query Analyzer node: retrieval gerekli mi, karmaşıklık sınıfı ne
- **5.3** Retrieve + Rerank node (Faz 4'ü node haline getirme)
- **5.4** Context Grader node: yeterli mi? — structured output ile, local 9B üzerinde
- **5.5** Conditional edge + `loop_count` guard (max 2) — sonsuz döngü testini bilerek tetikle
- **5.6** Rewrite node (R4) ve ölçümü
- **5.7** Decompose node (R5): multi-hop soruyu alt sorulara bölme, alt sonuçları birleştirme
- **5.8** Generate node: citation contract'ı
- **5.9** Grounding + Citation Verifier node: desteklenmeyen iddiaları yakala → repair veya abstain
- **5.10** Generation eval katmanı: groundedness, citation precision/coverage, no-answer accuracy
- **5.11** LLM-as-judge: farklı provider judge, versionlanmış rubric, %10-20 manuel audit
- **5.12** eval-v0.5'e büyütme (100 soru)
- **5.13** R4/R5/R6 ölçümü ve R3 ile karşılaştırma — **agentic katman gerçekten kazandırdı mı?**

**Definition of Done**
- Graph görselleştirilebiliyor ve her node'un ne yaptığını anlatabiliyorum
- Max loop ihlali sayısı = 0 (test ile kanıtlı)
- No-answer sorularında abstain oranı ölçüldü
- Agentic katmanın kazancı **ve maliyeti** (ekstra LLM çağrısı, latency) birlikte tabloda
- Eğer agentic katman kazandırmıyorsa bu da bir bulgudur ve raporlanır

**Kendini test et**
1. Bounded loop olmasaydı en kötü senaryoda ne olurdu (maliyet + latency)?
2. Context grader'ın kendisi yanılırsa sistem nasıl davranır?
3. LLM-as-judge'ı cevabı üreten modelle aynı yaparsak hangi bias oluşur?
4. Verifier "fail" dediğinde repair mi abstain mi? Karar kuralı ne?

**Yaygın tuzaklar:** her soruyu agentic akıştan geçirip basit sorularda 3 kat latency ödemek;
judge'ı tek gerçek kaynak sanmak; decomposition'ı ölçmeden "daha akıllı" varsaymak.

**YAPMAYACAKLARIMIZ:** model routing (Faz 6). Şu an her node sabit bir modelle çalışıyor.

---

## Faz 6 — Hybrid model router + model benchmark

**Amaç:** Hangi görevin local, hangisinin cloud olduğunu **ölçüye dayanarak** kararlaştırmak.
PRD'nin ana iddiası burada test ediliyor.

**Öğrenilecek kavramlar:** routing policy vs heuristic vs learned classifier, escalation,
composite quality score, Pareto frontier (kalite-maliyet-latency), privacy policy'nin routing'e
önceliği, confidence sinyalinin güvenilmezliği, provider health/rate-limit fallback.

**Adımlar**

- **6.1** Model görev setleri T1-T10 (PRD 16.2): classification, rewrite, decomposition,
  structured extraction, tool calling, relevance grading, grounded answer, multi-hop synthesis,
  verification, Türkçe kalite
- **6.2** Her görev seti için 4B / 9B / OpenAI fast / OpenAI strong / Claude fast / Claude strong ölçümü
- **6.3** Sonuç okuma oturumu: **hangi görevde local yeterli?** Bu tablo router'ın gerekçesi.
- **6.4** Privacy policy enum ve workspace ayarı; `SELF_HOSTED_ONLY` hard-block testi
- **6.5** S0 (local-only) ve S1/S2 (cloud-only) uçtan uca ölçümü — baseline'lar
- **6.6** S3: static hybrid — 6.3'teki tabloya göre sabit eşleme
- **6.7** S4: dynamic hybrid — complexity + schema validity + verifier failure sinyalleri
- **6.8** Escalation reason kaydı ve trace'te görünürlüğü
- **6.9** S0-S4 karşılaştırma raporu: composite quality, cost/100, p50/p95 latency, escalation rate
- **6.10** PRD hipotezinin testi: *hybrid, en iyi cloud-only'nin ≤3 puan altında kalırken
  cloud maliyetini ≥%40 azalttı mı?* — **çıkmadıysa da yazılır, bu bir sonuçtur**

**Definition of Done**
- Beş strateji de aynı dataset ve aynı prompt'larla ölçüldü
- Router kararının gerekçesi her request'te trace'te görünüyor
- Hipotez doğrulandı ya da çürütüldü; hangisi olursa olsun raporlandı
- `SELF_HOSTED_ONLY` altında cloud'a çıkılmadığı testle kanıtlı

**Kendini test et**
1. Composite quality skorunu nasıl tanımladık, ağırlıkları neye göre seçtik?
2. Modelin kendi "confidence" değeri neden tek başına routing sinyali olamaz?
3. Escalation oranı %70 çıksaydı hybrid'in anlamı ne olurdu?
4. Dynamic router'ın static'e göre ek maliyeti ne (ekstra çağrı, karar gecikmesi)?

**Yaygın tuzaklar:** local modeli sadece "ucuz" diye tercih edip kalite düşüşünü ölçmemek;
maliyeti sadece token fiyatıyla hesaplayıp retry maliyetini unutmak;
farklı stratejileri farklı prompt'larla karşılaştırmak (geçersiz benchmark).

---

## Faz 7 — Observability + minimum UI

**Amaç:** Sistemin içini görmek. Debug edilemeyen sistem geliştirilemez.

**Öğrenilecek kavramlar:** trace ağacı ve span, `trace_id` propagation, structured logging,
vendor-neutral trace vs LangSmith, cardinality problemi (neden her şeyi metric yapamayız),
SSE ile streaming, RED metrikleri (Rate, Errors, Duration).

**Adımlar**

- **7.1** Trace modeli (PRD 20.1) ve `model_calls`, `experiments` tablolarına yazma
- **7.2** Structured logging + her log satırında `trace_id`; prompt/PDF içeriği maskeleme
- **7.3** `/v1/traces/{trace_id}` endpoint'i
- **7.4** LangSmith entegrasyonu (opsiyonel, feature flag arkasında)
- **7.5** Next.js iskeleti + Chat ekranı: SSE streaming, citation chip, model badge, latency
- **7.6** Source viewer: citation tıklanınca PDF sayfası + chunk
- **7.7** Traces ekranı: node/tool/model/retrieval timeline
- **7.8** Eval Lab ekranı: dataset seç, experiment çalıştır, metric table, baseline diff
- **7.9** Model Lab ekranı: strateji seç, benchmark, karşılaştırma
- **7.10** Dashboard: doküman/chunk sayıları, son eval skorları, route dağılımı, ort. latency/cost

**Definition of Done**
- Bir sorgunun trace'inden retrieval → model → verifier yolunu okuyabiliyorum
- Citation tıklanınca doğru sayfa açılıyor
- Eval Lab'dan bir experiment başlatıp sonucu ekranda görebiliyorum
- Loglarda ham prompt veya API key yok (elle kontrol edildi)

**Kendini test et**
1. `trace_id` nerede üretilir, hangi katmanlardan nasıl geçer?
2. Neden her retrieval skorunu metric olarak değil, trace olarak saklıyoruz?
3. SSE ve WebSocket arasında neden SSE'yi seçtik?

**Yaygın tuzaklar:** UI'a fazla zaman harcamak (bu bir engineering surface, ürün değil);
trace'i sadece log olarak yazıp sorgulanamaz hale getirmek.

---

## Faz 8 — MCP Server

**Amaç:** Retrieval yeteneklerini standart protokolle dışarı açmak.

**Öğrenilecek kavramlar:** MCP mimarisi (host/client/server), tools vs resources vs prompts ayrımı,
stdio vs Streamable HTTP transport, capability negotiation, scoped token, protocol adapter'ın
core'dan ayrılması.

**Adımlar**

- **8.1** MCP kavram turu: tool / resource / prompt ne zaman hangisi
- **8.2** MCP Python SDK ile server iskeleti, stdio transport (local)
- **8.3** Tools: `search_documents`, `retrieve_chunks`, `get_document_metadata`, `get_source`, `list_collections`
- **8.4** Resources: `rag://collections/{id}`, `rag://documents/{id}`, `.../pages/{page}`
- **8.5** Prompts: `compare_documents`, `extract_evidence`, `answer_with_citations`
- **8.6** Streamable HTTP transport + collection-scope auth + scoped/revocable token
- **8.7** Her MCP request'inin `trace_id` üretmesi
- **8.8** Kabul testi: Claude Desktop (veya başka external MCP host) bu server'a bağlanıp arama yapıyor

**Definition of Done**
- Hem internal agent client hem en az bir **external** MCP host aynı server'ı kullanıyor
- Yetkisiz collection'a erişim denemesi reddediliyor (test ile)
- MCP çağrıları normal API çağrıları gibi trace'te görünüyor

**Kendini test et**
1. Tool ve resource arasındaki fark ne? `get_source` neden tool, `rag://documents/x` neden resource?
2. MCP'yi core retrieval'a gömseydik ne kaybederdik?
3. stdio ve Streamable HTTP'yi hangi senaryoda hangisini seçiyoruz?

---

## Faz 9 — Async queue/worker + AWS deployment

**Amaç:** Sistemi tek makineden çıkarıp production topolojisine taşımak.

**Öğrenilecek kavramlar:** request lifecycle'dan ağır işi ayırma, idempotency, at-least-once
delivery ve sonuçları, visibility timeout, dead-letter queue, retry/backoff, stateless API,
container image, ECS task vs service, ALB health check, IAM least privilege, secret injection.

**Adımlar**

- **9.1** `ingestion_jobs` tablosu + job state machine (queued/processing/indexed/failed)
- **9.2** Local queue (Redis veya SQS-compatible) ile ingestion worker; API sadece enqueue eder
- **9.3** Idempotency: aynı mesaj iki kez gelirse ne olur — bilerek test et
- **9.4** Retry + backoff + dead-letter path
- **9.5** Eval worker: 100+ sample'lık run'ı arka planda çalıştırma
- **9.6** Dockerfile (API + worker), multi-stage build, image boyutu
- **9.7** AWS: S3 bucket (private), RDS PostgreSQL, ElastiCache Redis, SQS
- **9.8** Secrets Manager + IAM rolleri (least privilege — hangi izin neden gerekli)
- **9.9** ECR push + ECS Fargate task/service tanımları (API + worker ayrı)
- **9.10** ALB + health check + staging deploy
- **9.11** CloudWatch log grubu, metrik, en az 2 alarm (5xx oranı, queue backlog)
- **9.12** Maliyet freni: küçük task boyutları, budget alarm, GPU default kapalı

**Definition of Done**
- Staging endpoint ayakta, `/health/ready` doğru cevap veriyor
- 10 paralel PDF upload'ı queue üzerinden işleniyor, worker CPU/RAM izlenebiliyor
- Bir worker'ı bilerek öldürdüm, job kaybolmadı
- CloudWatch'ta trace_id ile bir request'i bulabiliyorum
- Aylık maliyet tahmini yazılı

**Kendini test et**
1. At-least-once delivery neden idempotency'yi zorunlu kılar?
2. Visibility timeout'u işin süresinden kısa ayarlarsak ne olur?
3. Neden GPU inference Fargate'te değil, ayrı compute katmanında?
4. API'nin stateless olması ECS scaling için neden şart?

**Yaygın tuzaklar:** IAM'i `*` ile geçmek; RDS'i public subnet'e koymak;
secret'ı task definition'a plaintext environment olarak yazmak; maliyet alarmı kurmamak.

---

## Faz 10 — CI/CD + regression gates + load test + release

**Amaç:** Sistemi kendini koruyan hale getirmek. Bu faz projeyi "portfolyo"dan
"engineering artifact"a çıkarır.

**Öğrenilecek kavramlar:** quality gate, deterministik vs pahalı test ayrımı, smoke eval,
regression budget, canary/manual approval, rollback stratejisi, load test tasarımı
(concurrency vs RPS), p50/p95/p99 okuma, SLO.

**Adımlar**

- **10.1** GitHub Actions CI: ruff → type check → unit → integration (test container)
- **10.2** Golden retrieval smoke eval: küçük, deterministik, `FakeProvider` ile — her PR'da
- **10.3** Agent/tool schema testleri
- **10.4** Docker build + dependency/security scan + ECR push
- **10.5** Regression gate implementasyonu:
  - Recall@10 baseline'dan >3 puan düşemez
  - nDCG@10 baseline'dan >3 puan düşemez
  - groundedness hedef altına inerse block
  - structured output validity <%99 → fail
  - critical tool schema testleri %100
  - latency/cost regression budget → warning
- **10.6** Gate'i bilerek tetikle: retrieval'ı bozan bir PR aç, pipeline'ın bloklandığını gör
- **10.7** CD: staging deploy → health/smoke → release eval subset → manual approval → prod
- **10.8** eval-v1.0'a büyütme (200 soru); holdout ve challenge sonuçlarını dondurma
- **10.9** Load test: chat light (10), chat mixed (50), burst (100-250), ingestion (10/50), long-doc (500+ sayfa)
- **10.10** SLO karşılaştırması (PRD 18.2) ve sapmaların nedeni
- **10.11** README + architecture doc + benchmark raporları
- **10.12** CV bullet'ları — **sadece ölçülmüş sayılarla** doldurulur

**Definition of Done**
- Bozuk bir PR pipeline tarafından bloklandı (ekran görüntüsü/log kanıtı)
- Load test raporu p50/p95/p99 ile mevcut
- Holdout ve challenge sonuçları dondurulmuş ve commit'li
- README bir yabancının projeyi 5 dakikada anlayabileceği durumda
- CV bullet'larındaki her sayının kaynağı `evals/reports/` içinde bulunabiliyor

**Kendini test et**
1. Hangi testler her PR'da, hangileri nightly? Ayrım kriteri ne?
2. Regression gate eşiğini çok sıkı yaparsak ne olur, çok gevşek yaparsak ne olur?
3. p95 ve p99 arasındaki fark neyi ele verir?

---

## Faz 11 (P2, opsiyonel) — Self-hosted production inference

**Amaç:** Ollama'yı vLLM ile değiştirip aynı logical slot'un gerçekten portable olduğunu kanıtlamak.

**Adımlar**
- **11.1** GPU EC2 + vLLM kurulumu, OpenAI-compatible endpoint
- **11.2** `OpenAICompatibleSelfHostedProvider` — CLAUDE.md Bölüm 5.1 madde 7'nin ("aynı logical slot") testi: kaç satır değişti?
- **11.3** Throughput/latency/maliyet karşılaştırması: vLLM vs Ollama vs cloud
- **11.4** Break-even analizi: hangi hacimde self-hosted cloud'dan ucuz?

**Kendini test et**
1. vLLM'in continuous batching'i throughput'u neden bu kadar değiştiriyor?
2. GPU saatlik maliyeti hesaba katılınca break-even noktası nerede?

---

## Kapanış demo senaryosu (PRD 31)

Proje "bitti" sayılmadan önce **tek oturumda** gösterilebilmeli:

1. 3-5 farklı tip PDF yüklenir; ingestion status ve chunk/index sayısı görünür
2. Basit soru local Qwen'e gider; citation açılır
3. Karmaşık multi-document soru cloud strong'a escalate olur; **neden**i görünür
4. Aynı soru Model Lab'da local-only ve cloud-only ile karşılaştırılır
5. Eval Lab'da dense baseline vs hybrid+reranker farkı Recall/nDCG ile gösterilir
6. No-answer sorusunda sistem abstain eder
7. Trace ekranında retrieval → model → verifier yolu görünür
8. External MCP client search tool'unu çağırır
9. AWS endpoint health + CloudWatch telemetry görünür
10. CI pipeline'da test + eval smoke + Docker build sonucu görünür

---

## İlerleme takibi

| Faz | Konu | Durum | Bitiş tarihi | Ölçülen ana metrik |
|---|---|---|---|---|
| 0 | Zemin | ⬜ | | — |
| 1 | Provider abstraction | ⬜ | | 4B/9B latency, tok/s |
| 2 | Ingestion + baseline RAG | ⬜ | | — |
| 3 | Eval harness + v0.1 | ⬜ | | R0 Recall@10, nDCG@10 |
| 4 | Hybrid + reranker | ⬜ | | R3 vs R0 delta |
| 5 | Agentic orchestration | ⬜ | | groundedness, no-answer acc. |
| 6 | Hybrid router | ⬜ | | S4 vs S1/S2 quality+cost |
| 7 | Observability + UI | ⬜ | | — |
| 8 | MCP | ⬜ | | external client kabul |
| 9 | Queue + AWS | ⬜ | | job success rate, p95 |
| 10 | CI/CD + release | ⬜ | | gate çalıştı mı |
| 11 | vLLM (P2) | ⬜ | | break-even |

---

## Final prensip

> Bu projenin başarısı kaç teknoloji kullandığıyla değil; aynı dataset üzerinde bir değişikliğin
> retrieval, answer quality, agent success, latency ve maliyeti nasıl etkilediğini
> **tekrarlanabilir biçimde kanıtlayabilmekle** ölçülür.
>
> Ve bu proje için ikinci bir ölçüt daha var: her kararı, neden öyle olduğunu anlatarak
> savunabiliyor muyum?
