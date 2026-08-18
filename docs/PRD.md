# Agentic RAG Platformu - Kısaltılmış PRD

PRODUCT REQUIREMENTS DOCUMENT Agentic RAG Platformu Kısaltılmış PRD •
Hybrid Open-Weight + GPT/Claude • Evals • MCP • AWS Alan Değer Doküman
Ürün Gereksinimleri Dokümanı (kısaltılmış sürüm) Kaynak sürüm PRD v1.0
Kaynak tarih 11 Ağustos 2026 Durum Planlama / Uygulama öncesi Amaç
Orijinal kapsamı koruyarak tekrar, aşırı düşük seviye ayrıntı ve şablon
niteliğindeki içerikleri sadeleştirmek. Metodoloji notu: Bu dokümandaki
sayısal kalite, performans ve maliyet eşikleri gerçek benchmark sonucu
değil, başlangıç hedefleri / acceptance criteria'dır. Gerçek sonuçlar
sabitlenmiş eval dataset ve tekrarlanabilir benchmark koşullarıyla
ölçülerek güncellenmelidir. Temel ürün vaadi Herhangi bir doküman
koleksiyonunu güvenilir, kaynaklı ve ölçülebilir bir bilgi sistemine
dönüştürmek; basit görevleri self-hosted modele, karmaşık görevleri
gerektiğinde güçlü cloud modellere yönlendirmek ve sistem kalitesini
eval'lerle kanıtlamak.

# 1.  Ürün Özeti, Vizyon ve Kapsam Agentic RAG Platformu; PDF başta olmak
    üzere doküman koleksiyonlarını yükleyen, parse/chunk/embed/index
    eden, kaynaklara dayalı yanıt üreten, gerektiğinde çok adımlı
    retrieval yapan ve her değişikliğin retrieval, generation, agent
    davranışı, model routing, latency ve maliyet etkisini ölçen
    domain-agnostic bir document intelligence platformudur. Model
    katmanı provider-agnostic tasarlanır: local geliştirmede
    Ollama/open-weight modeller, cloud tarafında OpenAI ve Anthropic;
    production self-hosted senaryosunda aynı arayüz üzerinden vLLM
    benzeri endpoint desteklenir. Ürün sütunu Ne sağlar Nasıl kanıtlanır
    Reliable RAG Hybrid retrieval, reranking, query rewrite,
    decomposition/multi-hop, kaynak doğrulama. Recall/nDCG,
    groundedness, citation metrikleri. Hybrid Model Routing Basit
    görevleri local/self-hosted, zor görevleri cloud modellere
    yönlendirme. Kalite-maliyet-latency karşılaştırması, escalation
    oranı. Production LLMOps Tracing, offline/online eval, regression
    gate, queue/worker, AWS ve CI/CD. Canlı sistem metrikleri, load
    test, deployment pipeline. 1.1 MVP

-   Workspace/collection oluşturma, PDF yükleme ve asenkron ingestion.
-   Dokümanlar üzerinde kaynaklı soru-cevap; gerektiğinde query rewrite,
    decomposition ve tekrar retrieval.
-   Her sorguda model route'u, retrieval sonuçları, agent adımları,
    latency, token ve cost telemetry'si.
-   Eval Lab'da sabit dataset üzerinde retrieval ve answer
    experiment'leri; baseline karşılaştırması.
-   Model Lab'da local-only, cloud-only ve hybrid stratejilerin aynı
    görev setinde benchmark edilmesi.
-   Knowledge MCP Server ile retrieval yeteneklerinin dış istemcilere
    tool/resource/prompt olarak açılması. 1.2 Hedefler ve kapsam dışı
    Hedefler Kapsam dışı (ilk faz) Domain-agnostic kaynaklı QA ve
    karşılaştırma; eval-driven retrieval; kontrollü agentic
    orchestration; hybrid routing; AWS productionization; MCP;
    reproducible benchmarklar. General-purpose multi-agent platformu;
    LLM fine-tuning; her PDF türünde %100 extraction garantisi;
    enterprise DLP/eDiscovery; kapsamlı enterprise billing. 1.3 Öncelik
    modeli Seviye Anlam Örnek P0 MVP için zorunlu. Ingestion, RAG, eval,
    hybrid router, citations. P1 Production ve portföy kalitesini ciddi
    artırır. MCP, queue/worker, AWS, CI/CD regression gate. P2 Stretch /
    sonraki faz. GPU vLLM, advanced OCR, tam IaC.

