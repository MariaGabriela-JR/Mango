# Fluxo de Tratamento e Filtragem de Dados EEG

Este documento descreve os passos para tratamento, filtragem e seleção de pacientes usando os módulos `core.filters` e a API `filters_api`.

---

## 1. Descoberta de arquivos EDF

- **Endpoint:** `GET /discover`
- **Descrição:** Lista todos os arquivos `.edf` presentes na pasta base (`EDF_CONTAINER_PATH` definida no `.env`).
- **Validação:** Garante que a pasta base existe; caso contrário, retorna erro HTTP 500.
- **Retorno:** JSON com:
  - `file_name`: nome do arquivo
  - `file_path`: caminho completo
  - `exists_on_disk`: `true` se arquivo existe

---

## 2. Carregamento e pré-processamento

- **Função:** `validate_and_preprocess(file_path)`  
- **Descrição:** Carrega o arquivo `.edf` e realiza validação básica.
- **Erros possíveis:**  
  - `EDFValidationError` → arquivo inválido, retorna HTTP 400.
  - Qualquer outra exceção → erro inesperado, retorna HTTP 500.

---

## 3. Estratégias de filtragem

### 3.1 Raw (sem filtro)

- **Função:** `raw_filter(raw)`  
- **Comportamento:** Retorna os dados crus sem aplicar filtros.
- **Uso na API:** `mode="raw"`

### 3.2 Standard (filtro padrão)

- **Filtros aplicados:**  
  - Passa-banda: 1–40 Hz  
  - Notch: 50 Hz  
- **Uso na API:** `mode="standard"`

### 3.3 Custom (filtro manual)

- **Função:** `custom_filter(raw, config)`  
- **Configuração típica:**
```json
{
    "highpass": 1.0,
    "lowpass": 40.0,
    "notch": [50, 60]
}
```

- **Uso na API:** `mode="custom"` com parâmetros opcionais `l_freq`, `h_freq` e `notch`.

### 3.4 Auto (baseado em metadados do paciente)

- **Função:** `auto_filter(raw, patient_metadata, trial_metadata)`
- **Regras exemplares:**
  - Experimento `resting_state` → passa-banda 0.5–45 Hz + notch 50/60 Hz
  - Sessão `sleep` → passa-baixa 30 Hz
  - Paciente menor de 18 anos → passa-banda 1–40 Hz
  - Caso padrão → passa-banda 0.5–50 Hz
- **Uso na API:** `mode="auto"` (padrão)
- **Metadados necessários:**
  - `patient_metadata`: idade, sexo, etc.
  - `trial_metadata`: tipo de experimento, sessão, etc.

---

## 4. Salvando resultados

- **Diretório de saída:** definido por `OUTPUT_CONTAINER_PATH` no `.env`
- **Subpasta:** nome do paciente (`file_name.split('_')[0]`)
- **Nome do arquivo final:** `{stem}_filtered.fif`
- **Exemplo:** `output/Paciente01/sub-01_task-emotion_eeg_filtered.fif`

---

## 5. Resumo do fluxo completo

1. Descobrir arquivos EDF.
2. Carregar e validar EDF.
3. Selecionar modo de filtragem (`raw`, `standard`, `custom`, `auto`).
4. Aplicar filtros com base em parâmetros ou metadados.
5. Criar pasta de saída (se não existir).
6. Salvar arquivo filtrado.
7. Retornar JSON com informações do arquivo, número de canais e duração.

