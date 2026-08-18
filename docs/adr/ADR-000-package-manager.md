# ADR-000: Python paket yöneticisi olarak uv seçimi

## Bağlam
Proje çok sayıda Python paketi (`packages/*`, `apps/api`, `workers/*`) içeren bir monorepo.
Faz 1-6 boyunca provider SDK'ları (openai, anthropic), LangGraph, embedding/rerank
kütüphaneleri gibi bağımlılıklar sık sık eklenip çıkarılacak. Deterministik, hızlı ve
CI'da güvenilir bir bağımlılık çözümleme mekanizması gerekiyor.

## Karar
Paket yöneticisi olarak **uv** kullanılacak. `pyproject.toml` + `uv.lock` ile bağımlılıklar
yönetilecek. Kök `pyproject.toml`, `tool.uv.package = false` ile "kurulabilir paket" değil,
"workspace kökü" olarak işaretlendi — asıl kod `packages/` ve `apps/` altındaki alt
paketlerde yaşayacak (bu paketler ileriki fazlarda kendi `pyproject.toml`'larıyla eklenecek).

## Alternatifler
- **Poetry**: Olgun, geniş ekosistem desteği, entegre sanal ortam ve lock dosyası.
  Dezavantajı: bağımlılık çözücüsü (resolver) uv'ye göre gözle görülür yavaş; büyüyen
  bağımlılık ağacında (bu projede olacağı gibi) `poetry add`/`poetry lock` süreleri artar.
- **pip + requirements.txt**: En tanıdık, ekstra araç gerektirmez. Dezavantajı: deterministik
  lock yok (transitive bağımlılık versiyonları makineler arası kayabilir), sanal ortam
  yönetimi ayrı komutlarla (`venv`) yapılmak zorunda — proje tanımıyla bağlı değil.

## Sonuçlar
**Olumlu:** hızlı bağımlılık çözümü ve kurulum; `pip`-uyumlu arayüz sayesinde pip
deneyiminden geçiş küçük; tek `uv.lock` ile reproducibility.
**Olumsuz:** uv, Poetry kadar uzun süredir "battle-tested" değil; bazı nadir edge-case'lerde
(örn. çok özel build backend'leri) ekosistem desteği daha ince olabilir. Bu projenin
bağımlılık profili (yaygın PyPI paketleri) için bu risk düşük görülüyor.

## Durum
Kabul edildi, 2026-08-18.