# 2.  Kullanıcılar ve Temel Senaryolar

-   Knowledge Worker / Analyst: bir veya daha fazla doküman yükler;
    karşılaştırma, özet, factoid ve multi-hop sorular sorar; kaynağı
    açmak ve sistemin gerektiğinde abstain etmesini ister.
-   AI/ML Engineer / Evaluator: chunking, embedding, retriever, reranker
    ve model config experiment'lerini karşılaştırır; trace/tool/route
    kararlarını debug eder; regression gate ile kötüleşen değişiklikleri
    engeller. Senaryo Beklenen çıktı Öncelik Tek PDF factoid Kaynaklı
    kısa cevap + sayfa/chunk referansı P0 Çoklu PDF karşılaştırma
    Multi-source sentez + iddia bazlı P0

citation Belgede olmayan soru Kaynaklarda bulunamadı / abstain P0
Karmaşık multi-hop Decomposition + çoklu retrieval + sentez P0 Eval
experiment Metrikler + baseline diff P0 Local/cloud benchmark
Kalite/latency/cost karşılaştırması P0 MCP client araması Standart MCP
erişimi P1 Büyük batch ingestion Queue/worker ile asenkron işleme P1 3.
Bilgi Mimarisi ve UI/UX UI yalnızca bir demo yüzeyi değil, RAG ve LLM
engineering kararlarını görünür kılan bir engineering product surface
olmalıdır. Önerilen frontend Next.js + Tailwind; streaming için SSE veya
WebSocket kullanılabilir. 3.1 Ana navigasyon ve ekranlar Ekran P0 kapsam
P1/P2 geliştirmeler Dashboard Doküman/chunk sayıları, son eval skorları,
günlük sorgu, ort. latency/cost. Provider kırılımı, hata trendleri, SLA
grafikleri. Knowledge Bases Collections, documents, ingestion jobs;
upload/status/re-index/delete/metadata . Bulk upload, tags, versioning.
Chat / Agent Workspace Streaming yanıt, citation chips, source viewer,
model badge, latency. Agent step timeline, compare mode, feedback. Eval
Lab Dataset seçimi, experiment config/run, metric table, baseline diff.
Failure clustering, sample inspector, export. Model Lab Model/route
stratejisi seçimi, benchmark, sonuç karşılaştırma. Pareto frontier,
provider cost profile. Traces Request'in node/tool/model/retrieval
timeline'ı. Replay, fork, human review. MCP Server status, tool/resource
list, token oluşturma. Client test console. Settings Provider keys,
default model, retrieval config, privacy mode. Org/role yönetimi, quota.
## 3.2 Chat davranışı - Citation tıklanınca sağ panelde ilgili PDF
sayfası/chunk/metadata açılır. - Detaylar alanında route kararı, model,
retrieved/reranked K, token ve end-to-end latency gösterilir. - Agent
adımları ham chain-of-thought olarak değil, güvenli durum etiketleriyle
gösterilir (örn. sorgu yeniden yazıldı, kaynaklar tarandı). - Yetersiz
kanıtta sistem tahmin üretmez; abstain eder ve mümkünse eksik bilgi
türünü belirtir. 4. Fonksiyonel Gereksinimler Grup Zorunlu yetenekler
Workspace & ingestion Collection oluşturma; PDF upload;
queued/processing/indexed/failed status; chunk +
page/section/source/checksum metadata; async job. Retrieval & answer
Dense + lexical/sparse hybrid retrieval; reranking; context yetersizse
rewrite/decomposition; claim-source citations. Models & routing
Ollama/OpenAI/Anthropic/self-hosted aynı logical interface; policy +
complexity + failure sinyalli router. Evaluation & tracing
Dataset+config ile experiment;

