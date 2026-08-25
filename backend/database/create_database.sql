CREATE DATABASE IF NOT EXISTS momentus_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE momentus_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(160) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    telefone VARCHAR(40) DEFAULT '',
    senha_hash VARCHAR(255) NOT NULL,
    tipo VARCHAR(30) NOT NULL DEFAULT 'cliente',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_usuario_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fornecedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    nome_empresa VARCHAR(180) NOT NULL,
    cpf_cnpj VARCHAR(30) NOT NULL UNIQUE,
    tipo_servico VARCHAR(100) NOT NULL,
    descricao TEXT,
    cidade VARCHAR(120) DEFAULT '',
    endereco VARCHAR(255) DEFAULT '',
    avaliacao DECIMAL(3,2) NOT NULL DEFAULT 5.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_fornecedor_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS produtos_fornecedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fornecedor_id INT NOT NULL,
    nome VARCHAR(160) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(100) NOT NULL DEFAULT 'outros',
    preco DECIMAL(10,2) NOT NULL DEFAULT 0,
    unidade VARCHAR(60) DEFAULT 'unidade',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_produto_fornecedor (fornecedor_id),
    CONSTRAINT fk_produto_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    nome_evento VARCHAR(120) NOT NULL,
    tipo_evento VARCHAR(100) NOT NULL,
    data_evento DATE NOT NULL,
    hora_evento VARCHAR(10) DEFAULT '',
    endereco_evento VARCHAR(255) DEFAULT '',
    cidade_evento VARCHAR(120) DEFAULT '',
    orcamento_evento DECIMAL(10,2) NOT NULL DEFAULT 0,
    convidados_estimados INT NOT NULL DEFAULT 0,
    estilo_evento VARCHAR(100) DEFAULT '',
    observacoes TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'agendado',
    progresso INT NOT NULL DEFAULT 0,
    privacidade_convidados VARCHAR(30) NOT NULL DEFAULT 'organizador',
    rateio_ativo BOOLEAN NOT NULL DEFAULT FALSE,
    rateio_modo VARCHAR(20) NOT NULL DEFAULT 'auto',
    rateio_valor_fixo DECIMAL(10,2) NOT NULL DEFAULT 0,
    dados_evento TEXT,
    INDEX idx_evento_owner (owner_id),
    INDEX idx_evento_tipo (tipo_evento),
    INDEX idx_evento_data (data_evento),
    CONSTRAINT fk_evento_owner FOREIGN KEY (owner_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS convidados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    nome VARCHAR(160) NOT NULL,
    email VARCHAR(180) DEFAULT '',
    telefone VARCHAR(40) DEFAULT '',
    vinculo VARCHAR(100) DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    restricoes_alimentares TEXT,
    token_rsvp VARCHAR(120) NOT NULL UNIQUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_convidado_evento (evento_id),
    INDEX idx_convidado_status (status),
    CONSTRAINT fk_convidado_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS colaboradores_evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    usuario_id INT NULL,
    nome VARCHAR(160) NOT NULL,
    email VARCHAR(180) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    token VARCHAR(120) NOT NULL UNIQUE,
    pode_editar BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_colaborador_evento_email (evento_id, email),
    INDEX idx_colaborador_usuario (usuario_id),
    CONSTRAINT fk_colaborador_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
    CONSTRAINT fk_colaborador_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS itens_compartilhados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    nome VARCHAR(160) NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    responsavel_tipo VARCHAR(30) NULL,
    responsavel_id INT NULL,
    responsavel_nome VARCHAR(160) DEFAULT '',
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_item_comp_evento (evento_id),
    CONSTRAINT fk_item_comp_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS itens_evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    produto_id INT NULL,
    chave_externa VARCHAR(180) NULL,
    nome VARCHAR(160) NOT NULL,
    categoria VARCHAR(100) DEFAULT 'outros',
    preco DECIMAL(10,2) NOT NULL DEFAULT 0,
    quantidade INT NOT NULL DEFAULT 1,
    INDEX idx_item_evento (evento_id),
    CONSTRAINT fk_item_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
    CONSTRAINT fk_item_produto FOREIGN KEY (produto_id) REFERENCES produtos_fornecedor(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tarefas_evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    chave VARCHAR(100) NULL,
    feita BOOLEAN NOT NULL DEFAULT FALSE,
    prazo DATETIME NULL,
    ordem INT NOT NULL DEFAULT 0,
    INDEX idx_tarefa_evento (evento_id),
    CONSTRAINT fk_tarefa_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS despesas_evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    descricao VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) DEFAULT 'geral',
    valor DECIMAL(10,2) NOT NULL DEFAULT 0,
    comprovante VARCHAR(255) DEFAULT '',
    pago_por VARCHAR(160) DEFAULT '',
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_despesa_evento (evento_id),
    CONSTRAINT fk_despesa_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fotos_evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    usuario_id INT NULL,
    arquivo VARCHAR(255) NOT NULL,
    legenda VARCHAR(255) DEFAULT '',
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_foto_evento (evento_id),
    CONSTRAINT fk_foto_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
    CONSTRAINT fk_foto_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS notificacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo VARCHAR(60) NOT NULL,
    titulo VARCHAR(180) NOT NULL,
    mensagem TEXT NOT NULL,
    evento_id INT NULL,
    referencia_id INT NULL,
    lida BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notificacao_usuario (usuario_id),
    CONSTRAINT fk_notificacao_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_notificacao_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS favoritos_fornecedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    chave VARCHAR(180) NOT NULL,
    UNIQUE KEY uq_favorito_usuario_chave (usuario_id, chave),
    CONSTRAINT fk_favorito_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS logs_evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    usuario_id INT NULL,
    acao VARCHAR(100) NOT NULL,
    detalhe TEXT,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_log_evento (evento_id),
    CONSTRAINT fk_log_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
    CONSTRAINT fk_log_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB;

DROP PROCEDURE IF EXISTS sp_eventos_por_tipo;
DELIMITER //
CREATE PROCEDURE sp_eventos_por_tipo(
    IN e_tipo VARCHAR(100),
    IN e_owner_id INT
)
BEGIN
    SELECT id, owner_id, nome_evento, tipo_evento, data_evento, hora_evento,
           endereco_evento, cidade_evento, orcamento_evento, convidados_estimados,
           estilo_evento, observacoes, status, progresso, privacidade_convidados,
           rateio_ativo, rateio_modo, rateio_valor_fixo, dados_evento
    FROM eventos
    WHERE tipo_evento = e_tipo AND owner_id = e_owner_id
    ORDER BY nome_evento;
END //
DELIMITER ;
