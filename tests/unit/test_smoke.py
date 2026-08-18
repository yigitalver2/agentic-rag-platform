"""Faz 0 smoke test: pytest'in gerçekten çalıştığını doğrular.

Bu test hiçbir iş mantığını sınamıyor — amacı sadece test altyapısının
(discovery, çalıştırma, raporlama) doğru kurulduğunu kanıtlamak.
"""


def test_pytest_altyapisi_calisiyor() -> None:
    assert 1 + 1 == 2