request/tool/retrieval/model/token trace. P1 MCP server; ingestion/eval
queue-worker; CI/CD quality gate. P2 Production self-hosted open-weight
inference endpoint (vLLM benzeri). 5. Ingestion, Retrieval ve Agentic
RAG Mimarisi 5.1 Ingestion Tek parser yaklaşımı yerine adapter tabanlı
pipeline kullanılacaktır: Upload checksum/type validation parser router
clean/normalize page/section segmentation chunking metadata -\> -\> -\>
-\> -\> -\> embedding index quality checks -\> -\> -\> - Parser router:
native text; scanned PDF için OCR fallback; table/layout-aware fallback
P1/P2. - Test corpusu born-digital, multi-column, table-heavy, scanned,
mixed, 100--500+ sayfalık uzun ve Türkçe/İngilizce PDF'leri kapsar. -
Chunking baseline recursive token/character + overlap;
section/page-aware alternatifleri benchmark edilir. Chunk size/overlap
Eval Lab parametresidir. - Chunk metadata en az document_id, page range,
section title, index, checksum, language ve parser_version içerir. 5.2
Retrieval Query normalize dense + lexical/sparse fusion Top-N reranker
Top-K context context packer LLM/Agent -\> -\> -\> -\> -\> -\> -\> -\> -
Retrieval experiment ailesi dense-only, sparse-only, hybrid,
hybrid+reranker, query rewrite, multi-query/decomposition ve conditional
agentic retrieval katmanlarını sırayla karşılaştırır. - Fusion için
rank-based/normalize edilmiş yöntemler denenir; duplicate chunk'lar
temizlenir; context packer token budget, kaynak çeşitliliği, sayfa
komşuluğu ve source coverage'ı dikkate alır. - Debug için
raw/fused/rerank score ve final rank saklanır. 5.3 Agentic orkestrasyon
Policy & Complexity Router Query Analyzer Retrieve + Rerank Context
Grader gerekirse Rewrite/Decompose + tekrar -\> -\> -\> -\>

retrieval Generate Grounding/Citation Verifier repair veya abstain -\>
-\> -\> - LangGraph benzeri explicit-state graph; sınırsız loop yok.
Başlangıç max retrieval loop = 2. - State: original/normalized query,
subqueries, retrieval results, context quality, route, answer draft,
citations, verification, trace_id, loop_count. - Guardrails: bounded
retries, tool schema validation, insufficient evidence'de abstain,
sensitive workspace'te cloud escalation yasağı, minimum telemetry ve
kullanıcıya ham reasoning göstermeme. 6. Hybrid Model Stratejisi ve
Router Amaç local modelin her şeyi yapması değil; mümkün olan görevlerde
küçük/ucuz/gizli modeli kullanıp kalite riski yükseldiğinde cloud modele
escalation yapmaktır. Ortam / slot Yaklaşım Local development Ollama;
başlangıç adayları Qwen3.5 4B Q4 (\~3.4 GB) ve 9B Q4 (\~6.6 GB). gpt-oss
20B (\~14 GB) yalnız deneysel stres testi. Cloud OPENAI_FAST /
OPENAI_STRONG ve ANTHROPIC_FAST / ANTHROPIC_STRONG logical slotları;
exact model ID config/database'den gelir. AWS prod Ana uygulama ECS
Fargate; P2'de ayrı GPU/vLLM inference endpoint. Privacy mode Sadece
self-hosted; doküman içeriği üçüncü taraf API'ye

