# Migração para Streamlit - e-Stress2D

## Como rodar o aplicativo Streamlit

A migração do notebook marimo para Streamlit foi concluída! 

### Instalação

```bash
# Instalar dependências (já configurado no pyproject.toml)
uv sync
```

### Executar o Streamlit

```bash
# Rodar a aplicação Streamlit
streamlit run app_streamlit.py
```

Ou, alternativamente:

```bash
# Com Python virtual environment (se necessário)
python -m streamlit run app_streamlit.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

## Principais mudanças da migração

### De Marimo para Streamlit

1. **Layout**: Convertido de células marimo para aplicativo linear Streamlit
2. **Inputs**: Inputs de marimo (`mo.ui.number()`) convertidos para `st.number_input()` na sidebar
3. **Display**: `mo.md()` convertido para `st.markdown()`
4. **Métrica/Resultados**: Dados exibidos com `st.metric()` para melhor visualização
5. **Gráficos**: Matplotlib plots exibidos com `st.pyplot()`
6. **Interatividade**: Implementado `st.session_state` para manter valores entre reruns
7. **Botão de aleatoriedade**: Adicionado botão "Gerar valores aleatórios" na sidebar

### Estrutura do app Streamlit

- **Sidebar**: Contém inputs de σ_xx, σ_yy, σ_xy e botão para gerar valores aleatórios
- **Aba Equacionamento**: Expandível, contém as fórmulas matemáticas
- **Aba Unidades**: Expandível, com observações sobre homogeneidade de unidades
- **Resultados**: Métricas exibidas em colunas para melhor organização visual
- **Gráficos**: Três gráficos matplotlib exibidos em sequência

## Funcionalidades mantidas

✓ Cálculo de tensões principais (σ_1, σ_2)  
✓ Cálculo de tensão média (σ_med)  
✓ Cálculo de raio de Mohr (R)  
✓ Cálculo de ângulos principais (θ_1, θ_2)  
✓ Três representações gráficas planificadas:
  - Estado de tensões cartesiano
  - Elementos com tensões principais
  - Elementos com tensões de cisalhamento extremas

## Notas adicionais

- Todas as funcionalidades do marimo foram preservadas
- A interface é mais responsiva e adequada para web
- Os cálculos matemáticos permanecem idênticos
- Matplotlib figures são fechadas após exibição para otimizar memória
