-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 04, 2018 at 07:53 PM
-- Server version: 5.7.21
-- PHP Version: 7.1.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `MLS_2017`
--

-- --------------------------------------------------------

--
-- Table structure for table `Event`
--

CREATE TABLE `Event` (
  `id` int(11) NOT NULL,
  `game` int(11) NOT NULL,
  `minute` int(3) NOT NULL,
  `type` char(10) NOT NULL,
  `player1` int(11) NOT NULL,
  `player2` int(11) NOT NULL,
  `team` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `Game`
--

CREATE TABLE `Game` (
  `id` int(11) NOT NULL,
  `gamedate` char(25) NOT NULL,
  `home` int(11) NOT NULL,
  `away` int(11) NOT NULL,
  `location` char(50) NOT NULL,
  `attendance` char(50) NOT NULL,
  `referee` char(50) NOT NULL,
  `home_manager` char(50) NOT NULL,
  `away_manager` char(50) NOT NULL,
  `home_formation` char(25) NOT NULL,
  `away_formation` char(25) NOT NULL,
  `home1` int(11) NOT NULL,
  `home2` int(11) NOT NULL,
  `home3` int(11) NOT NULL,
  `home4` int(11) NOT NULL,
  `home5` int(11) NOT NULL,
  `home6` int(11) NOT NULL,
  `home7` int(11) NOT NULL,
  `home8` int(11) NOT NULL,
  `home9` int(11) NOT NULL,
  `home10` int(11) NOT NULL,
  `home11` int(11) NOT NULL,
  `away1` int(11) NOT NULL,
  `away2` int(11) NOT NULL,
  `away3` int(11) NOT NULL,
  `away4` int(11) NOT NULL,
  `away5` int(11) NOT NULL,
  `away6` int(11) NOT NULL,
  `away7` int(11) NOT NULL,
  `away8` int(11) NOT NULL,
  `away9` int(11) NOT NULL,
  `away10` int(11) NOT NULL,
  `away11` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `League`
--

CREATE TABLE `League` (
  `id` char(25) NOT NULL,
  `name` char(25) NOT NULL,
  `country` char(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `League`
--

-- --------------------------------------------------------

--
-- Table structure for table `Player`
--

CREATE TABLE `Player` (
  `id` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `birthdate` char(25) NOT NULL,
  `birthplace` char(50) NOT NULL,
  `birth_country` char(50) NOT NULL,
  `height` int(11) NOT NULL,
  `nat1` char(25) NOT NULL,
  `nat2` char(25) NOT NULL,
  `position` char(3) NOT NULL,
  `team` int(11) NOT NULL,
  `player_number` int(3) NOT NULL,
  `value` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `Team`
--

CREATE TABLE `Team` (
  `id` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `league` char(25) NOT NULL,
  `points` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



--
-- Indexes for dumped tables
--

--
-- Indexes for table `Event`
--
ALTER TABLE `Event`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `Game`
--
ALTER TABLE `Game`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `League`
--
ALTER TABLE `League`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `Player`
--
ALTER TABLE `Player`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `Team`
--
ALTER TABLE `Team`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