çıkmaz. 6.1 Başlangıç görev politikası Görev Default Escalation
Classification / metadata extraction Local 4B/9B Schema invalid / düşük
confidence. Query rewrite / relevance grading / tool selection Local 9B
Düşük eval skoru, karmaşık dil, high- stakes, tool-call failure. Simple
grounded answer Local 9B Uzun/çelişkili context veya verifier fail.
Multi-hop synthesis Cloud strong SELF_HOSTED_ONLY policy varsa
local/self-hosted. Final verifier / offline judge Tercihen farklı
provider güçlü model Privacy/maliyet politikası; human audit ile
kalibrasyon. 6.2 Routing girdileri ve stratejiler - Privacy policy;
query complexity; context size/doküman sayısı; beklenen tool/agent
depth; local structured- output başarısı; verifier sonucu; provider
health/rate-limit; budget/latency preference. - Benchmark stratejileri:
S0 local-only, S1 OpenAI-only, S2 Claude-only, S3 static hybrid, S4
dynamic hybrid (hedef production). - Dynamic router özeti:
SELF_HOSTED_ONLY ise self-hosted; basit kısa görevlerde önce local;
multi-hop/verifier failure/conflicting context'te cloud strong; diğer
durumda cloud fast. - Başlangıç hypothesis'i: hybrid, en iyi cloud-only
composite quality skorunun en fazla 3 puan altında kalırken cloud
maliyetini en az %40 azaltmayı hedefler. 7. Eval ve Benchmark Sistemi
Eval yaklaşımı ürünün merkezindedir. Retrieval, final cevap, agent
trajectory, model routing ve sistem performansı ayrı ama aynı
versionlanmış experiment metadata'sıyla ölçülür. 7.1 Eval dataset Split
Adet Kullanım Dev Chunking/retrieval/prompt/router tuning. Holdout Karar
ve raporlama; tuning sırasında cevaplar görülmez. Challenge Adversarial,
no-answer, conflicting source, zor multi-hop. - Toplam hedef 200 soru.
Kategoriler: factoid, single-doc reasoning, multi-document comparison,
multi-hop, ambiguous, no-answer, conflicting sources, table/numeric. -
Her sample'da question/language/category/answerable/expected
answer/evidence/source refs/expected route-tools/difficulty gibi alanlar
bulunur. - Ground truth manuel doğrulanır; source-span tabanlı kanıt
korunur; dataset semver ile versionlanır; challenge set tuning'de
optimize edilmez. 7.2 Retrieval, generation ve agent metrikleri Katman
Ana metrikler / ilk hedefler Retrieval Recall@10 hedef 0.90, nDCG@10
0.82; ayrıca Recall@5, ≥ ≥ MRR, HitRate@5, Precision@K. Baseline ve
stretch eşikleri corpus sonrası kalibre edilir. Generation Groundedness
0.90, citation precision 0.95, citation ≥ ≥ coverage 0.90, no-answer
accuracy 0.90, structured ≥ ≥

output validity 0.99. ≥ Agent Route accuracy 0.92; tool selection 0.95;
tool argument ≥ ≥ validity 0.98; task success 0.90; unnecessary tool
call ≥ ≥ 0.10; max loop violation = 0; routine escalation 0.35 ≤ ≤
hypothesis. - LLM-as-judge tek gerçek kaynak değildir: mümkünse farklı
provider judge, versionlanmış rubric ve release benchmarkında %10--20
manual audit kullanılır; deterministik metrik varsa öncelik ondadır. 7.3
Model ve component benchmarkları - Model görev setleri: classification,
query rewrite, decomposition, structured extraction, tool calling,
relevance grading, grounded answer, multi-hop synthesis, verification ve
Türkçe kalite. - Performans: TTFT, total latency, prompt/gen throughput,
cold/warm load, peak memory/swap, token usage ve cost. - Benchmark
protokolü: deterministik ayar, aynı prompt/tool schema/context,
stochastic örneklerde tekrar ve median/p95, exact
model/quantization/context/hardware/timestamp kaydı, git SHA +
prompt/dataset/config version. - Embedding: retrieval quality +
index/query latency + storage; dil bazlı skor. Reranker: no-reranker vs
cross- encoder/opsiyonel LLM reranker. Parser/OCR: text coverage,
reading order, page mapping, Unicode integrity, downstream QA,
throughput, failure rate. 7.4 Sistem/load benchmarkı ve cache Senaryo
Örnek yük / ölçüm Chat light 10 concurrent; RPS, p50/p95/p99, error.
Chat mixed 50 concurrent; route, latency, queue, DB pool. Burst 100--250
kısa süreli; rate limit/fallback. Ingestion 10/50 paralel PDF; queue
depth, pages/min, worker resource. Eval batch 200 sample; süre,
rate-limit, cost. Long-doc 500+ sayfa; memory, retry/resume, indexing
duration. - Başlangıç SLO'lar: non-LLM API p95 \<300 ms; cloud simple
chat p95 \<6 s; local simple M1 target p95 \<15 s; enqueue \<1 s; retry
sonrası job success 99%; 5xx \<1%; citation source open p95 \<1 s. ≥ -
Cache: checksum, embedding, güvenli/version-aware retrieval cache; LLM
response cache varsayılan kapalı veya exact config/hash ile. 8. MCP
Tasarımı MCP, retrieval yeteneklerini bağımsız agent istemcilerine
taşıyan gerçek entegrasyon katmanıdır. - Transport: localde stdio
mümkün; remote/staging için Streamable HTTP tercih edilir. MCP ayrı
servis veya FastAPI deployment içinde ayrı route/process olabilir. -
Tools: search_documents, retrieve_chunks, get_document_metadata,
get_source, list_collections, P1 compare_sources. - Resources:
collection, document ve document/page URI'ları. Prompts:
compare_documents, extract_evidence, answer_with_citations. - Kabul:
internal agent client + en az bir external MCP host/client;
collection-scope auth; her request için trace_id.

