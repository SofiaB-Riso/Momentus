CREATE DATABASE IF NOT EXISTS evento_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE evento_db;

CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_evento VARCHAR(120) NOT NULL,
    tipo_evento VARCHAR(100) NOT NULL,
    data_evento DATE NOT NULL,
    endereco_evento VARCHAR(255) NOT NULL,
    orcamento_evento DECIMAL(10,2) NOT NULL DEFAULT 0
);

DROP PROCEDURE IF EXISTS sp_eventos_por_tipo;

DELIMITER //
CREATE PROCEDURE sp_eventos_por_tipo(
    IN e_tipo VARCHAR(100)
)
BEGIN
    SELECT id, nome_evento, tipo_evento, data_evento, endereco_evento, orcamento_evento 
    FROM eventos
    WHERE tipo_evento = e_tipo
    ORDER BY nome_evento;
END //
DELIMITER ;
