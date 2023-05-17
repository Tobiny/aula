-- Crear la base de datos 'Aula Inteligente'
CREATE DATABASE `aula_inteligente`;

-- Usar la base de datos 'Aula Inteligente'
USE `aula_inteligente`;

-- Crear la tabla 'clase'
CREATE TABLE `clase` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `codigo_maestro` VARCHAR(50),
  `materia` VARCHAR(100),
  `dia` INT,
  `mes` INT,
  `anio` INT,
  `hora` VARCHAR(6)
);

-- Crear la tabla 'lecturas'
CREATE TABLE `lecturas` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `clase_id` INT,
  `hora` TIME,
  `emocion` VARCHAR(50),
  `temperatura` FLOAT,
  FOREIGN KEY (`clase_id`) REFERENCES `clase`(`id`)
);