# 9.  Observability, Veri Modeli ve API 9.1 Trace ve telemetry

-   Trace ağacı route decision, rewrite, dense/sparse retrieval, rerank,
    LLM calls, tool calls, verification ve final response'u bağlar.
-   Kaydedilir: request/workspace/status; exact
    model/prompt/tokens/latency/cost/retry; retrieval strategy/scores;
    agent path/tool/loop/escalation; eval version/config/judge/metrics;
    CPU-memory/queue/DB pool/error/worker duration.
-   Araç yaklaşımı: LangSmith opsiyonel; CloudWatch AWS
    log/metric/alarm; vendor-neutral trace_id; PostgreSQL experiment
    metadata. 9.2 Veri modeli ve depolama
-   Ana entity'ler: users, workspaces, collections, documents, chunks,
    conversations/messages, eval_datasets/samples, experiments/results,
    model_calls, ingestion_jobs, secret references.
-   S3: orijinal doküman ve durable artifacts; PostgreSQL/RDS:
    metadata/auth/experiments/trace summary; vector store: Qdrant veya
    pgvector benzeri; Redis: short-lived cache/rate-limit/state; SQS:
    ingestion/eval queue.
-   Secret değerleri DB'de plaintext tutulmaz. 9.3 API yüzeyi
-   Collection/document lifecycle:
    create/list/upload/status/reindex/delete.
-   Chat: query + streaming; response answer, citations,
    route/provider/model/reason, trace_id, latency ve usage/cost içerir.
-   Evals: run/status/compare; model benchmark run/status; trace fetch;
    health live/ready; P1 /mcp endpoint. Orijinal PRD'deki endpoint
    isimleri ve request/response JSON örnekleri implementasyon referansı
    olarak korunabilir; kısaltılmış ana PRD'de kontrat seviyesi
    yeterlidir.

# 10. AWS Deployment ve CI/CD 10.1 Production topology Internet
    CloudFront/Frontend ALB ECS Fargate FastAPI RDS + Redis + S3 +
    Vector Store + Secrets Manager + -\> -\> -\> -\> CloudWatch + SQS
    ECS Worker(s) -\>

-   P2: API open-weight inference gateway GPU EC2/vLLM; cloud
    providerlar paralel seçenek olarak kalır. -\> -\>
-   ECS Fargate API/worker container'larını server yönetmeden ölçekler;
    GPU inference ayrı compute katmanıdır.
-   Environment'lar: local (Ollama + optional cloud), test (mock/fake
    provider + deterministic tests), staging (cloud + optional
    self-hosted + smoke eval), prod (policy-driven routing + managed
    secrets). 10.2 CI/CD ve regression gate
-   CI: lint/type checks unit integration küçük deterministic retrieval
    eval agent/tool schema tests

