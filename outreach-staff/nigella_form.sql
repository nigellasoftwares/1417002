-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 03, 2023 at 11:02 AM
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
-- Table structure for table `category_list`
--

CREATE TABLE `category_list` (
  `id` int NOT NULL,
  `categories` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `category_list`
--

INSERT INTO `category_list` (`id`, `categories`) VALUES
(1, 'License Category'),
(2, 'City'),
(3, 'State'),
(4, 'Sector'),
(5, 'Gender'),
(6, 'Citizenship'),
(7, 'Maritial Status'),
(8, 'Point of Entry'),
(9, 'Religion'),
(10, 'Race'),
(11, 'Relationship'),
(12, 'Job Sector'),
(13, 'Job status&sponsor'),
(14, 'Job Status'),
(15, 'Document Status'),
(16, 'Country of issued document'),
(17, 'Current Status of document'),
(18, 'Is dependent together'),
(19, 'Type of document'),
(21, 'Employment Status'),
(22, 'Worker legal Status'),
(23, 'Designation'),
(24, 'Job Sub Sector');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_citizenship`
--

CREATE TABLE `detailed_dd_citizenship` (
  `id` int NOT NULL,
  `citizenship` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_citizenship`
--

INSERT INTO `detailed_dd_citizenship` (`id`, `citizenship`, `category_list`, `uuid`) VALUES
(75, 'Indonesia', 'Citizenship', 'ue\\t]'),
(76, 'Philippines', 'Citizenship', 'qllfx');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_city`
--

CREATE TABLE `detailed_dd_city` (
  `id` int NOT NULL,
  `city` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_city`
--

INSERT INTO `detailed_dd_city` (`id`, `city`, `category_list`, `uuid`) VALUES
(49, 'Beaufort', 'City', 'uYc^y'),
(50, 'Beluran', 'City', 'kYrce'),
(51, 'Bongawan', 'City', '[gwxf'),
(52, 'Inanam', 'City', 'kbp\\f'),
(53, 'Keningau', 'City', 'aiebu'),
(54, 'Kota Belud', 'City', 'rZ_sY'),
(55, 'Kota Kinabalu', 'City', 'Y[vyy'),
(56, 'Kota Marudu', 'City', 'ud_je'),
(57, 'Kuala Penyu', 'City', 'vg\\gY'),
(58, 'Kudat', 'City', 'nclbn'),
(59, 'Kunak', 'City', 'deswm'),
(60, 'Lahad Datu', 'City', 'vb`pg'),
(61, 'Lamag', 'City', 'd`y__'),
(62, 'Likas', 'City', '\\ymys'),
(63, 'Membakut', 'City', 'gpi^n'),
(64, 'Menumbok', 'City', 'Z`]hf'),
(65, 'Nabawan', 'City', '\\xxZd'),
(66, 'Papar', 'City', 'sw^tc'),
(67, 'Penampang', 'City', 'Yj\\ai'),
(68, 'Ranau', 'City', '^ge\\_'),
(69, 'Sandakan', 'City', '_ie^o'),
(70, 'Semporna', 'City', 'vY`Ys'),
(71, 'Sipitang', 'City', ']dj\\`'),
(72, 'Tambunan', 'City', 'juprp'),
(73, 'Tamparuli', 'City', 'Yyhse'),
(74, 'Tg. Aru', 'City', 'ejhkj'),
(75, 'Tawau', 'City', 'hk[Zk'),
(76, 'Tenom', 'City', 'py\\[u'),
(77, 'Tuaran', 'City', '^Z`nb'),
(78, 'Kinabatangan', 'City', 'v_[ph'),
(79, 'Pamol', 'City', 'k]cm\\'),
(80, 'Putatan', 'City', 'xqk`t');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_country_issued_doc`
--

CREATE TABLE `detailed_dd_country_issued_doc` (
  `id` int NOT NULL,
  `country_issued_doc` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_country_issued_doc`
--

INSERT INTO `detailed_dd_country_issued_doc` (`id`, `country_issued_doc`, `category_list`, `uuid`) VALUES
(7, 'Indonesia', 'Country of issued document', 'qjcbx'),
(8, 'Philippines', 'Country of issued document', 'cx`c_'),
(10, 'Malaysia', 'Country of issued document', 'svahe');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_current_status_doc`
--

CREATE TABLE `detailed_dd_current_status_doc` (
  `id` int NOT NULL,
  `current_status_doc` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_current_status_doc`
--

INSERT INTO `detailed_dd_current_status_doc` (`id`, `current_status_doc`, `category_list`, `uuid`) VALUES
(9, 'Aktif', 'Current Status of document', 'pqgqx'),
(10, 'Tamat tempoh', 'Current Status of document', 'ZdZ]m'),
(11, 'Diperbaharui', 'Current Status of document', 'ab^vi'),
(12, 'Tiada', 'Current Status of document', 'mjeyY'),
(13, 'Permohonan baru', 'Current Status of document', ']cvvm'),
(14, 'Tidak diperakui', 'Current Status of document', 't\\dnw'),
(15, 'Permohonan baru (Regu)', 'Current Status of document', '[[Zvu');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_designation`
--

CREATE TABLE `detailed_dd_designation` (
  `id` int NOT NULL,
  `designation` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_designation`
--

INSERT INTO `detailed_dd_designation` (`id`, `designation`, `category_list`, `uuid`) VALUES
(6, 'my designation', 'Designation', 'ol`ol'),
(7, '1231231', 'Designation', 'evpcn');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_doc_status`
--

CREATE TABLE `detailed_dd_doc_status` (
  `id` int NOT NULL,
  `doc_status` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_doc_status`
--

INSERT INTO `detailed_dd_doc_status` (`id`, `doc_status`, `category_list`, `uuid`) VALUES
(1, 'Sah', 'Document Status', '1'),
(5, 'Tidak sah', 'Document Status', 'gmiti'),
(6, 'Tamat tempoh', 'Document Status', 'mpi^^'),
(8, 'Tamat tempoh (Diperbaharui)', 'Document Status', 'kq[c['),
(9, 'Tidak diperakui', 'Document Status', 'owxgy'),
(10, 'Permohonan baru', 'Document Status', 'jfpa^'),
(11, 'Permohonan baru(Regu)', 'Document Status', 'f[]]k'),
(12, 'Tiada', 'Document Status', 'skxbx');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_employement_status`
--

CREATE TABLE `detailed_dd_employement_status` (
  `id` int NOT NULL,
  `employement_status` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_employement_status`
--

INSERT INTO `detailed_dd_employement_status` (`id`, `employement_status`, `category_list`, `uuid`) VALUES
(8, 'Sah/Aktif', 'Employment Status', 'xyohZ'),
(9, 'Tidak sah', 'Employment Status', 'gmsgr'),
(10, 'Tidak berkerja', 'Employment Status', 'kZxv`'),
(11, 'Kerja sambilan', 'Employment Status', 'owaf]');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_gender`
--

CREATE TABLE `detailed_dd_gender` (
  `id` int NOT NULL,
  `gender` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_gender`
--

INSERT INTO `detailed_dd_gender` (`id`, `gender`, `category_list`, `uuid`) VALUES
(1, 'Perempuan', 'Gender', '1'),
(2, 'Lelaki', 'Gender', '2');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_is_dependent_together`
--

CREATE TABLE `detailed_dd_is_dependent_together` (
  `id` int NOT NULL,
  `is_dep_together` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_is_dependent_together`
--

INSERT INTO `detailed_dd_is_dependent_together` (`id`, `is_dep_together`, `category_list`, `uuid`) VALUES
(4, 'Ya', 'Is dependent together', '`lhlk'),
(5, 'Tidak', 'Is dependent together', 'oemc_');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_job_sector`
--

CREATE TABLE `detailed_dd_job_sector` (
  `id` int NOT NULL,
  `job_sector` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_job_sector`
--

INSERT INTO `detailed_dd_job_sector` (`id`, `job_sector`, `category_list`, `uuid`) VALUES
(9, 'Pertanian', 'Job Sector', 'l_nwZ'),
(10, 'Perladangan', 'Job Sector', 'dkhce'),
(11, 'Perkilangan', 'Job Sector', 'o[Ziv'),
(12, 'Perkhidmatan', 'Job Sector', '\\jyor'),
(13, 'Pembinaan', 'Job Sector', 'hkk[Y'),
(14, 'Perlombongan', 'Job Sector', 'hfqga');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_job_status_sponsor`
--

CREATE TABLE `detailed_dd_job_status_sponsor` (
  `id` int NOT NULL,
  `job_status_sponser` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_job_status_sponsor`
--

INSERT INTO `detailed_dd_job_status_sponsor` (`id`, `job_status_sponser`, `category_list`, `uuid`) VALUES
(7, 'Majikan', 'Job status&sponsor', 'm[rfk'),
(8, 'Sendiri', 'Job status&sponsor', 'sulpu');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_job_sub_sector`
--

CREATE TABLE `detailed_dd_job_sub_sector` (
  `id` int NOT NULL,
  `job_sub_sector` varchar(255) /*CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL*/,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_job_sub_sector`
--

INSERT INTO `detailed_dd_job_sub_sector` (`id`, `job_sub_sector`, `category_list`, `uuid`) VALUES
(10, 'Tapak Semaian Lain', 'Job Sub Sector', 'Yteqv'),
(11, 'Tanaman', 'Job Sub Sector', 'y_]hq'),
(12, 'Akuakultur', 'Job Sub Sector', 'ha]b`'),
(13, 'Ternakan', 'Job Sub Sector', 'o^un_'),
(14, 'Ladang Kelapa Sawit', 'Job Sub Sector', 'qytsj'),
(15, 'Ladang Koko', 'Job Sub Sector', '^`Zj^'),
(16, 'Ladang Getah', 'Job Sub Sector', 'rn_ux'),
(17, 'Ladang Hutan', 'Job Sub Sector', 'vnqta'),
(18, 'Ladang Jati / Sentang', 'Job Sub Sector', ']spp]'),
(19, 'Tapak Semaian Sawit', 'Job Sub Sector', 'b_jt^'),
(20, 'Berorientasi Eksport', 'Job Sub Sector', 'mynue'),
(21, 'Bukan Berorientasi Eksport', 'Job Sub Sector', '\\`mau'),
(22, 'Sektor Elektrik dan Elektronik', 'Job Sub Sector', '^qga\\'),
(23, 'Restoran', 'Job Sub Sector', 'wbYr_'),
(24, 'Dobi', 'Job Sub Sector', 'fknjk');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_license_category`
--

CREATE TABLE `detailed_dd_license_category` (
  `id` int NOT NULL,
  `license_list` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_license_category`
--

INSERT INTO `detailed_dd_license_category` (`id`, `license_list`, `category_list`, `uuid`) VALUES
(125, 'A', 'License Category', 'kcwsp'),
(126, 'B', 'License Category', 'rvnvo'),
(127, 'C', 'License Category', '`pqog');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_maritail_status`
--

CREATE TABLE `detailed_dd_maritail_status` (
  `id` int NOT NULL,
  `maritial_status` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_maritail_status`
--

INSERT INTO `detailed_dd_maritail_status` (`id`, `maritial_status`, `category_list`, `uuid`) VALUES
(11, 'Berkawhin', 'Maritial Status', 'sgihe'),
(12, 'Bujang', 'Maritial Status', 'lkitw'),
(13, 'Bercerai', 'Maritial Status', 'ooqyt'),
(14, 'Duda/Janda', 'Maritial Status', '_mi]r'),
(16, 'Tinggal berasingan', 'Maritial Status', 'rshmh');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_poe`
--

CREATE TABLE `detailed_dd_poe` (
  `id` int NOT NULL,
  `poe` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_poe`
--

INSERT INTO `detailed_dd_poe` (`id`, `poe`, `category_list`, `uuid`) VALUES
(1, 'Sandakan', 'Point of Entry', '1'),
(6, 'Tawau', 'Point of Entry', 'dt[va'),
(7, 'Kota Kinabalu', 'Point of Entry', 'qntfu'),
(8, 'Kuala Sipitang', 'Point of Entry', 'wvnij'),
(9, 'Semporna', 'Point of Entry', '`oyih'),
(10, 'Kudat', 'Point of Entry', 'qgle\\'),
(11, 'Lahad Datu', 'Point of Entry', 'loyrn'),
(12, 'Pulau Bangi', 'Point of Entry', 'bplbm'),
(13, 'Menumbok', 'Point of Entry', 'x]Zj`'),
(14, 'Lain-lain', 'Point of Entry', '\\\\jc['),
(15, '', 'Point of Entry', 'obvxZ');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_race`
--

CREATE TABLE `detailed_dd_race` (
  `id` int NOT NULL,
  `race` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_race`
--

INSERT INTO `detailed_dd_race` (`id`, `race`, `category_list`, `uuid`) VALUES
(1, 'Lain-Lain', 'Race', '1'),
(2, 'Melayu', 'Race', '2'),
(5, 'Bugis', 'Race', 'yla_l'),
(6, 'Boyan', 'Race', 'vu\\pZ'),
(7, 'Banjar', 'Race', 'ni`ru'),
(8, 'Jawa', 'Race', 'Z\\uin'),
(9, 'Minangkabau', 'Race', 'jr\\gh'),
(10, 'India Muslim', 'Race', 'bbYhy'),
(11, 'Tamil', 'Race', 'oyisp'),
(12, 'India', 'Race', 's\\ws`'),
(13, 'Bisaya', 'Race', 'fybp\\'),
(14, 'Timor', 'Race', 'og\\f`'),
(15, 'Tator', 'Race', 'xZk_\\');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_relationship`
--

CREATE TABLE `detailed_dd_relationship` (
  `id` int NOT NULL,
  `relationship` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_relationship`
--

INSERT INTO `detailed_dd_relationship` (`id`, `relationship`, `category_list`, `uuid`) VALUES
(1, 'Suami', 'Relationship', '1'),
(5, 'Isteri', 'Relationship', 'k`\\tn'),
(6, 'Ayah', 'Relationship', 'pmueo'),
(7, 'Ibu', 'Relationship', 'w_c`b'),
(8, 'Abang', 'Relationship', '`^rto'),
(9, 'Adik', 'Relationship', 'Yygp^'),
(10, 'Kakak', 'Relationship', 'nysgy'),
(11, 'Saudara', 'Relationship', 'eZn]u');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_religion`
--

CREATE TABLE `detailed_dd_religion` (
  `id` int NOT NULL,
  `religion` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_religion`
--

INSERT INTO `detailed_dd_religion` (`id`, `religion`, `category_list`, `uuid`) VALUES
(1, 'Islam', 'Religion', '1'),
(2, 'Kristian', 'Religion', '2'),
(5, 'Buddha', 'Religion', 'sn_t^'),
(6, 'Hindu', 'Religion', 'r^leu'),
(7, 'Tiada', 'Religion', 'nhcb`'),
(8, 'Lain-lain', 'Religion', 'w[b^f');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_sector`
--

CREATE TABLE `detailed_dd_sector` (
  `id` int NOT NULL,
  `sector` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_sector`
--

INSERT INTO `detailed_dd_sector` (`id`, `sector`, `category_list`, `uuid`) VALUES
(17, 'Tanaman', 'Sector', 'dxva]'),
(18, 'Akuakultur', 'Sector', 'k]bxY'),
(19, 'Ternakan', 'Sector', 'd_xin'),
(20, 'Ladang Kelapa Sawit', 'Sector', 'yonvy'),
(21, 'Ladang Getah', 'Sector', '\\exey'),
(22, 'Ladang Koko', 'Sector', 't^rYo'),
(23, 'Ladang Hutan', 'Sector', 'tnxc['),
(24, 'Ladang Jati / Sentang', 'Sector', 'auget'),
(25, 'Semaian Ladang Sawit', 'Sector', 'tluhv'),
(26, 'Tapak Semaian Lain', 'Sector', '[`ala'),
(27, 'Berorientasi Eksport', 'Sector', '_bdcr'),
(28, 'Bukan Berorientasi Eksport', 'Sector', 't\\r[n'),
(29, 'Sektor Elektrik dan Elektronik', 'Sector', 'f]exn'),
(30, 'Restoran', 'Sector', 'r_\\no'),
(31, 'Dobi', 'Sector', 'htdpt'),
(32, 'Rumah Kebajikan', 'Sector', 'ffnvh'),
(33, 'Spa dan Refleksologi', 'Sector', '[hton'),
(34, 'Pusat Peranginan', 'Sector', 'r[ngl'),
(35, 'Pembersihan', 'Sector', '[Yqxl'),
(36, 'Borong dan Runcit', 'Sector', '_sjwj'),
(37, 'Hotel', 'Sector', 'gtl\\c'),
(38, 'Bangunan', 'Sector', 'aYc`\\'),
(39, 'Infrastruktur', 'Sector', 'lZZa_'),
(40, 'Lanskap', 'Sector', 'cy^o\\'),
(41, 'Perlombongan', 'Sector', 'a\\ep`'),
(42, 'Pengkuarian', 'Sector', 'jkixZ');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_state`
--

CREATE TABLE `detailed_dd_state` (
  `id` int NOT NULL,
  `state` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_state`
--

INSERT INTO `detailed_dd_state` (`id`, `state`, `category_list`, `uuid`) VALUES
(11, 'Sabah', 'State', 'im]kj');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_type_of_doc`
--

CREATE TABLE `detailed_dd_type_of_doc` (
  `id` int NOT NULL,
  `type_of_doc` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_type_of_doc`
--

INSERT INTO `detailed_dd_type_of_doc` (`id`, `type_of_doc`, `category_list`, `uuid`) VALUES
(7, 'Biodata Siswa', 'Type of document', 'qvbbr'),
(8, 'Formulir Peserta Didik', 'Type of document', 'ohmol'),
(9, 'i-Kad', 'Type of document', 'meag`'),
(10, 'Kartu Indonesia Sehat', 'Type of document', 'bkush'),
(11, 'Kartu Keluarga', 'Type of document', 'jZyvw'),
(12, 'Kartu TP', 'Type of document', ']\\djs'),
(13, 'Lain-lain', 'Type of document', 'fmjwi'),
(14, 'Passport', 'Type of document', 'qhie`'),
(15, 'Pemeriksaan Kesihatan', 'Type of document', '_[lwv'),
(16, 'PLKS', 'Type of document', 'a`g[b'),
(17, 'PLKS (Regu)', 'Type of document', 'vvwt\\'),
(18, 'PLS', 'Type of document', ']hvjn'),
(19, 'PLS (Jaminan Isteri)', 'Type of document', 'ZlY\\x'),
(20, 'PLS (Jaminan Suami)', 'Type of document', 'rYmhx'),
(21, 'PLS (Regu)', 'Type of document', 'Ysewl'),
(22, 'Rekod Kesihatan', 'Type of document', 'shwht'),
(23, 'Rekod Sekolah', 'Type of document', 'pYYlq'),
(24, 'Sijil Lahir Indonesia', 'Type of document', 'bnfiy'),
(25, 'Sijil/Surat Nikah', 'Type of document', 'Yfvkw'),
(26, 'Surat Bukti Pencatatan Kelahiran', 'Type of document', 'aaYul'),
(27, 'Surat Keterangan Kabupaten', 'Type of document', 'Zwwgh');

-- --------------------------------------------------------

--
-- Table structure for table `detailed_dd_worker_legal_status`
--

CREATE TABLE `detailed_dd_worker_legal_status` (
  `id` int NOT NULL,
  `legal_status` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `detailed_dd_worker_legal_status`
--

INSERT INTO `detailed_dd_worker_legal_status` (`id`, `legal_status`, `category_list`, `uuid`) VALUES
(1, 'legal', 'Worker legal Status', '1'),
(2, 'illegal', 'Worker legal Status', '2');

-- --------------------------------------------------------

--
-- Table structure for table `family_form`
--

CREATE TABLE `family_form` (
  `id` int NOT NULL,
  `form_created_by` varchar(255) NOT NULL,
  `form_created_date` varchar(255) NOT NULL,
  `form_unique_key` varchar(255) NOT NULL,
  `form_family_reg_no` varchar(255) NOT NULL,
  `family_form_worker_name` varchar(255) NOT NULL,
  `family_form_relationship` varchar(255) NOT NULL,
  `family_form_name_of_family_member` varchar(255) NOT NULL,
  `family_form_family_name` varchar(255) NOT NULL,
  `family_form_is_famliy_togther` varchar(255) NOT NULL,
  `family_form_family_form_poe` varchar(255) NOT NULL,
  `family_form_citizenship` varchar(255) NOT NULL,
  `family_form_religion` varchar(255) NOT NULL,
  `family_form_marital_status` varchar(255) NOT NULL,
  `family_form_gender` varchar(255) NOT NULL,
  `family_form_address1` varchar(255) NOT NULL,
  `family_form_address2` varchar(255) NOT NULL,
  `family_form_address3` varchar(255) NOT NULL,
  `family_form_postcode` varchar(255) NOT NULL,
  `family_form_city` varchar(255) NOT NULL,
  `family_form_state` varchar(255) NOT NULL,
  `family_form_contact_no` varchar(255) NOT NULL,
  `family_form_race` varchar(255) NOT NULL,
  `family_form_place_of_birth` varchar(255) NOT NULL,
  `family_form_emp_status` varchar(255) NOT NULL,
  `family_form_emp_name` varchar(255) NOT NULL,
  `family_form_emp_address` varchar(255) NOT NULL,
  `family_form_doc_path_email` varchar(255) NOT NULL,
  `family_form_doc_image_no` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `family_form`
--

INSERT INTO `family_form` (`id`, `form_created_by`, `form_created_date`, `form_unique_key`, `form_family_reg_no`, `family_form_worker_name`, `family_form_relationship`, `family_form_name_of_family_member`, `family_form_family_name`, `family_form_is_famliy_togther`, `family_form_family_form_poe`, `family_form_citizenship`, `family_form_religion`, `family_form_marital_status`, `family_form_gender`, `family_form_address1`, `family_form_address2`, `family_form_address3`, `family_form_postcode`, `family_form_city`, `family_form_state`, `family_form_contact_no`, `family_form_race`, `family_form_place_of_birth`, `family_form_emp_status`, `family_form_emp_name`, `family_form_emp_address`, `family_form_doc_path_email`, `family_form_doc_image_no`) VALUES
(1, 'form_created_by', '21/05/2023', 'form_unique_key', 'form_family_reg_no', 'family_form_worker_name', 'family_form_relationship', 'family_form_name_of_family_member', 'family_form_family_name', 'family_form_is_famliy_togther', 'family_form_family_form_poe', 'family_form_citizenship', 'family_form_religion', 'family_form_marital_status', 'family_form_gender', 'family_form_address1', 'family_form_address2', 'family_form_address3', 'family_form_postcode', 'family_form_city', 'family_form_state', 'family_form_contact_no', 'family_form_race', 'family_form_place_of_birth', 'family_form_emp_status', 'family_form_emp_name', 'family_form_emp_address', 'family_form_doc_path_email', 'family_form_doc_image_no'),
(2, 'form_created_by', '21/05/2023', 'form_unique_key1', 'form_family_reg_no', 'family_form_worker_name', 'family_form_relationship', 'family_form_name_of_family_member', 'family_form_family_name', 'family_form_is_famliy_togther', 'family_form_family_form_poe', 'family_form_citizenship', 'family_form_religion', 'family_form_marital_status', 'family_form_gender', 'family_form_address1', 'family_form_address2', 'family_form_address3', 'family_form_postcode', 'family_form_city', 'family_form_state', 'family_form_contact_no', 'family_form_race', 'family_form_place_of_birth', 'family_form_emp_status', 'family_form_emp_name', 'family_form_emp_address', 'family_form_doc_path_email', 'family_form_doc_image_no');

-- --------------------------------------------------------

--
-- Table structure for table `form_image`
--

CREATE TABLE `form_image` (
  `id` int NOT NULL,
  `image_email` varchar(255) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `image_store_date` varchar(255) NOT NULL,
  `image_store_time` varchar(255) NOT NULL,
  `form_unique_key` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `form_image`
--

INSERT INTO `form_image` (`id`, `image_email`, `image_path`, `image_store_date`, `image_store_time`, `form_unique_key`) VALUES
(1, 'image_email', 'image_path', 'image_store_date', 'image_store_time', 'form_unique_key'),
(2, 'image_email', 'image_path', 'image_store_date', 'image_store_time', 'form_unique_key1');

-- --------------------------------------------------------

--
-- Table structure for table `form_worker_registration_no`
--

CREATE TABLE `form_worker_registration_no` (
  `id` int NOT NULL,
  `worker_email` varchar(255) NOT NULL,
  `worker_no` varchar(255) NOT NULL,
  `worker_no_reg_date` varchar(255) NOT NULL,
  `worker_no_reg_time` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `form_worker_registration_no`
--

INSERT INTO `form_worker_registration_no` (`id`, `worker_email`, `worker_no`, `worker_no_reg_date`, `worker_no_reg_time`) VALUES
(1, 'amsonlyfarhan19@gmail.com', 'W000001', '17-03-2023', '06:36'),
(2, 'nigellainfotech.com@gmail.com', 'W000001', '18-03-2023', '12:34'),
(3, 'yeoh.2007@gmail.com', 'W000001', '30-03-2023', '03:49');

-- --------------------------------------------------------

--
-- Table structure for table `full_form`
--

CREATE TABLE `full_form` (
  `id` int NOT NULL,
  `form_id` varchar(255) NOT NULL,
  `created_by` varchar(255) NOT NULL,
  `created_time` varchar(255) NOT NULL,
  `completed_at` varchar(255) NOT NULL,
  `form_status` varchar(255) NOT NULL,
  `form_made_on_platform` varchar(255) NOT NULL,
  `form_fill_start_time` varchar(255) NOT NULL,
  `form_fill_end_time` varchar(255) NOT NULL,
  `form_fill_date_start` varchar(255) NOT NULL,
  `form_fill_date_end` varchar(255) NOT NULL,
  `form_last_fill_position` varchar(255) NOT NULL,
  `is_aps_completed` varchar(255) NOT NULL,
  `is_add_employer_completed` varchar(255) NOT NULL,
  `is_add_branch_loc_completed` varchar(255) NOT NULL,
  `is_add_worker_list_completed` varchar(255) NOT NULL,
  `is_add_dependent_completed` varchar(255) NOT NULL,
  `agensi_pekerjaan_aps` varchar(255) NOT NULL,
  `license_category_aps` varchar(255) NOT NULL,
  `postcode_aps` varchar(255) NOT NULL,
  `office_telephone_no_aps` varchar(255) NOT NULL,
  `new_ssm_number_aps` varchar(255) NOT NULL,
  `address_1_aps` varchar(255) NOT NULL,
  `city_aps` varchar(255) NOT NULL,
  `mobile_number_aps` varchar(255) NOT NULL,
  `old_ssm_number_aps` varchar(255) NOT NULL,
  `address_2_aps` varchar(255) NOT NULL,
  `state_aps` varchar(255) NOT NULL,
  `email_aps` varchar(255) NOT NULL,
  `aps_license_no` varchar(255) NOT NULL,
  `address_3_aps` varchar(255) NOT NULL,
  `license_expr_date_aps` varchar(255) NOT NULL,
  `contact_person_aps` varchar(255) NOT NULL,
  `company_name_employer` varchar(255) NOT NULL,
  `new_ssm_number_employer` varchar(255) NOT NULL,
  `old_ssm_number_employer` varchar(255) NOT NULL,
  `address_1_employer` varchar(255) NOT NULL,
  `address_2_employer` varchar(255) NOT NULL,
  `address_3_employer` varchar(255) NOT NULL,
  `postcode__employer` varchar(255) NOT NULL,
  `city_employer` varchar(255) NOT NULL,
  `state_employer` varchar(255) NOT NULL,
  `office_telephone_no_employer` varchar(255) NOT NULL,
  `mobile_no_employer` varchar(255) NOT NULL,
  `fax_no_employer` varchar(255) NOT NULL,
  `yr_of_buss_comm_employer` varchar(255) NOT NULL,
  `sector_employer` varchar(255) NOT NULL,
  `name_of_pes_incharge_employer` varchar(255) NOT NULL,
  `designation_employer` varchar(255) NOT NULL,
  `pic_mob_no_employer` varchar(255) NOT NULL,
  `employment_loc_name_location` varchar(255) NOT NULL,
  `address_1_location` varchar(255) NOT NULL,
  `address_2_location` varchar(255) NOT NULL,
  `address_3_location` varchar(255) NOT NULL,
  `postcode_location` varchar(255) NOT NULL,
  `state_location` varchar(255) NOT NULL,
  `city_location` varchar(255) NOT NULL,
  `office_telephpone_no_location` varchar(255) NOT NULL,
  `office_mob_no_location` varchar(255) NOT NULL,
  `email_location` varchar(255) NOT NULL,
  `name_of_pers_incharge_location` varchar(255) NOT NULL,
  `designation_location` varchar(255) NOT NULL,
  `pic_mob_no_location` varchar(255) NOT NULL,
  `name_of_worker_WorkerList` varchar(255) NOT NULL,
  `family_name_WorkerList` text NOT NULL,
  `gender_WorkerList` text NOT NULL,
  `d_o_b_WorkerList` text NOT NULL,
  `place_of_birth_WorkerList` text NOT NULL,
  `citizenship_WorkerList` text NOT NULL,
  `maritial_status_WorkerList` text NOT NULL,
  `p_o_e_WorkerList` text NOT NULL,
  `religion_WorkerList` text NOT NULL,
  `race_WorkerList` text NOT NULL,
  `worker_contact_no_WorkerList` text NOT NULL,
  `worker_email_WorkerList` text NOT NULL,
  `nok__WorkerList` text NOT NULL,
  `relationship_WorkerList` text NOT NULL,
  `nok_contact_no_WorkerList` text NOT NULL,
  `job_sector_employmentdetails` text NOT NULL,
  `job_sub_sector_employmentdetails` text NOT NULL,
  `job_status_sponsor_employmentdetails` text NOT NULL,
  `address1_employmentdetails` text NOT NULL,
  `address2_employmentdetails` text NOT NULL,
  `address3_employmentdetails` text NOT NULL,
  `postcode_employmentdetails` text NOT NULL,
  `city_employmentdetails` text NOT NULL,
  `state_employmentdetails` text NOT NULL,
  `document_id_doc_details` text NOT NULL,
  `type_of_doc_doc_details` text NOT NULL,
  `doc_img_doc_details` text NOT NULL,
  `place_of_issue_doc_details` text NOT NULL,
  `doc_issued_date_doc_details` text NOT NULL,
  `doc_exp_date_doc_details` text NOT NULL,
  `country_of_issuing_doc_doc_details` text NOT NULL,
  `doc_status_doc_details` text NOT NULL,
  `status_of_current_doc_doc_details` text NOT NULL,
  `document_no_doc_details` text NOT NULL,
  `worker_name_family_member` text NOT NULL,
  `relationship_family_member` text NOT NULL,
  `name_of_family_member` text NOT NULL,
  `family_name_family_member` text NOT NULL,
  `is_family_member_together_family_member` text NOT NULL,
  `poe_family_member` text NOT NULL,
  `citizenship_family_member` text NOT NULL,
  `religion_family_member` text NOT NULL,
  `maritial_status_family_member` text NOT NULL,
  `gender_family_member` text NOT NULL,
  `address_1_family_member` text NOT NULL,
  `address_2_family_member` text NOT NULL,
  `address_3_family_member` text NOT NULL,
  `postcode_family_member` text NOT NULL,
  `city_family_member` text NOT NULL,
  `state_family_member` text NOT NULL,
  `contact_no_family_member` text NOT NULL,
  `race_family_member` text NOT NULL,
  `place_of_birth_family_member` text NOT NULL,
  `emplyement_status_family_member` text NOT NULL,
  `employement_name_family_member` text NOT NULL,
  `employement_address_family_member` text NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `full_form`
--

INSERT INTO `full_form` (`id`, `form_id`, `created_by`, `created_time`, `completed_at`, `form_status`, `form_made_on_platform`, `form_fill_start_time`, `form_fill_end_time`, `form_fill_date_start`, `form_fill_date_end`, `form_last_fill_position`, `is_aps_completed`, `is_add_employer_completed`, `is_add_branch_loc_completed`, `is_add_worker_list_completed`, `is_add_dependent_completed`, `agensi_pekerjaan_aps`, `license_category_aps`, `postcode_aps`, `office_telephone_no_aps`, `new_ssm_number_aps`, `address_1_aps`, `city_aps`, `mobile_number_aps`, `old_ssm_number_aps`, `address_2_aps`, `state_aps`, `email_aps`, `aps_license_no`, `address_3_aps`, `license_expr_date_aps`, `contact_person_aps`, `company_name_employer`, `new_ssm_number_employer`, `old_ssm_number_employer`, `address_1_employer`, `address_2_employer`, `address_3_employer`, `postcode__employer`, `city_employer`, `state_employer`, `office_telephone_no_employer`, `mobile_no_employer`, `fax_no_employer`, `yr_of_buss_comm_employer`, `sector_employer`, `name_of_pes_incharge_employer`, `designation_employer`, `pic_mob_no_employer`, `employment_loc_name_location`, `address_1_location`, `address_2_location`, `address_3_location`, `postcode_location`, `state_location`, `city_location`, `office_telephpone_no_location`, `office_mob_no_location`, `email_location`, `name_of_pers_incharge_location`, `designation_location`, `pic_mob_no_location`, `name_of_worker_WorkerList`, `family_name_WorkerList`, `gender_WorkerList`, `d_o_b_WorkerList`, `place_of_birth_WorkerList`, `citizenship_WorkerList`, `maritial_status_WorkerList`, `p_o_e_WorkerList`, `religion_WorkerList`, `race_WorkerList`, `worker_contact_no_WorkerList`, `worker_email_WorkerList`, `nok__WorkerList`, `relationship_WorkerList`, `nok_contact_no_WorkerList`, `job_sector_employmentdetails`, `job_sub_sector_employmentdetails`, `job_status_sponsor_employmentdetails`, `address1_employmentdetails`, `address2_employmentdetails`, `address3_employmentdetails`, `postcode_employmentdetails`, `city_employmentdetails`, `state_employmentdetails`, `document_id_doc_details`, `type_of_doc_doc_details`, `doc_img_doc_details`, `place_of_issue_doc_details`, `doc_issued_date_doc_details`, `doc_exp_date_doc_details`, `country_of_issuing_doc_doc_details`, `doc_status_doc_details`, `status_of_current_doc_doc_details`, `document_no_doc_details`, `worker_name_family_member`, `relationship_family_member`, `name_of_family_member`, `family_name_family_member`, `is_family_member_together_family_member`, `poe_family_member`, `citizenship_family_member`, `religion_family_member`, `maritial_status_family_member`, `gender_family_member`, `address_1_family_member`, `address_2_family_member`, `address_3_family_member`, `postcode_family_member`, `city_family_member`, `state_family_member`, `contact_no_family_member`, `race_family_member`, `place_of_birth_family_member`, `emplyement_status_family_member`, `employement_name_family_member`, `employement_address_family_member`) VALUES
(1, 'swims-bio-111', 'amsonlyfarhan19@gmail.com', '05:58', '27-02-2023', 'filling', 'android', '05:58', '', '27-02-2023', '', '1/2', 'yes', 'no', 'no', 'no', 'no', 'demo name', 'License A', '226020', '05226525140', '123456', 'tedhi pulia ring road', 'lucknow', '9795331109', '098786', 'tedhi pulia ring road', 'uttar pradesh', 'mohdfarhantahir@gmail.com', '1417', 'tedhi pulia ring road', '22-02-2025', '9839076240', 'nigella softwares', '1417', '42342', 'tedhi pulia ring road', 'tedhi pulia ring road', 'tedhi pulia ring road', '226020', 'lko', 'up', '0522-897989', '9839271417', '055-2222', '2023', 'plantation', 'yeoh em ling', 'suervisor', '99799989', 'lko', 'tedhi pulia ring road', 'tedhi pulia ring road', 'tedhi pulia ring road', '226020', 'up', 'lko', '0633431', '3425443', 'someemail@demo.com', 'syaiful', 'malaysia', '+61-224242-24242', 'demo name', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
(2, 'swims-bio-222', 'Mohd Rais Siddiqui', '04:42', '01-03-2023', 'Completed', 'Windows', '04:43', 'NA', '01-03-2023', 'NA', '1/4', 'NA', 'NA', 'NA', 'NA', 'NA', 'mohd rais', 'plantation', '226021', '0522-6525140', '0001111', 'my address 1', 'my city', '000000000', '11111111', 'my address 2', 'lucknow', 'raissiddqiui721@gmail.com', '1234456678', 'my address 3', '02-03-2025', '9898989898', '000000099999', '121212121', '12213312312', 'my address 1 emp', 'my address 2 emp', 'my adddress 3 emp', '776767', 'lucknow', 'uttar pradesh', '0522-121212', '9909090909', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Mohd Rais', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
(3, 'swims-bio-333', 'some random', '05:29', 'NA', 'NA', '', '', '', '', '', '', '', '', '', '', '', 'yeoh', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'yeoh', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
(131, '1231wq1q12323', 'Mohd Farhan Tahir 12', '01:45', 'NA', 'pending', 'android', '01:46', 'NA', '04-03-2023', 'NA', 'APS', 'No', 'No', 'No', 'No', 'No', 'NiGELLA SOFTWARES', 'checking', '22222', '0522-232323', '98232323', 'tedhi puliya', 'lko', '999999', 'ewrr', 'NiGELLA SOFTWARES 1', 'NiGELLA SOFTWARES 2', 'NiGELLA SOFTWARES 3', 'NiGELLA SOFTWARES 4', 'NiGELLA SOFTWARES 5', 'NiGELLA SOFTWARES 6', 'NiGELLA SOFTWARES 7', 'NiGELLA SOFTWARES 8', 'NiGELLA SOFTWARES 9', 'NiGELLA SOFTWARES 10', 'NiGELLA SOFTWARES 12', 'NiGELLA SOFTWARES 13', 'NiGELLA SOFTWARES 14', 'NiGELLA SOFTWARES 15', 'NiGELLA SOFTWARES 16', 'NiGELLA SOFTWARES 17', 'NiGELLA SOFTWARES 18', 'NiGELLA SOFTWARES 19', 'NiGELLA SOFTWARES 20', 'NiGELLA SOFTWARES 21', 'NiGELLA SOFTWARES 22', 'NiGELLA SOFTWARES 23', 'NiGELLA SOFTWARES 24', 'NiGELLA SOFTWARES 25', 'NiGELLA SOFTWARES 26', 'NiGELLA SOFTWARES 27', 'NiGELLA SOFTWARES 28', 'NiGELLA SOFTWARES 29', 'NiGELLA SOFTWARES 30', 'NiGELLA SOFTWARES 31', 'NiGELLA SOFTWARES 32', 'NiGELLA SOFTWARES 33', 'NiGELLA SOFTWARES 34', 'NiGELLA SOFTWARES 35', 'NiGELLA SOFTWARES 36', 'dsdsd', 'dsdswewew', 'sds', 'postmane 14', 'postmane 13', 'postmane 12', 'postmane 11', 'postmane 10', 'postmane 9', 'postmane 8', 'postmane 7', 'postmane 6', 'postmane 5', 'postmane 4', 'postmane 3', 'postmane 2', 'postmane 1', 'POSTMAN 1', 'POSTMAN 2', 'POSTMAN 3', 'POSTMAN 4', 'POSTMAN 5', 'POSTMAN 6', 'POSTMAN 7', 'POSTMAN 8', 'POSTMAN 9', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
(132, '1231wq1q123231212', 'Mohd Farhan Tahir 12', '01:45', 'NA', 'pending', 'android', '01:46', 'NA', '04-03-2023', 'NA', 'APS', 'No', 'No', 'No', 'No', 'No', 'NiGELLA SOFTWARES', 'checking', '22222', '0522-232323', '98232323', 'tedhi puliya', 'lko', '999999', 'ewrr', 'NiGELLA SOFTWARES 1', 'NiGELLA SOFTWARES 2', 'NiGELLA SOFTWARES 3', 'NiGELLA SOFTWARES 4', 'NiGELLA SOFTWARES 5', 'NiGELLA SOFTWARES 6', 'NiGELLA SOFTWARES 7', 'NiGELLA SOFTWARES 8', 'NiGELLA SOFTWARES 9', 'NiGELLA SOFTWARES 10', 'NiGELLA SOFTWARES 12', 'NiGELLA SOFTWARES 13', 'NiGELLA SOFTWARES 14', 'NiGELLA SOFTWARES 15', 'NiGELLA SOFTWARES 16', 'NiGELLA SOFTWARES 17', 'NiGELLA SOFTWARES 18', 'NiGELLA SOFTWARES 19', 'NiGELLA SOFTWARES 20', 'NiGELLA SOFTWARES 21', 'NiGELLA SOFTWARES 22', 'NiGELLA SOFTWARES 23', 'NiGELLA SOFTWARES 24', 'NiGELLA SOFTWARES 25', 'NiGELLA SOFTWARES 26', 'NiGELLA SOFTWARES 27', 'NiGELLA SOFTWARES 28', 'NiGELLA SOFTWARES 29', 'NiGELLA SOFTWARES 30', 'NiGELLA SOFTWARES 31', 'NiGELLA SOFTWARES 32', 'NiGELLA SOFTWARES 33', 'NiGELLA SOFTWARES 34', 'NiGELLA SOFTWARES 35', 'NiGELLA SOFTWARES 36', 'dsdsd', 'dsdswewew', 'sds', 'postmane 14', 'postmane 13', 'postmane 12', 'postmane 11', 'postmane 10', 'postmane 9', 'postmane 8', 'postmane 7', 'postmane 6', 'postmane 5', 'postmane 4', 'postmane 3', 'postmane 2', 'postmane 1', 'POSTMAN 1', 'POSTMAN 2', 'POSTMAN 3', 'POSTMAN 4', 'POSTMAN 5', 'POSTMAN 6', 'POSTMAN 7', 'POSTMAN 8', 'POSTMAN 9', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
(133, '1231wq1q123231212-900', 'Mohd Farhan Tahir 12', '01:45', 'NA', 'pending', 'android', '01:46', 'NA', '04-03-2023', 'NA', 'APS', 'No', 'No', 'No', 'No', 'No', 'NiGELLA SOFTWARES', 'checking', '22222', '0522-232323', '98232323', 'tedhi puliya', 'lko', '999999', 'ewrr', 'NiGELLA SOFTWARES 1', 'NiGELLA SOFTWARES 2', 'NiGELLA SOFTWARES 3', 'NiGELLA SOFTWARES 4', 'NiGELLA SOFTWARES 5', 'NiGELLA SOFTWARES 6', 'NiGELLA SOFTWARES 7', 'NiGELLA SOFTWARES 8', 'NiGELLA SOFTWARES 9', 'NiGELLA SOFTWARES 10', 'NiGELLA SOFTWARES 12', 'NiGELLA SOFTWARES 13', 'NiGELLA SOFTWARES 14', 'NiGELLA SOFTWARES 15', 'NiGELLA SOFTWARES 16', 'NiGELLA SOFTWARES 17', 'NiGELLA SOFTWARES 18', 'NiGELLA SOFTWARES 19', 'NiGELLA SOFTWARES 20', 'NiGELLA SOFTWARES 21', 'NiGELLA SOFTWARES 22', 'NiGELLA SOFTWARES 23', 'NiGELLA SOFTWARES 24', 'NiGELLA SOFTWARES 25', 'NiGELLA SOFTWARES 26', 'NiGELLA SOFTWARES 27', 'NiGELLA SOFTWARES 28', 'NiGELLA SOFTWARES 29', 'NiGELLA SOFTWARES 30', 'NiGELLA SOFTWARES 31', 'NiGELLA SOFTWARES 32', 'NiGELLA SOFTWARES 33', 'NiGELLA SOFTWARES 34', 'NiGELLA SOFTWARES 35', 'NiGELLA SOFTWARES 36', 'dsdsd', 'dsdswewew', 'sds', 'postmane 14', 'postmane 13', 'postmane 12', 'postmane 11', 'postmane 10', 'postmane 9', 'postmane 8', 'postmane 7', 'postmane 6', 'postmane 5', 'postmane 4', 'postmane 3', 'postmane 2', 'postmane 1', 'POSTMAN 1', 'POSTMAN 2', 'POSTMAN 3', 'POSTMAN 4', 'POSTMAN 5', 'POSTMAN 6', 'POSTMAN 7', 'POSTMAN 8', 'POSTMAN 9', 'POSTMAN 11', 'POSTMAN 12', 'POSTMAN 13', 'POSTMAN 14', 'POSTMAN 15', 'POSTMAN 16', 'POSTMAN 17', 'POSTMAN 18', 'POSTMAN 19', 'POSTMAN 20', 'POSTMAN 21', 'POSTMAN 22', 'POSTMAN 23', 'POSTMAN 24', 'POSTMAN 25', 'POSTMAN 26', 'POSTMAN 27', 'POSTMAN 28', 'POSTMAN 29', 'POSTMAN 30', 'POSTMAN 31', 'POSTMAN 32', 'POSTMAN 33', 'POSTMAN 34', 'POSTMAN 35', 'POSTMAN 36', 'POSTMAN 37', 'POSTMAN 38', 'POSTMAN 39', 'POSTMAN 40', 'POSTMAN 41', 'POSTMAN 42'),
(145, 'tvyfn', 'amsonlyfarhan19@gmail.com', '4:56 PM', 'N/A', 'Started', 'Android', '4:56 PM', 'N/A', '09-03-2023', 'N/A', '4/5', 'Yes', 'N/A', 'N/A', 'N/A', 'N/A', 'dfff', '53', '225', '5525', '555', 'fcggv', 'city 3', '9795331125866', '99988', 'ccc.    hhh', 'state!', 'dvvv', 'ghhbb', 'ghbbbb', 'fvbbb', 'hhh bhh j', 'ghhh', 'ghgh', '55555', 'vbbbbbggggg', 'vvvvhgg', 'vvvvbbbvbbh', '2586080', 'city 3', 'state!', 'ghhh', '97953311090', 'ghhhh', 'ggggg', 'Pertanian', 'vbbhh', 'ghghh', '979543223456678', 'ghhhhgghhh', 'ghhhgggg', 'bbbbb bhh', 'hhhhh hhh', '999998', 'state!', 'city 1', '85588', '979533110899', 'dggg', 'gggg', 'ghh', '97953311090', 'demo nameggg', 'gggg', 'PEREMPUAN', 'ghh', 'ggggg', 'Afghanistan', 'BUJANG', 'KOTA KINABALU', 'ISLAM', 'TIDA MAKLUMAT', '979533110895', 'dfgg', 'vhghh', 'Suami', '979533110665', 'Pertanian', 'hhh', 'Jaminan Majikah', 'hhhh', 'gggggg', 'gghhhh', '66988', 'city 2', 'ada', 'X]G^Ti@wYTTT+?=>', 'Passport', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_06a748f0-5ecc-408e-a2fa-774f6e4160045725904554953342162.jpg', 'tyyh', 'hhh', 'yyyy', 'Afghanistan', 'Passport', 'Passport', 'ghhhh', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'),
(146, 'o^_xY', 'amsonlyfarhan19@gmail.com', '5:18 PM', 'N/A', 'Started', 'Android', '5:18 PM', 'N/A', '09-03-2023', 'N/A', '4/5', 'Yes', 'N/A', 'N/A', 'N/A', 'N/A', 'ghhh', '58', '2558', '9966', '2255', 'ghhh hhh', 'city 4', '9795331109', '258', 'ghhh', 'ada', 'fggg', 'ghh', 'gggg', 'ghyh', 'ghhh', 'gggg', 'gggg', '6666', 'cvvv', 'fgggg', 'gygg', '3633', 'city 1', 'ada', 'ghh', '97953311098', 'ggg', 'tyy', 'Pertanian', 'gggg', 'tttt', '97953311098', 'tyyh', 'tyyyy', 'yyyy', 'fgghgf', '5588', 'ada', 'city 1', '55588', '979533110888', 'fgg', 'ccgf', 'gyyy', 'Oiouttrrffvv', 'fggvv', 'ghhh', 'LELAKI', 'gggg', 'yhyy', 'Afghanistan', 'BUJANG', 'KOTA KINABALU', 'ISLAM', 'TIDA MAKLUMAT', '979533118550', 'fghhghgghhggfffddfffffffffffffff', 'ghgfdgg', 'Suami', '9795331108505', 'Pertanian', 'ghgv', 'Jaminan Majikah', 'ggggggg', 'gggggg', 'gggggg', '55588', 'city 1', 'ada', '?yDi+glW%m@e5W1=', 'Marriage cerificate', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_b7c5aaa0-685b-44e6-ae1e-b2c67ba19cc84090251206080213096.jpg', 'tggg', 'vhhg', 'ggggg', 'Afghanistan', 'Marriage cerificate', 'Marriage cerificate', 'hhhhhhh', 'hhhhh', 'Isteri', 'ghhh', 'bhhh', 'no 2', 'SABDAKAN', 'Australia', 'KRITIAN', 'BUJANG', 'PEREMPUAN', 'gggg', 'fgggg', 'gyggg', '666588', 'city 3', 'ada', '979655444444', 'MELAYU', 'yhhhh', 'Employment status 2', 'yuhhhg', 'ghgggg'),
(147, 'yel`x', 'amsonlyfarhan19@gmail.com', '5:28 PM', 'N/A', 'Started', 'Android', '5:28 PM', 'N/A', '09-03-2023', 'N/A', '4/5', 'Yes', 'N/A', 'N/A', 'N/A', 'N/A', 'agendi hjj', 'license @', '2226820', '0822655', '36985', 'hello how are you?', 'city 1', '9795331109', '31248', 'my address 2 ', 'ada', 'email', '577ni', '&++( address 3 ', '688 license no', 'contact person ', 'company name', 'new SSM number', '369988', 'adreless 1', 'address 2\n\nhjjj', 'adreless 3 ', '226650', 'city 2', 'ada', 'office telephone no', '979533110899', 'fax no', 'yuii', 'Pertanian', 'name of person in charge ', 'designation ', '979533110899', 'employment location name', 'address 1', 'address 2', 'address 23', '3668', 'ada', 'city 4', '97953656664', '9869856943799', 'anmsm', 'nnnn', 'nnmnn', '089899777930304', 'name of erolrr', 'jjjj', 'PEREMPUAN', 'hjjk', 'hjjj', 'Afghanistan', 'BUJANG', 'KOTA KINABALU', 'ISLAM', 'TIDA MAKLUMAT', '98999855699885', 'ghbb', 'vhbbbnn hjjnn. hjjn. hj', 'Suami', '566699999999999', 'Pertanian', 'hhjxjj', 'Jaminan Majikah', 'address 1 ', 'address 2 ', 'adreless 3 ', '66999', 'city 2', 'state!', ']AJ=[@pe[u#k@j=k', 'Marriage cerificate', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_faae8b9d-3542-4b3b-bc2b-9d8c56a18fa37987443900892156566.jpg', 'bhbb', 'hj', 'yuuu', 'Australia', 'Marriage cerificate', 'Marriage cerificate', 'hjjj', 'worker namem', 'Suami', 'njdkmd', 'jjjk', 'no 2', 'KOTA KINABALU', 'Afghanistan', 'KRITIAN', 'BUJANG', 'LELAKI', 'address 1 ', 'address 2 ', 'address 3 ', '55888', 'city 4', 'state!', '9796331178899', 'MELAYU', 'hjjj', 'Employement status 1', 'bbbb', 'hhjjjj'),
(148, 'orwch', 'amsonlyfarhan19@gmail.com', '6:08 PM', 'N/A', 'Started', 'Android', '6:08 PM', 'N/A', '09-03-2023', 'N/A', '4/5', 'Yes', 'N/A', 'N/A', 'N/A', 'N/A', 'Tariq Masood', 'test 8', '2558', '9666', '9666', 'ghggh', 'city 2', '9898555555', '6999', 'hhhjjj', 'state!', 'hhjj', 'uuiii', 'uijj', 'jikkk', 'hijkk', 'hjjjj', 'iioo', '63', 'hhjjj', 'jijjj', 'uiik', '3666', 'city 2', 'state!', 'jjjkk', 'jhjjjjjjjjjjjj', 'kkkkkk', 'jjjj', 'Pertanian', 'kkkkk', 'iiooo', 'jkkkkkjkjjjjjkkkk', 'jjjkkkk', 'jkkkkk', 'iiiiok', 'ioooo', '33', 'state!', 'city 1', '669999', '99999999999999988', 'hhjjj', 'uiiii', 'ioopok', 'jjjjjjjjjjjjkkk', 'hhjjj', 'kikkkkk', 'LELAKI', 'kkkj', 'uuuuu', 'Australia', 'BERKAHWIN', 'SABDAKAN', 'KRITIAN', 'TIDA MAKLUMAT', '999999999999996', 'ghjjj', 'hjjjjj', 'Suami', '999999999999999', 'Pertanian', 'iiiii', 'Berkerja Sendiri', 'jjjjjk', 'iiiook', 'iooooko', '66666', 'city 3', 'state!', 'k%K72N5oJ?Fi#CC@', 'Passport', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_1dfd060b-ff5b-40f1-b357-47d27a92bfee564540287394040930.jpg', 'hjjjj', 'kkkk', 'uiiii', 'Australia', 'Passport', 'Passport', 'mmmkk', 'iiiii', 'Suami', 'jjkkk', 'iiioo', 'no 2', 'SABDAKAN', 'Australia', 'KRITIAN', 'BERKAHWIN', 'PEREMPUAN', 'jjkk', 'kkkkk', 'iopool', '3', 'city 3', 'state!', 'jjjkkkkkkkkkkk', 'MELAYU', 'kooooooo', 'Employment status 2', 'iioo', 'kkkkkk'),
(149, 'kse[a', 'amsonlyfarhan19@gmail.com', '6:31 PM', 'N/A', 'Started', 'Android', '6:31 PM', 'N/A', '09-03-2023', 'N/A', '4/5', 'Yes', 'N/A', 'N/A', 'N/A', 'N/A', 'riyaz', 'test 7', '3699', '999', '9999', 'my address ', 'city 3', '9795331109', '366', 'ghnnn', 'ada', 'son', 'hjjj', 'bnnnn', 'nnnn', 'nnnnnnnn', 'my company name ', 'hjn', '699999999', 'bbnbb', 'bnnn', 'bnnn', '6666', 'city 2', 'state!', 'bbbb', 'hhjjjjjjjjjjjjj', 'hhhn', 'nnn', 'Perladangan', 'bbnn', 'nnn', 'nnnnnnnnnhujvgg', 'bbbn', 'nnnn', 'nnnn', 'nnnn', '9999', 'state!', 'city 1', '999', '9999995568559', 'vhbnn', 'bbbn', 'bbnn', 'bbnnhyxvnhcnm', 'bbnn', 'nnnn', 'PEREMPUAN', 'bnn', 'hhh', 'Afghanistan', 'BUJANG', 'KOTA KINABALU', 'ISLAM', 'TIDA MAKLUMAT', '999856956855', 'gnnn', 'bbb', 'Suami', '9985685688568', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'),
(150, 'rcbwZ', 'amsonlyfarhan19@gmail.com', '5:56 PM', 'N/A', 'Started', 'Android', '5:56 PM', 'N/A', '10-03-2023', 'N/A', '4/5', 'Yes', 'N/A', 'N/A', 'N/A', 'N/A', 'aitraaz', 'test 15', '225022', '053358866', '36988', 'alamat 1', 'city 2', '052265280588', '3688', 'alamat 2', 'state!', 'amsonlyfarhan19@gmail.com', 'no lesen aps', 'alamat 3', 'tarikh tamat lesen', 'orang yang boleh dihubungi', 'nama syarikat', 'no SSM baharu', '280', 'alamat 1', 'alamat 2', 'alamat 3', '25509', 'city 2', 'ada', 'no telefon pejabat', 'no telefon bimbit', 'no faxa', 'tarikh Mila operasi', 'Perladangan', 'nama pegawai', 'jawatan', 'no tel pegawi', 'nama syarikat ', 'alamat 1 ', 'alamat 2 ', 'alamat 3 ', 'poskod', 'state!', 'city 1', 'no telefon pejabat', 'no telefon bimbit', 'emel', 'nama pegawai ', 'jawatan', 'no tel pegawai', 'nama pekerja', 'nama keluaraga', 'LELAKI', '16/02/1990', 'tempat lahir', 'Australia', 'BUJANG', 'KOTA KINABALU', 'ISLAM', 'TIDA MAKLUMAT', '699836698055', 'emel pekerja', 'nama saudara', 'Isteri', 'nok hubungi no', 'Pertanian', 'sub sektor pekerjaan', 'Jaminan Majikah', 'alamat 1 ', 'alamat 2 ', 'alamat 3 ', 'poskod', 'city 2', 'state!', '=/aaF?53^R6Gp^OR', 'Passport', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_b9b7ce9d-2f80-4752-8ede-bd2f551eb2a18076600303082348458.jpg', 'tempat isu', 'tarikh dikeluarkan', 'tarikh luput dokumen', 'Australia', 'Passport', 'Passport', 'dokumen no', 'nama pekerja ', 'Isteri', 'nama ahki keluarga', 'nama keluaraga', 'yes 1', 'KOTA KINABALU', 'Afghanistan', 'ISLAM', 'BUJANG', 'LELAKI', 'alamat 2 ', 'alamat 2 ', 'alamat 3 ', 'poskod', 'city 2', 'state!', 'nombor perhubungan', 'TIDA MAKLUMAT', 'tempat lahir', 'Employement status 1', 'nama pekerjaan', 'alamat perkerjaan'),
(151, 'Y[tfj', 'amsonlyfarhan19@gmail.com', '6:28 PM', 'N/A', 'Started', 'Android', '6:28 PM', 'N/A', '12-03-2023', 'N/A', '3/5', 'Yes', 'N/A', 'N/A', 'N/A', 'N/A', 'mohd rais ', 'fefedf', '226021', '0522651890', '369258', 'puraniya', 'city 2', '9839076240', '369525', 'baari enclave ', 'updated by mobile', 'raissiddiqui721@gmail.com', 'nig1416', 'tedhi puliya ', '10/12/2024', 'Mr yeoh', 'NiGELLA SOFTWARES ', 'nig1417', '9388', 'tedhi puliya ', 'n/a', 'n/a', '226024', 'city 2', 'updated by mobile', '05333678', '9839271417', 'n/a', '2024', 'sector 22', 'Mr mohd rais', 'co-owner', '9839076420', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'updated by mobile', 'city 1', 'n/a', '077567884777', 'n/a', 'n/a', 'n/a', '9839078994', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A');

-- --------------------------------------------------------

--
-- Table structure for table `half_form`
--

CREATE TABLE `half_form` (
  `id` int NOT NULL,
  `form_created_by` varchar(255) NOT NULL,
  `form_created_date` varchar(255) NOT NULL,
  `form_worker_reg_no` varchar(255) NOT NULL,
  `no_family_mem` varchar(255) /*CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci*/ NOT NULL,
  `worker_detail_worker_legal_status` varchar(255) NOT NULL,
  `worker_detail_name_of_worker` varchar(255) NOT NULL,
  `worker_detail_family_name` varchar(255) NOT NULL,
  `worker_detail_gender` varchar(255) NOT NULL,
  `worker_detail_DOB` varchar(255) NOT NULL,
  `worker_detail_place_birth` varchar(255) NOT NULL,
  `worker_detail_citizenship` varchar(255) NOT NULL,
  `worker_detail_marital_status` varchar(255) NOT NULL,
  `worker_detail_poe` varchar(255) NOT NULL,
  `worker_detail_religion` varchar(255) NOT NULL,
  `worker_detail_race` varchar(255) NOT NULL,
  `worker_detail_contact_no` varchar(255) NOT NULL,
  `worker_detail_email` varchar(255) NOT NULL,
  `worker_detail_nok` varchar(255) NOT NULL,
  `worker_detail_relationship` varchar(255) NOT NULL,
  `worker_detail_nok_contact_no` varchar(255) NOT NULL,
  `worker_emp_dtl_job_sector` varchar(255) NOT NULL,
  `worker_emp_dtl_job_sub_sector` varchar(255) NOT NULL,
  `worker_emp_dtl_emp_sponsorship_status` varchar(255) NOT NULL,
  `worker_emp_dtl_address1` varchar(255) NOT NULL,
  `worker_emp_dtl_address2` varchar(255) NOT NULL,
  `worker_emp_dtl_address3` varchar(255) NOT NULL,
  `worker_emp_dtl_postcode` varchar(255) NOT NULL,
  `worker_emp_dtl_city` varchar(255) NOT NULL,
  `worker_emp_dtl_state` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_id` varchar(255) NOT NULL,
  `worker_doc_dtl_type_of_doc` varchar(255) NOT NULL,
  `worker_doc_dtl_no_of_doc` varchar(255) NOT NULL,
  `worker_doc_dtl_images_path_email` varchar(255) NOT NULL,
  `worker_doc_dtl_place_of_issue` varchar(255) NOT NULL,
  `worker_doc_dtl_issue_date` varchar(255) NOT NULL,
  `worker_doc_dtl_expiry_date` varchar(255) NOT NULL,
  `worker_doc_dtl_country_doc_issued` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_status` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_current_status` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_no` varchar(255) NOT NULL,
  `form_position` varchar(255) NOT NULL,
  `form_status` varchar(255) NOT NULL,
  `form_unique_key` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `half_form`
--

INSERT INTO `half_form` (`id`, `form_created_by`, `form_created_date`, `form_worker_reg_no`, `no_family_mem`, `worker_detail_worker_legal_status`, `worker_detail_name_of_worker`, `worker_detail_family_name`, `worker_detail_gender`, `worker_detail_DOB`, `worker_detail_place_birth`, `worker_detail_citizenship`, `worker_detail_marital_status`, `worker_detail_poe`, `worker_detail_religion`, `worker_detail_race`, `worker_detail_contact_no`, `worker_detail_email`, `worker_detail_nok`, `worker_detail_relationship`, `worker_detail_nok_contact_no`, `worker_emp_dtl_job_sector`, `worker_emp_dtl_job_sub_sector`, `worker_emp_dtl_emp_sponsorship_status`, `worker_emp_dtl_address1`, `worker_emp_dtl_address2`, `worker_emp_dtl_address3`, `worker_emp_dtl_postcode`, `worker_emp_dtl_city`, `worker_emp_dtl_state`, `worker_doc_dtl_doc_id`, `worker_doc_dtl_type_of_doc`, `worker_doc_dtl_no_of_doc`, `worker_doc_dtl_images_path_email`, `worker_doc_dtl_place_of_issue`, `worker_doc_dtl_issue_date`, `worker_doc_dtl_expiry_date`, `worker_doc_dtl_country_doc_issued`, `worker_doc_dtl_doc_status`, `worker_doc_dtl_doc_current_status`, `worker_doc_dtl_doc_no`, `form_position`, `form_status`, `form_unique_key`) VALUES
(1, '2423', '21/05/2023', '000003', '252fdgs', 'illegal', 'Akash', '2rewwr', 'worker_detail_gender', '11/05/1998', 'UP', 'citizenship', 'worker_detail_marital_status', 'worker_detail_poe', 'worker_detail_religion', 'worker_detail_race', 'worker_detail_contact_no', 'worker_detail_email', 'worker_detail_nok', 'worker_detail_relationship', 'worker_detail_nok_contact_no', 'worker_emp_dtl_job_sector', 'worker_emp_dtl_job_sub_sector', 'worker_emp_dtl_emp_sponsorship_status', 'worker_emp_dtl_address1', 'worker_emp_dtl_address2', 'worker_emp_dtl_address3', 'worker_emp_dtl_postcode', 'worker_emp_dtl_city', 'worker_emp_dtl_state', 'worker_doc_dtl_doc_id', 'worker_doc_dtl_type_of_doc', 'worker_doc_dtl_no_of_doc', 'worker_doc_dtl_images_path_email', 'worker_doc_dtl_place_of_issue', 'worker_doc_dtl_issue_date', 'worker_doc_dtl_expiry_date', 'worker_doc_dtl_country_doc_issued', 'worker_doc_dtl_doc_status', 'worker_doc_dtl_doc_current_status', 'worker_doc_dtl_doc_no', 'form_position', 'form_status', 'form_unique_key'),
(2, '2423', '21/05/2023', '000001', '252fdgs', 'legal', 'Vijay', '2rewwr', 'worker_detail_gender', 'worker_detail_DOB', 'worker_detail_place_birth', 'worker_detail_citizenship', 'worker_detail_marital_status', 'worker_detail_poe', 'worker_detail_religion', 'worker_detail_race', 'worker_detail_contact_no', 'worker_detail_email', 'worker_detail_nok', 'worker_detail_relationship', 'worker_detail_nok_contact_no', 'worker_emp_dtl_job_sector', 'worker_emp_dtl_job_sub_sector', 'worker_emp_dtl_emp_sponsorship_status', 'worker_emp_dtl_address1', 'worker_emp_dtl_address2', 'worker_emp_dtl_address3', 'worker_emp_dtl_postcode', 'worker_emp_dtl_city', 'worker_emp_dtl_state', 'worker_doc_dtl_doc_id', 'worker_doc_dtl_type_of_doc', 'worker_doc_dtl_no_of_doc', 'worker_doc_dtl_images_path_email', 'worker_doc_dtl_place_of_issue', 'worker_doc_dtl_issue_date', 'worker_doc_dtl_expiry_date', 'worker_doc_dtl_country_doc_issued', 'worker_doc_dtl_doc_status', 'worker_doc_dtl_doc_current_status', 'worker_doc_dtl_doc_no', 'form_position', 'form_status', 'vbn'),
(3, '2423', '21/05/2023', '0000002', '252fdgs', 'illegal', 'Alakh', '2rewwr', 'worker_detail_gender', 'worker_detail_DOB', 'worker_detail_place_birth', 'worker_detail_citizenship', 'worker_detail_marital_status', 'worker_detail_poe', 'worker_detail_religion', 'worker_detail_race', 'worker_detail_contact_no', 'worker_detail_email', 'worker_detail_nok', 'worker_detail_relationship', 'worker_detail_nok_contact_no', 'worker_emp_dtl_job_sector', 'worker_emp_dtl_job_sub_sector', 'worker_emp_dtl_emp_sponsorship_status', 'worker_emp_dtl_address1', 'worker_emp_dtl_address2', 'worker_emp_dtl_address3', 'worker_emp_dtl_postcode', 'worker_emp_dtl_city', 'worker_emp_dtl_state', 'worker_doc_dtl_doc_id', 'worker_doc_dtl_type_of_doc', 'worker_doc_dtl_no_of_doc', 'worker_doc_dtl_images_path_email', 'worker_doc_dtl_place_of_issue', 'worker_doc_dtl_issue_date', 'worker_doc_dtl_expiry_date', 'worker_doc_dtl_country_doc_issued', 'worker_doc_dtl_doc_status', 'worker_doc_dtl_doc_current_status', 'worker_doc_dtl_doc_no', 'form_position', 'form_status', 'vbn1');

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `id` int NOT NULL,
  `aps_agency_pekerjaan` varchar(255) NOT NULL,
  `aps_license_category` varchar(255) NOT NULL,
  `aps_postcode` varchar(255) NOT NULL,
  `aps_office_telephone_no` varchar(20) NOT NULL,
  `aps_new_ssm_number` varchar(255) NOT NULL,
  `aps_address1` text NOT NULL,
  `aps_city` varchar(255) NOT NULL,
  `aps_mobile_number` varchar(20) NOT NULL,
  `aps_old_SSM_number` varchar(20) NOT NULL,
  `aps_address2` text NOT NULL,
  `aps_state` varchar(255) NOT NULL,
  `aps_email` varchar(100) NOT NULL,
  `aps_license_no` varchar(20) NOT NULL,
  `aps_address3` text NOT NULL,
  `aps_license_exp_date` varchar(20) NOT NULL,
  `aps_contact_person` varchar(255) NOT NULL,
  `employer_company_name` varchar(255) NOT NULL,
  `employer_new_ssm_number` varchar(255) NOT NULL,
  `employer_old_ssm_number` varchar(20) NOT NULL,
  `employer_address1` text NOT NULL,
  `employer_address2` text NOT NULL,
  `employer_address3` text NOT NULL,
  `employer_postcode` varchar(20) NOT NULL,
  `employer_city` varchar(255) NOT NULL,
  `employer_state` varchar(255) NOT NULL,
  `employer_office_telephone_no` varchar(20) NOT NULL,
  `employer_mobile_no` varchar(20) NOT NULL,
  `employer_fax_number` varchar(20) NOT NULL,
  `employer_year_of_commence` varchar(20) NOT NULL,
  `employer_sector` varchar(255) NOT NULL,
  `employer_name_of_person_in_charge` text NOT NULL,
  `employer_designation` varchar(255) NOT NULL,
  `employer_pic_mobile_number` varchar(20) NOT NULL,
  `branch_employment_location_name` varchar(255) NOT NULL,
  `branch_address1` text NOT NULL,
  `branch_address2` text NOT NULL,
  `branch_address3` text NOT NULL,
  `branch_postcode` varchar(20) NOT NULL,
  `branch_state` varchar(255) NOT NULL,
  `branch_city` varchar(255) NOT NULL,
  `branch_office_telephone_number` varchar(20) NOT NULL,
  `branch_office_mobile_number` varchar(20) NOT NULL,
  `branch_email` varchar(100) NOT NULL,
  `branch_name_of_person_in_charge` varchar(255) NOT NULL,
  `branch_designation` varchar(255) NOT NULL,
  `branch_pic_mobile_number` varchar(20) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`id`, `aps_agency_pekerjaan`, `aps_license_category`, `aps_postcode`, `aps_office_telephone_no`, `aps_new_ssm_number`, `aps_address1`, `aps_city`, `aps_mobile_number`, `aps_old_SSM_number`, `aps_address2`, `aps_state`, `aps_email`, `aps_license_no`, `aps_address3`, `aps_license_exp_date`, `aps_contact_person`, `employer_company_name`, `employer_new_ssm_number`, `employer_old_ssm_number`, `employer_address1`, `employer_address2`, `employer_address3`, `employer_postcode`, `employer_city`, `employer_state`, `employer_office_telephone_no`, `employer_mobile_no`, `employer_fax_number`, `employer_year_of_commence`, `employer_sector`, `employer_name_of_person_in_charge`, `employer_designation`, `employer_pic_mobile_number`, `branch_employment_location_name`, `branch_address1`, `branch_address2`, `branch_address3`, `branch_postcode`, `branch_state`, `branch_city`, `branch_office_telephone_number`, `branch_office_mobile_number`, `branch_email`, `branch_name_of_person_in_charge`, `branch_designation`, `branch_pic_mobile_number`) VALUES
(3, 'nAP1', 'Category 1', 'guy', 'uyg', 'news', 'gug', 'City 1', 'uyg', 'olds', 'ug', 'State 1', 'uyg@dsfgsd', 'gug', 'ugu', '2023-04-08', 'uyg', 'uyg', 'ygygyuy', 'gug', 'uy', 'guy', 'guyg', 'uyg', 'a', 'a', 'uyg', 'uyg', 'uyg', 'uyg', 'uy', 'guyg', 'ug', 'uyg', 'uyg', 'uyg', 'uyg', 'uy', 'guyg', 'a', 'a', 'uyg', 'uyg', 'uyg@sdfdf', 'uyg', 'uyg12', 'uy');

-- --------------------------------------------------------

--
-- Table structure for table `profile_new`
--

CREATE TABLE `profile_new` (
  `id` int NOT NULL,
  `is_profile_completed` varchar(255) NOT NULL,
  `profile_registered_email` varchar(255) NOT NULL,
  `profile_registered_password` varchar(255) NOT NULL,
  `profile_registration_date` varchar(255) NOT NULL,
  `device_status_online` varchar(255) NOT NULL,
  `user_status` varchar(255) NOT NULL,
  `platform` varchar(255) NOT NULL,
  `push_token` varchar(255) NOT NULL,
  `user_guid` varchar(255) NOT NULL,
  `aps_agensi_pekerjaan` varchar(255) NOT NULL,
  `aps_license_category` varchar(255) NOT NULL,
  `aps_new_ssm_no` varchar(255) NOT NULL,
  `aps_old_ssm_no` varchar(255) NOT NULL,
  `aps_licence_no` varchar(255) NOT NULL,
  `aps_lic_exp_date` varchar(255) NOT NULL,
  `aps_email` varchar(255) NOT NULL,
  `aps_address1` varchar(255) NOT NULL,
  `aps_address2` varchar(255) NOT NULL,
  `aps_address3` varchar(255) NOT NULL,
  `aps_postcode` varchar(255) NOT NULL,
  `aps_city` varchar(255) NOT NULL,
  `aps_state` varchar(255) NOT NULL,
  `aps_mobile_no` varchar(255) NOT NULL,
  `aps_office_tele_no` varchar(255) NOT NULL,
  `emp_company_name` varchar(255) NOT NULL,
  `emp_new_ssm_no` varchar(255) NOT NULL,
  `emp_old_ssm_no` varchar(255) NOT NULL,
  `emp_address1` varchar(255) NOT NULL,
  `emp_address2` varchar(255) NOT NULL,
  `emp_address3` varchar(255) NOT NULL,
  `emp_postcode` varchar(255) NOT NULL,
  `emp_city` varchar(255) NOT NULL,
  `emp_state` varchar(255) NOT NULL,
  `emp_office_tele_no` varchar(255) NOT NULL,
  `emp_mobile_no` varchar(255) NOT NULL,
  `emp_fax_no` varchar(255) NOT NULL,
  `emp_year_of_commence` varchar(255) NOT NULL,
  `emp_sector` varchar(255) NOT NULL,
  `emp_name_of_person_incharge` varchar(255) NOT NULL,
  `emp_designation` varchar(255) NOT NULL,
  `emp_pic_mobile_no` varchar(255) NOT NULL,
  `branch_emp_loc_name` varchar(255) NOT NULL,
  `branch_address1` varchar(255) NOT NULL,
  `branch_address2` varchar(255) NOT NULL,
  `branch_address3` varchar(255) NOT NULL,
  `branch_postcode` varchar(255) NOT NULL,
  `branch_state` varchar(255) NOT NULL,
  `branch_city` varchar(255) NOT NULL,
  `branch_office_tele_no` varchar(255) NOT NULL,
  `branch_office_mob_no` varchar(255) NOT NULL,
  `branch_email` varchar(255) NOT NULL,
  `branch_name_of_person_incharge` varchar(255) NOT NULL,
  `branch_designation` varchar(255) NOT NULL,
  `branch_pic_mob_no` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `profile_new`
--

INSERT INTO `profile_new` (`id`, `is_profile_completed`, `profile_registered_email`, `profile_registered_password`, `profile_registration_date`, `device_status_online`, `user_status`, `platform`, `push_token`, `user_guid`, `aps_agensi_pekerjaan`, `aps_license_category`, `aps_new_ssm_no`, `aps_old_ssm_no`, `aps_licence_no`, `aps_lic_exp_date`, `aps_email`, `aps_address1`, `aps_address2`, `aps_address3`, `aps_postcode`, `aps_city`, `aps_state`, `aps_mobile_no`, `aps_office_tele_no`, `emp_company_name`, `emp_new_ssm_no`, `emp_old_ssm_no`, `emp_address1`, `emp_address2`, `emp_address3`, `emp_postcode`, `emp_city`, `emp_state`, `emp_office_tele_no`, `emp_mobile_no`, `emp_fax_no`, `emp_year_of_commence`, `emp_sector`, `emp_name_of_person_incharge`, `emp_designation`, `emp_pic_mobile_no`, `branch_emp_loc_name`, `branch_address1`, `branch_address2`, `branch_address3`, `branch_postcode`, `branch_state`, `branch_city`, `branch_office_tele_no`, `branch_office_mob_no`, `branch_email`, `branch_name_of_person_incharge`, `branch_designation`, `branch_pic_mob_no`) VALUES
(1, 'Yes', 'amsonlyfarhan19@gmail.com', 'kata laun', '', 'Online', '', 'Android', 'eJQqhZCWRhCK5NpZnkTG-r:APA91bHS7FSuF_gsGYs3Whgk2ozYwhU_PguI53qSJk4FtJdeuJWrCY3aCwuZJ4MOw6--ihnpelDrLxycUe152tf2MOCIZjw2suXps-PdB_e-tnv9WGQzA4mhwrkr_1Dt_JhMc5_39LiN', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_b88a5c26-cd71-418d-9b18-ff3deb82994f5622688721089142422.jpg', 'Yeoh nama agency pekerjaan ', 'sdsds', 'no SSM baharu yeoh', 'no SSM lama yeoh', 'no lesen aps yeoh', 'undefined', 'email Yeoh aps', 'alamat 1 aps yeoh', 'alamat 2 aps yeoh ', 'alamat 3 aps yeoh ', 'poskod aps yeoh ', 'city 2', 'updated by mobile', 'no telefon aps bimbit yeoh', 'no telefon pejabat aps yeoh ', 'mohd farhan', 'no SSM baharu majikan yeoh ', 'no SSM lama majikan yeoh ', 'alamat 1 majikan yeoh ', 'alamat 2 majikan yeoh ', 'alamat 3 majikan yeoh ', 'poskod majikan yeoh ', 'city 2', 'state!', 'no telefon pejabat majikan yeoh ', 'no telefon bimbit majikan yeoh ', 'no fax majikan yeoh ', 'tarikh mula operasi majikan yeoh ', 'sector 22', 'nama pegawai majikan yeoh ', 'jawatan majikan yeoh ', 'telefon bimbit pegawaip majikan yeoh ', 'nama syarikat cawangan yeoh', 'alamat 1 cawangan yeoh ', 'alamat 2 cawangan yeoh ', 'alamat 3 cawangan yeoh ', 'poskod cawangan yeoh ', 'state!', 'city 2', 'no telefon pejabat cawangan yeoh ', 'no telefon bimbit pejabat cawangan yeoh ', 'email cawangan yeoh ', 'nama pegawai cawangan yeoh ', 'jawatan cawangan yeoh ', 'no telefon bimbit pegawai cawangan yeoh '),
(2, 'Yes', 'nigellainfotech.com@gmail.com', 'yakeen', '', 'Online', '', 'Android', 'eJQqhZCWRhCK5NpZnkTG-r:APA91bG6BnFkKOcKxUdXn6hz3WcT-PC50FUml4jGkRf3u-nB2XYCABPdOsedJi1W-JQwsziwgPFR9okugfAvjKLyje09yr3FjSVtQHNIyzTo-ZAPnwiDL9h0ZqnkLigkkWN40evsVfny', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_18c49f8b-cd22-4d75-bb7e-ac5b0d1ef7d73749634445620252892.jpg', 'ggg', 'sdsds', 'ghgg', 'ghhh', 'ghh', 'undefined', 'ghgg', 'yuhh', 'uuh', 'hhhh', 'ghg', 'city 2', 'updated by mobile', 'bbhhjjjjjjjjjjj', 'hhhh', 'Syaiful Bahri', 'hhhh', 'yhhh', 'yyyy', 'hhhh', 'yhhh', 'ggh', 'city 1', 'state!', 'hhhh', 'gggg', 'hhhhh', 'ggghhh', 'sector 3', 'gghhh', 'hhhh', 'ghhhh', 'hhhhh', 'yuyu', 'yuuuu', 'hjjj', 'hhjjh', 'updated by mobile', 'city 1', 'ccgg', 'cvvvv', 'vvggg', 'ffgfg', 'hhhhhh', 'fggggg'),
(3, 'Yes', 'yeoh.2007@gmail.com', 'my password', '', 'Online', '', 'Android', 'eJQqhZCWRhCK5NpZnkTG-r:APA91bHS7FSuF_gsGYs3Whgk2ozYwhU_PguI53qSJk4FtJdeuJWrCY3aCwuZJ4MOw6--ihnpelDrLxycUe152tf2MOCIZjw2suXps-PdB_e-tnv9WGQzA4mhwrkr_1Dt_JhMc5_39LiN', '/data/user/0/com.nigellaform.nigellafrom/cache/scaled_a7edc107-a8d4-4e56-b6a3-dba3ec7d54d21687703706219259048.jpg', 'yeoh', 'sdsds', 'yeoh', 'yeoh', 'yeoh', 'undefined', 'yeoh', 'yeoh', 'yeoh', 'yeoh', 'yeoh', 'city 2', 'updated by mobile', 'yeoh', 'yeoh', 'Yeoh Plantation', 'Yeoh 1', 'Yeoh 1', 'Yeoh 1', 'Yeoh 1', 'Yeoh 1', 'Yeoh 1', 'city 3', 'state!', 'Yeoh 1', 'Yeoh 1', 'Yeoh 1', 'Yeoh 1', 'sector 22', 'Yeoh 1', 'Yeoh 1', 'Yeoh 1', 'Yeoh 2', 'Yeoh 2', 'Yeoh 2', 'Yeoh 2', 'Yeoh 2', 'state!', 'city 1', 'Yeoh 2', 'Yeoh 2', 'Yeoh 2', 'Yeoh 2', 'Yeoh 2', 'Yeoh 2'),
(4, 'No', 'rais19@gmail.com', '2331', '30-03-2023', 'Offline', '', 'N/A', 'N/A', 'N/A', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `created_at` varchar(255) NOT NULL,
  `created_time` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `device_status_online` varchar(255) NOT NULL,
  `user_status` varchar(255) NOT NULL,
  `platform` varchar(255) NOT NULL,
  `push_token` varchar(255) NOT NULL,
  `email_verified` varchar(255) NOT NULL,
  `guid` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `red_date` varchar(255) NOT NULL,
  `reg_time` varchar(255) NOT NULL
) /*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `created_at`, `created_time`, `email`, `device_status_online`, `user_status`, `platform`, `push_token`, `email_verified`, `guid`, `username`, `password`, `red_date`, `reg_time`) VALUES
(95, 'Arun Agarwal', '03-03-2023', '12:49 PM', 'agarwalarun1135@gmail.com', 'offline', 'Active', 'Android', 'e_JbaoL7SNSRz7mTfxYOab:APA91bHcpQ-NokhaYZGR4JVxDRwWmKaF95Gkr7J4nFjbjYGZnZCid0soY-Ve0Yo9UqXUepe-AKmlNmqkYqndKpldx5XSqYJdTxvUYa-InqStVyJCjkw_cEWK6OPvBmg_o0ZGEb27gy99', 'true', 'https://lh3.googleusercontent.com/a/AGNmyxYi-Og2OF3AVhG_9UmAt-3MNtv3dPlpa2G6Pqwu=s96-c', '', '', '', ''),
(98, 'Nigella Softwares', '03-03-2023', '7:01 PM', 'nigellainfotech.com@gmail.com', 'online', 'Active', 'iOS', 'cMH5iptPN0n9r-c-YpFqS6:APA91bHLZSFdpOJSxZE-nfaUuf9NoMMjPGMqIMB8VSYM1ZarsgkPTp25ovh8cA-PPUhY2KA62O81F6OWp7KBTSNyzcK08s6ftV4l7SuOia-NMB041iKxDAAvPTPyKzcDXlPGYlTQAWRs', 'true', 'https://lh3.googleusercontent.com/a/AEdFTp7AeqtqqIfUnwrfqoQ6jMyKAlh1aaR-EBviY24_UQ=s96-c', '', '', '', ''),
(99, 'Eng Lim Yeoh', '04-03-2023', '9:56 PM', 'yeoh.2007@gmail.com', 'offline', 'Active', 'Android', 'e2D2BmUpRWSbng2PtIhPgb:APA91bFozOZK84qsFAzTS8HXIILSnvPfs79q6Z0MJjmHIT6kExWKTeC2C-dq4yUT4kyUeaPb9bmGvCXsMl4se34YlIN6Hk7O9tZU2kew8GrJ1-n7SEubfr3dYvyz9QgmZyjxzq_Cyu4r', 'true', 'https://lh3.googleusercontent.com/a/AGNmyxYb8V2DOznmCstalf4UE5Lz3uZQN9FqiEWIdXls8g=s96-c', 'demo', '123456', '', ''),
(101, 'Mohd farhan', '09-03-2023', '6:31 PM', 'amsonlyfarhan19@gmail.com', 'offline', 'Active', 'Android', 'eJQqhZCWRhCK5NpZnkTG-r:APA91bHS7FSuF_gsGYs3Whgk2ozYwhU_PguI53qSJk4FtJdeuJWrCY3aCwuZJ4MOw6--ihnpelDrLxycUe152tf2MOCIZjw2suXps-PdB_e-tnv9WGQzA4mhwrkr_1Dt_JhMc5_39LiN', 'true', 'https://lh3.googleusercontent.com/a/AEdFTp4aMpOszC_3FpZtPSTFvn3ACOOl2x18P02YJ5EoaQ=s96-c', '', '', '', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category_list`
--
ALTER TABLE `category_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `detailed_dd_citizenship`
--
ALTER TABLE `detailed_dd_citizenship`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_city`
--
ALTER TABLE `detailed_dd_city`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_country_issued_doc`
--
ALTER TABLE `detailed_dd_country_issued_doc`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_current_status_doc`
--
ALTER TABLE `detailed_dd_current_status_doc`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_designation`
--
ALTER TABLE `detailed_dd_designation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_doc_status`
--
ALTER TABLE `detailed_dd_doc_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_employement_status`
--
ALTER TABLE `detailed_dd_employement_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_gender`
--
ALTER TABLE `detailed_dd_gender`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_is_dependent_together`
--
ALTER TABLE `detailed_dd_is_dependent_together`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_job_sector`
--
ALTER TABLE `detailed_dd_job_sector`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_job_status_sponsor`
--
ALTER TABLE `detailed_dd_job_status_sponsor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_job_sub_sector`
--
ALTER TABLE `detailed_dd_job_sub_sector`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_license_category`
--
ALTER TABLE `detailed_dd_license_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_maritail_status`
--
ALTER TABLE `detailed_dd_maritail_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_poe`
--
ALTER TABLE `detailed_dd_poe`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_race`
--
ALTER TABLE `detailed_dd_race`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_relationship`
--
ALTER TABLE `detailed_dd_relationship`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_religion`
--
ALTER TABLE `detailed_dd_religion`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_sector`
--
ALTER TABLE `detailed_dd_sector`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_state`
--
ALTER TABLE `detailed_dd_state`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_type_of_doc`
--
ALTER TABLE `detailed_dd_type_of_doc`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `detailed_dd_worker_legal_status`
--
ALTER TABLE `detailed_dd_worker_legal_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `family_form`
--
ALTER TABLE `family_form`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `form_unique_key` (`form_unique_key`);

--
-- Indexes for table `form_image`
--
ALTER TABLE `form_image`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `form_unique_key` (`form_unique_key`);

--
-- Indexes for table `form_worker_registration_no`
--
ALTER TABLE `form_worker_registration_no`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `worker_email` (`worker_email`);

--
-- Indexes for table `full_form`
--
ALTER TABLE `full_form`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `form_id` (`form_id`);

--
-- Indexes for table `half_form`
--
ALTER TABLE `half_form`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `form_unique_key` (`form_unique_key`);

--
-- Indexes for table `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `profile_new`
--
ALTER TABLE `profile_new`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `profile_registered_email` (`profile_registered_email`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category_list`
--
ALTER TABLE `category_list`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `detailed_dd_citizenship`
--
ALTER TABLE `detailed_dd_citizenship`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `detailed_dd_city`
--
ALTER TABLE `detailed_dd_city`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `detailed_dd_country_issued_doc`
--
ALTER TABLE `detailed_dd_country_issued_doc`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `detailed_dd_current_status_doc`
--
ALTER TABLE `detailed_dd_current_status_doc`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `detailed_dd_designation`
--
ALTER TABLE `detailed_dd_designation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `detailed_dd_doc_status`
--
ALTER TABLE `detailed_dd_doc_status`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `detailed_dd_employement_status`
--
ALTER TABLE `detailed_dd_employement_status`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `detailed_dd_gender`
--
ALTER TABLE `detailed_dd_gender`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `detailed_dd_is_dependent_together`
--
ALTER TABLE `detailed_dd_is_dependent_together`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `detailed_dd_job_sector`
--
ALTER TABLE `detailed_dd_job_sector`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `detailed_dd_job_status_sponsor`
--
ALTER TABLE `detailed_dd_job_status_sponsor`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `detailed_dd_job_sub_sector`
--
ALTER TABLE `detailed_dd_job_sub_sector`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `detailed_dd_license_category`
--
ALTER TABLE `detailed_dd_license_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=128;

--
-- AUTO_INCREMENT for table `detailed_dd_maritail_status`
--
ALTER TABLE `detailed_dd_maritail_status`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `detailed_dd_poe`
--
ALTER TABLE `detailed_dd_poe`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `detailed_dd_race`
--
ALTER TABLE `detailed_dd_race`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `detailed_dd_relationship`
--
ALTER TABLE `detailed_dd_relationship`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `detailed_dd_religion`
--
ALTER TABLE `detailed_dd_religion`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `detailed_dd_sector`
--
ALTER TABLE `detailed_dd_sector`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `detailed_dd_state`
--
ALTER TABLE `detailed_dd_state`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `detailed_dd_type_of_doc`
--
ALTER TABLE `detailed_dd_type_of_doc`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `detailed_dd_worker_legal_status`
--
ALTER TABLE `detailed_dd_worker_legal_status`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `family_form`
--
ALTER TABLE `family_form`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `form_image`
--
ALTER TABLE `form_image`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `form_worker_registration_no`
--
ALTER TABLE `form_worker_registration_no`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `full_form`
--
ALTER TABLE `full_form`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=152;

--
-- AUTO_INCREMENT for table `half_form`
--
ALTER TABLE `half_form`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `profile`
--
ALTER TABLE `profile`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `profile_new`
--
ALTER TABLE `profile_new`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
