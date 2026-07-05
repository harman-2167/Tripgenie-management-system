-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: tripgenie
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `phone` bigint DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `booking_type` varchar(50) DEFAULT NULL,
  `booking_number` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (1,'raman',987656789,'raman@gmail.com','ambala','GENERAL',1),(2,'RAMAN',9876567888,'raman@gmail.com','ambala','GENERAL',1),(3,'A',987667890,'a@gmail.com','Apple land','GENERAL',1),(4,'A',987667890,'a@gmail.com','Apple land','GENERAL',1),(5,'harman',6787656787,'harman@gmail.com','patiala','GENERAL',1),(6,'banu',9876789788,'banu@gmail.com','mumbai','GENERAL',1),(7,'bana',8767856433,'bana@gmail.com','mumbai','GENERAL',1),(8,'kamal',9878987883,'kamal@gmail.com','mohali','GENERAL',1),(9,'diya',1234567890,'diya@gmail.com','noida','login',0),(10,'diya',1234567890,'diya@gmail.com','noida','GENERAL',1),(11,'kamal',8765456787,'kamal@gmail.com','mohali','GENERAL',1),(12,'radhika',6787656788,'radhika@gmail.com','Ambala','GENERAL',1),(13,'KIRAT',9876567898,'kirat@gmail.com','Zirakpur','GENERAL',1),(14,'harsimran',8766567899,'harsimarn@gmail.com','chandigarh','GENERAL',1),(15,'shivangi',4737586783,'shivangi@gmail.com','gorakhpur','GENERAL',1);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaints`
--

DROP TABLE IF EXISTS `complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints` (
  `complaint_id` int NOT NULL AUTO_INCREMENT,
  `complaint_text` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints`
--

LOCK TABLES `complaints` WRITE;
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `review_text` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotel_booking`
--

DROP TABLE IF EXISTS `hotel_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel_booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) DEFAULT NULL,
  `room_type` varchar(100) DEFAULT NULL,
  `room_fare` int DEFAULT NULL,
  `booking_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_booking`
--

LOCK TABLES `hotel_booking` WRITE;
/*!40000 ALTER TABLE `hotel_booking` DISABLE KEYS */;
INSERT INTO `hotel_booking` VALUES (1,'RAMAN','Single Room',3600,NULL),(2,'A','Single Room',3600,NULL),(3,'Non-AC Room','AC Premium Room',6000,5),(4,'Non-AC Room','Single Room',3600,8),(5,'diya','Couple Room',2200,NULL),(6,'Non-AC Room','Couple Room',4400,10),(7,'Non-AC Room','Single Room',3600,11),(8,'Non-AC Room','AC Premium Room',6000,12),(9,'Non-AC Room','Single Room',5400,13),(10,'Non-AC Room','AC Premium Room',9000,14),(11,'Non-AC Room','Family Room',10000,15);
/*!40000 ALTER TABLE `hotel_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owner`
--

DROP TABLE IF EXISTS `owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owner` (
  `owner_id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`owner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owner`
--

LOCK TABLES `owner` WRITE;
/*!40000 ALTER TABLE `owner` DISABLE KEYS */;
INSERT INTO `owner` VALUES (1,'Admin123');
/*!40000 ALTER TABLE `owner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `place_booking`
--

DROP TABLE IF EXISTS `place_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `place_booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) DEFAULT NULL,
  `place_name` varchar(100) DEFAULT NULL,
  `place_fare` int DEFAULT NULL,
  `booking_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `place_booking`
--

LOCK TABLES `place_booking` WRITE;
/*!40000 ALTER TABLE `place_booking` DISABLE KEYS */;
INSERT INTO `place_booking` VALUES (1,NULL,'Udaipur',0,8),(2,'diya','Amritsar',0,NULL),(3,'diya','Shimla',0,NULL),(4,NULL,'Manali',0,10),(5,NULL,'Goa',0,11),(6,NULL,'Mysore',0,12),(7,NULL,'Jaisalmer',0,13),(8,NULL,'Amritsar',0,14),(9,NULL,'Shimla',0,15);
/*!40000 ALTER TABLE `place_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transport_booking`
--

DROP TABLE IF EXISTS `transport_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transport_booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) DEFAULT NULL,
  `transport_type` varchar(100) DEFAULT NULL,
  `transport_fare` int DEFAULT NULL,
  `booking_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transport_booking`
--

LOCK TABLES `transport_booking` WRITE;
/*!40000 ALTER TABLE `transport_booking` DISABLE KEYS */;
INSERT INTO `transport_booking` VALUES (1,'A','Train',1200,NULL),(2,'harman','Train',1200,5),(3,'kamal','Train',1200,8),(4,'diya','Train',600,NULL),(5,'diya','Train',1200,10),(6,'kamal','Train',1200,11),(7,'radhika','Train',1200,12),(8,'KIRAT','Cab',10500,13),(9,'harsimran','Train',1800,14),(10,'shivangi','Train',2400,15);
/*!40000 ALTER TABLE `transport_booking` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-03 20:44:16
