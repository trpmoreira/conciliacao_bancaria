# Adicionar no início do arquivo junto com os outros mapeamentos
-- Tabela de configuração de bancos
CREATE TABLE bancos (
    id INTEGER PRIMARY KEY,
    nome_banco TEXT NOT NULL,
    nome_conta TEXT NOT NULL,
    conta_phc TEXT NOT NULL,
    nome_folha TEXT NOT NULL,
    codigo_banco TEXT NOT NULL
);

-- Tabela para armazenar os movimentos do PHC
CREATE TABLE phc_movimentos (
    id INTEGER PRIMARY KEY,
    data TEXT NOT NULL,
    numero_doc TEXT NOT NULL,
    descricao TEXT,
    valor REAL NOT NULL,
    conta_phc TEXT NOT NULL,
    nome_conta_phc TEXT NOT NULL,
    ano_mes TEXT NOT NULL,
    banco_id INTEGER,
    processado INTEGER DEFAULT 0,
    FOREIGN KEY (banco_id) REFERENCES bancos (id)
);

-- Tabela para armazenar os extratos bancários
CREATE TABLE banco_extratos (
    id INTEGER PRIMARY KEY,
    nome_conta TEXT NOT NULL,
    data TEXT NOT NULL,
    descricao TEXT,
    valor REAL NOT NULL,
    codigo_mecanografico TEXT,
    ano_mes TEXT NOT NULL,
    banco_id INTEGER NOT NULL,
    processado INTEGER DEFAULT 0,
    FOREIGN KEY (banco_id) REFERENCES bancos (id)
);

-- Tabela para armazenar os movimentos conciliados
CREATE TABLE movimentos_conciliados (
    id INTEGER PRIMARY KEY,
    nome_conta TEXT NOT NULL,
    codigo_mecanografico TEXT NOT NULL,
    valor_banco REAL,
    valor_phc REAL,
    diferenca REAL,
    ano_mes TEXT NOT NULL,
    banco_id INTEGER NOT NULL,
    FOREIGN KEY (banco_id) REFERENCES bancos (id)
);

-- Tabela para armazenar os movimentos com documento inválido
CREATE TABLE movimentos_invalidos (
    id INTEGER PRIMARY KEY,
    nome_conta TEXT NOT NULL,
    numero_doc TEXT NOT NULL,
    descricao TEXT,
    data TEXT NOT NULL,
    valor REAL NOT NULL,
    ano_mes TEXT NOT NULL,
    banco_id INTEGER NOT NULL,
    motivo TEXT NOT NULL,
    FOREIGN KEY (banco_id) REFERENCES bancos (id)
);

-- Tabela para armazenar o resumo de saldos
CREATE TABLE resumo_saldos (
    id INTEGER PRIMARY KEY,
    banco TEXT NOT NULL,
    saldo_phc REAL NOT NULL,
    saldo_banco REAL NOT NULL,
    diferenca REAL NOT NULL,
    ano_mes TEXT NOT NULL,
    banco_id INTEGER NOT NULL,
    FOREIGN KEY (banco_id) REFERENCES bancos (id)
);

-- Tabela para controlo de processamento
CREATE TABLE status_processamento (
    id INTEGER PRIMARY KEY,
    ano_mes TEXT NOT NULL,
    banco_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (banco_id) REFERENCES bancos (id),
    UNIQUE(ano_mes, banco_id)
);