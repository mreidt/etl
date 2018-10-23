-- MySQL dump 10.16  Distrib 10.2.18-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: ETLDB
-- ------------------------------------------------------
-- Server version	10.2.18-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `ETLDB`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ETLDB` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `ETLDB`;

--
-- Table structure for table `ENDERECOS`
--

DROP TABLE IF EXISTS `ENDERECOS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ENDERECOS` (
  `ID_ENDERECOS` int(11) NOT NULL AUTO_INCREMENT,
  `LATITUDE` double DEFAULT NULL,
  `LONGITUDE` double DEFAULT NULL,
  `RUA` varchar(100) DEFAULT NULL,
  `NUMERO` varchar(20) DEFAULT NULL,
  `BAIRRO` varchar(100) DEFAULT NULL,
  `CIDADE` varchar(100) DEFAULT NULL,
  `CEP` varchar(10) DEFAULT NULL,
  `ESTADO` varchar(20) DEFAULT NULL,
  `PAIS` varchar(50) DEFAULT NULL,
  `LATITUDEGRAUS` varchar(20) DEFAULT NULL,
  `LONGITUDEGRAUS` varchar(20) DEFAULT NULL,
  `DISTANCIA` varchar(30) DEFAULT NULL,
  `BEARING` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ID_ENDERECOS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `VISUALIZA_RESULTADOS`
--

DROP TABLE IF EXISTS `VISUALIZA_RESULTADOS`;
/*!50001 DROP VIEW IF EXISTS `VISUALIZA_RESULTADOS`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `VISUALIZA_RESULTADOS` (
  `LATITUDE` tinyint NOT NULL,
  `LONGITUDE` tinyint NOT NULL,
  `RUA` tinyint NOT NULL,
  `NUMERO` tinyint NOT NULL,
  `BAIRRO` tinyint NOT NULL,
  `CIDADE` tinyint NOT NULL,
  `CEP` tinyint NOT NULL,
  `ESTADO` tinyint NOT NULL,
  `PAIS` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Current Database: `ETLDB`
--

USE `ETLDB`;

--
-- Final view structure for view `VISUALIZA_RESULTADOS`
--

/*!50001 DROP TABLE IF EXISTS `VISUALIZA_RESULTADOS`*/;
/*!50001 DROP VIEW IF EXISTS `VISUALIZA_RESULTADOS`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `VISUALIZA_RESULTADOS` AS select `ENDERECOS`.`LATITUDE` AS `LATITUDE`,`ENDERECOS`.`LONGITUDE` AS `LONGITUDE`,`ENDERECOS`.`RUA` AS `RUA`,`ENDERECOS`.`NUMERO` AS `NUMERO`,`ENDERECOS`.`BAIRRO` AS `BAIRRO`,`ENDERECOS`.`CIDADE` AS `CIDADE`,`ENDERECOS`.`CEP` AS `CEP`,`ENDERECOS`.`ESTADO` AS `ESTADO`,`ENDERECOS`.`PAIS` AS `PAIS` from `ENDERECOS` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-23 16:24:17
