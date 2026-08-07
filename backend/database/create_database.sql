CREATE DATABASE IF NOT EXISTS evento_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE evento_db;

CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_evento VARCHAR(120) NOT NULL,
    tipo_evento VARCHAR(100) NOT NULL,
    data_evento DATE NOT NULL,
    endereco_evento VARCHAR(255) NULL DEFAULT '',
    orcamento_evento DECIMAL(10,2) NOT NULL DEFAULT 0,
    dados_evento TEXT NULL
);

-- Se você já tinha o banco criado antes desta atualização, rode isto
-- para adicionar a coluna nova sem perder os dados existentes:
-- ALTER TABLE eventos ADD COLUMN dados_evento TEXT NULL;
-- ALTER TABLE eventos MODIFY endereco_evento VARCHAR(255) NULL DEFAULT '';

DROP PROCEDURE IF EXISTS sp_eventos_por_tipo;

DELIMITER //
CREATE PROCEDURE sp_eventos_por_tipo(
    IN e_tipo VARCHAR(100)
)
BEGIN
    SELECT id, nome_evento, tipo_evento, data_evento, endereco_evento, orcamento_evento, dados_evento
    FROM eventos
    WHERE tipo_evento = e_tipo
    ORDER BY nome_evento;
END //
DELIMITER ;