-\> -\> -\> -\> -\> Docker build security/dependency scan ECR. -\> -\> -
CD: staging deploy health/smoke release eval subset başlangıçta manual
approval ECS prod post- -\> -\> -\> -\> -\> deploy monitor/rollback. -
Gate örnekleri: Recall@10 veya nDCG@10 baseline'dan \>3 puan düşemez;
groundedness hedef altına inerse block; structured output \<99% fail;
critical tool schema testleri %100; latency/cost regression budget; no-
answer challenge eşiği. 11. Güvenlik, Gizlilik, NFR ve Test Privacy
policy Davranış

SELF_HOSTED_ONLY Doküman/sorgu cloud API'ye gönderilmez. HYBRID_REDACTED
Cloud escalation öncesi yalnız gerekli excerpt ve mümkünse PII
redaction. HYBRID Router kalite/maliyet politikasına göre cloud
kullanabilir. CLOUD_ONLY Local disabled; cloud providerlar arasında
seçim. - JWT/session auth ve workspace-scoped authorization; her
document/query erişiminde ownership kontrolü. - Private S3 + kısa ömürlü
presigned URL; Secrets Manager/env injection; API key plaintext
loglanmaz. - Raw PDF/full prompt logging varsayılan minimize/masked;
file type/size validation ve malware scan hook. - Rate limit/quota;
delete işlemi DB + vector + object storage cleanup; MCP tokenları
scoped/revocable. - NFR: idempotent/retryable background jobs, stateless
API, horizontal workers, traceability, adapter portability,
reproducibility, least privilege, cost control, TR/EN Unicode,
typed/modular maintainability. 11.1 Test stratejisi - CI: unit
(chunking/fusion/router/cost), schema/contract, integration, golden
retrieval subset, security ve UI E2E. - Nightly/release: full 200-sample
offline eval. Release öncesi load test. P1: MCP interoperability ve
worker/provider failure/retry/redrive testleri. 12. Başarı Metrikleri
Metrik MVP hedef Recall@10 0.90 ≥ nDCG@10 0.82 ≥ Groundedness 0.90 ≥
Citation precision 0.95 ≥ No-answer accuracy 0.90 ≥ Tool argument
validity 0.98 ≥ Structured output validity 0.99 ≥ Hybrid quality delta
Best cloud-only'e göre 3 puan kayıp hedefi ≤ Hybrid cloud cost reduction
Cloud-only'e göre %40 hypothesis ≥ Critical regression Release sırasında
0 critical regression - Public demo kullanım metrikleri: upload success,
query success/abstain, citation open rate, median/p95 latency,
local/cloud route dağılımı ve successful answer başına cost. 13.
Roadmap, Riskler ve Demo Kabulü 13.1 8 haftalık core roadmap Hafta Ana
hedef Definition of Done Local LLM + provider abstraction Ollama 4B/9B,
structured/tool calling, benchmark collector, OpenAI/Anthropic adapters.
Ingestion + baseline RAG Upload, async-ish job, parser, chunks,
embedding, dense retrieval, citations. Eval dataset + retrieval suite
Eval v1 seed, Recall/MRR/nDCG, R0--R3, baseline dashboard. Agentic RAG
Router/retrieval/grader/rewrite/ decompose/verifier; bounded loops.
Hybrid router + model benchmark S0--S4; task suites;
quality/cost/latency reports. MCP + observability + UI polish Remote
MCP, traces, Eval Lab, Model Lab, source viewer.

