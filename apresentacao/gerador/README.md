# Gerador da apresentação

Gera o `.pptx`, o `roteiro.md` e o PDF do roteiro a partir de uma fonte só, para que não divirjam.

| Arquivo | O que faz |
|---|---|
| `roteiro.json` | A fonte: título, tempo, palavras-chave, fala, cuidado e passe de cada slide, mais as perguntas da banca |
| `gerar.py` | Gera o `.pptx` (python-pptx), com a fala nas notas do apresentador. A lista de referências vem de `artigo/referencias.md` |
| `gerar_roteiro_md.py` | Gera `../roteiro.md` e `../README.md` |
| `gerar_pdf.py` | Gera o PDF do roteiro (reportlab, página A5). Usa a fonte Arial; aponte `FONTES` para a pasta dela fora do Windows |

```bash
pip install python-pptx reportlab
python apresentacao/gerador/gerar.py apresentacao/apresentacao-sdcac.pptx
python apresentacao/gerador/gerar_roteiro_md.py
python apresentacao/gerador/gerar_pdf.py apresentacao/roteiro-filipe.pdf
```

**Para mudar um texto**, mude o `roteiro.json` (fala e notas) e, se o texto aparece no slide, o `gerar.py`. Gere os três arquivos de
novo. Não edite o `.pptx` ou o PDF à mão, porque a próxima geração desfaz a edição.

O `.pptx` foi conferido abrindo-o no PowerPoint 2007 e renderizando os slides. Os scripts não rodam no CI.
