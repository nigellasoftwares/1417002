-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 02, 2023 at 09:20 AM
-- Server version: 8.0.33-0ubuntu0.20.04.2
-- PHP Version: 7.4.3-4ubuntu2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nigella_form`
--

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_job_sub_sector`
--

CREATE TABLE `detailed_dd_job_sub_sector` (
  `id` int NOT NULL,
  `job_sub_sector` varchar(255)  NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
);

--
-- Dumping data for table `detailed_dd_job_sub_sector`
--

INSERT INTO `detailed_dd_job_sub_sector` (`id`, `job_sub_sector`, `category_list`, `uuid`) VALUES
(10, 'Tapak Semaian Lain', 'Job Sub Sector', 'dkhce'),
(11, 'Tanaman', 'Job Sub Sector', 'dkhce'),
(12, 'Akuakultur', 'Job Sub Sector', 'ha]b`'),
(13, 'Ternakan', 'Job Sub Sector', 'o^un_'),
(14, 'Ladang Kelapa Sawit', 'Job Sub Sector', 'dkhce'),
(15, 'Ladang Koko', 'Job Sub Sector', 'l_nwZ'),
(16, 'Ladang Getah', 'Job Sub Sector', 'l_nwZ'),
(17, 'Ladang Hutan', 'Job Sub Sector', 'l_nwZ'),
(18, 'Ladang Jati / Sentang', 'Job Sub Sector', ']spp]'),
(19, 'Tapak Semaian Sawit', 'Job Sub Sector', 'b_jt^'),
(20, 'Berorientasi Eksport', 'Job Sub Sector', 'hfqga'),
(21, 'Bukan Berorientasi Eksport', 'Job Sub Sector', 'hfqga'),
(22, 'Sektor Elektrik dan Elektronik', 'Job Sub Sector', 'hfqga'),
(23, 'Restoran', 'Job Sub Sector', 'hfqga'),
(24, 'Dobi', 'Job Sub Sector', 'hfqga');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detailed_dd_job_sub_sector`
--
ALTER TABLE `detailed_dd_job_sub_sector`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `job_sub_sector` (`job_sub_sector`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detailed_dd_job_sub_sector`
--
ALTER TABLE `detailed_dd_job_sub_sector`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
