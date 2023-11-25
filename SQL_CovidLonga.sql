CREATE DATABASE  IF NOT EXISTS `mydb_covid` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `mydb_covid`;
-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: mydb_covid
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Paciente`
--

DROP TABLE IF EXISTS `Paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Paciente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `idade` int DEFAULT NULL,
  `sexo` varchar(10) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `raca` varchar(10) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `escolaridade` varchar(20) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `estado` varchar(2) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `cidade` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `zona` varchar(10) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `nosocomial` int DEFAULT NULL,
  `dispneia` int DEFAULT NULL,
  `cardiopati` int DEFAULT NULL,
  `asma` int DEFAULT NULL,
  `diabetes` int DEFAULT NULL,
  `neurologic` int DEFAULT NULL,
  `sintoma_nevoa_mental` int DEFAULT '0',
  `sintoma_perda_olfato` int DEFAULT '0',
  `sintoma_perda_paladar` int DEFAULT '0',
  `sintoma_fadiga` int DEFAULT '0',
  `sintoma_dores_cabeca` int DEFAULT '0',
  `sintoma_problemas_sono` int DEFAULT '0',
  `sintomas_neuromusculares` int DEFAULT '0',
  `sintoma_disturbios_emocionais_psicologicos` int DEFAULT '0',
  `dose_1` int DEFAULT NULL,
  `dose_2` int DEFAULT NULL,
  `hospitalization` int DEFAULT '0',
  `internacao_hospitalar` int DEFAULT NULL,
  `internacao_uti` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `paciente_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `password_reset`
--

DROP TABLE IF EXISTS `password_reset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_reset` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `token` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `expiration_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `probabilidade`
--

DROP TABLE IF EXISTS `probabilidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `probabilidade` (
  `idcovidLonga` int NOT NULL AUTO_INCREMENT,
  `covid` varchar(45) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `probabilidade` varchar(10) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`idcovidLonga`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `resultado_teste`
--

DROP TABLE IF EXISTS `resultado_teste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resultado_teste` (
  `id` int NOT NULL AUTO_INCREMENT,
  `probabilidade` float DEFAULT NULL,
  `mensagem` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `data_teste` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ResultadoTeste`
--

DROP TABLE IF EXISTS `ResultadoTeste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ResultadoTeste` (
  `id` int NOT NULL AUTO_INCREMENT,
  `probabilidade` float DEFAULT NULL,
  `mensagem` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `data_teste` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `resultadoteste_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Teste`
--

DROP TABLE IF EXISTS `Teste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Teste` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `paciente_id` int NOT NULL,
  `nome` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `probabilidade` float DEFAULT NULL,
  `data_do_teste` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `paciente_id` (`paciente_id`),
  CONSTRAINT `teste_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
  CONSTRAINT `teste_ibfk_2` FOREIGN KEY (`paciente_id`) REFERENCES `Paciente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb3_unicode_ci NOT NULL,
  `password` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  `confirm_password` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  `birth_date` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  `gender` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  `city` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  `state` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  `race` varchar(60) COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `UserProfile`
--

DROP TABLE IF EXISTS `UserProfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UserProfile` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `username` varchar(100) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `userprofile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-25 19:55:17