AWS productionization S3/SQS/RDS/Redis/ECS API-worker, CloudWatch,
secrets, staging. CI/CD + load + release Regression gates, load test,
docs, architecture, public demo. 9+ P2 self-hosted cloud inference GPU
EC2 + vLLM; OpenAI-compatible endpoint ve cost benchmark. - Her
milestone çalışan artifact + ölçülebilir çıktı üretir; README/ADR
güncellenir; yeni özellik en az bir eval/test ile ölçülür; public
release öncesi holdout/challenge sonuçları dondurulur. 13.2 Ana riskler
Risk Azaltma Scope creep P0/P1/P2 sınırı; multi-agent ayrı proje. Local
model kalite/memory Hybrid escalation, task-specific local usage, 4B
fallback, context cap, benchmark. PDF parser edge cases Adapter + OCR
fallback + corpus sınıf benchmarkı. LLM judge bias Cross-provider
judge + human audit. Cloud/AWS maliyeti Subset, caching, fast model,
budget caps, small/on-demand compute; GPU default off. Provider API
churn Provider abstraction + config-driven exact model IDs. Ground truth
/ benchmark noise Manual evidence validation, holdout review, repeated
runs, exact config logging. Security leakage Privacy policy, log
minimization, secrets, auth scope. 13.3 Demo / portföy kabul
senaryosu 1. 3--5 farklı tip PDF yükle; ingestion status ve chunk/index
sayısı görünsün. 2. Basit soru local Qwen route'una gitsin ve citation
açılsın. 3. Karmaşık multi-document soru cloud strong'a escalate olsun;
nedeni görünsün. 4. Aynı soru local-only/cloud-only ile Model Lab'da
karşılaştırılsın. 5. Eval Lab'da dense baseline ile hybrid+reranker
farkı Recall/nDCG ile gösterilsin. 6. No-answer örneğinde sistem abstain
etsin. 7. Trace ekranında retrieval model verifier path'i görülsün. -\>
-\> 8. External MCP client search tool'u çağırsın. 9. AWS endpoint
health + CloudWatch telemetry gösterilsin. 10. CI pipeline'da test +
eval smoke + Docker build sonucu gösterilsin. 14. Backlog, ADR ve Repo
Yapısı 14.1 Backlog - P1: document versioning/re-index diff; user
feedback eval candidate; online eval sampling; source-level -\> access
control; MCP playground; batch comparison/report export; advanced
table-aware extraction. - P2: GPU EC2 + vLLM; Terraform/CDK tam IaC;
multimodal PDF understanding; learned/dynamic router classifier; context
compression/memory optimization; reranker serving optimization; tenant
billing/quotas; multi-region/DR. 14.2 Temel teknik kararlar (ADR) ADR
Karar / gerekçe Provider abstraction zorunlu --- model/provider churn ve
benchmark karşılaştırılabilirliği. Eval dataset feature'dan önce ---
iyileşmeyi objektif ölçmek. Agent loops bounded --- reliability, maliyet
ve debug.

MCP ayrı protocol adapter --- core retrieval'den protocol bağımlılığını
ayırmak. Async ingestion --- büyük PDF işini request lifecycle'dan
ayırmak. Cloud model IDs config-driven --- provider değişikliklerine
dayanıklılık. Local/prod self-hosted aynı logical slot --- Ollama vLLM
-\> geçişini kolaylaştırmak. Benchmark sonuçları artifact ---
reproducibility ve portföy kanıtı. 14.3 Önerilen repo iskeleti
agentic-rag-platform/ apps/ \# api (FastAPI), web (Next.js) ├─ packages/
\# ingestion, retrieval, agents, providers, evals, mcp_server,
observability ├─ workers/ \# ingestion_worker, eval_worker ├─ evals/ \#
datasets, rubrics, reports ├─ infra/ \# docker, terraform (P2/late P1)
├─ tests/ \# unit, integration, e2e ├─ docs/ \# architecture, adr,
benchmarks ├─ .github/workflows/ ├─ README.md └─ 14.4 Benchmark artifact
metadata - Her run en az experiment_id, git_sha, dataset/prompt/router
version, retrieval profile, embedding/reranker, provider+exact model id,
quantization/context, hardware ve timestamp ile ilişkilendirilir. -
Raporlar retrieval, end-to-end route quality/cost/latency ve local
inference (cold load, TTFT, throughput, p50/p95, peak memory/swap)
tablolarını üretir. - Resmi teknik kaynaklar olarak Ollama
capabilities/model docs, LangGraph docs, MCP Python SDK, Anthropic MCP,
OpenAI Responses/tools/structured outputs ve AWS ECS/Fargate
dokümantasyonu referans alınır; hızlı değişen model ID/fiyatlar
implementasyon sırasında yeniden doğrulanır. Final prensip: Başarı
kullanılan teknoloji sayısıyla değil, aynı dataset üzerinde bir
değişikliğin retrieval, answer quality, agent success, latency ve
maliyeti nasıl etkilediğini tekrarlanabilir biçimde kanıtlayabilmekle
ölçülür.
