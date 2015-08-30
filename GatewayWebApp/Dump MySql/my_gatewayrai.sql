-- phpMyAdmin SQL Dump
-- version 4.1.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Set 16, 2014 alle 10:17
-- Versione del server: 5.1.71-community-log
-- PHP Version: 5.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `my_gatewayrai`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `app_frame`
--

CREATE TABLE IF NOT EXISTS `app_frame` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `IL` tinyint(3) unsigned NOT NULL,
  `TP` int(10) unsigned NOT NULL,
  `TMR` tinyint(3) unsigned NOT NULL,
  `NRT` tinyint(3) unsigned NOT NULL,
  `DATA` bigint(20) unsigned NOT NULL,
  `COD_FRAME` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `COD_FRAME` (`COD_FRAME`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `app_type`
--

CREATE TABLE IF NOT EXISTS `app_type` (
  `CODE` tinyint(3) unsigned NOT NULL,
  `DESCRIPTION` varchar(50) NOT NULL,
  PRIMARY KEY (`CODE`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `app_type`
--

INSERT INTO `app_type` (`CODE`, `DESCRIPTION`) VALUES
(0, 'REGISTRATION FRAME'),
(1, 'DATA FRAME');

-- --------------------------------------------------------

--
-- Struttura della tabella `frame`
--

CREATE TABLE IF NOT EXISTS `frame` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `TIMESTAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `TYPE` tinyint(3) unsigned NOT NULL,
  `ID_NODE` tinyint(3) unsigned NOT NULL,
  `STATE` tinyint(3) unsigned NOT NULL,
  `COD_RX_DEVICE` tinyint(4) unsigned NOT NULL,
  `CL` tinyint(3) unsigned NOT NULL,
  `BC` tinyint(3) unsigned NOT NULL,
  `ST` tinyint(3) unsigned NOT NULL,
  `TY` tinyint(3) unsigned NOT NULL,
  `RN` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `task`
--

CREATE TABLE IF NOT EXISTS `task` (
  `ID` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `REGISTER` varchar(100) NOT NULL,
  `VALUE` varchar(100) NOT NULL,
  `COD_GATEWAY` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=77 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `uart_state`
--

CREATE TABLE IF NOT EXISTS `uart_state` (
  `CODE` tinyint(3) unsigned NOT NULL,
  `DESCRIPTION` varchar(50) NOT NULL,
  PRIMARY KEY (`CODE`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `uart_state`
--

INSERT INTO `uart_state` (`CODE`, `DESCRIPTION`) VALUES
(174, 'CRC OK'),
(175, 'CRC ERROR'),
(165, 'NODE NOT REGISTERED'),
(172, 'DEAD NODE'),
(173, 'VALID NODE');

-- --------------------------------------------------------

--
-- Struttura della tabella `uart_type`
--

CREATE TABLE IF NOT EXISTS `uart_type` (
  `CODE` tinyint(3) unsigned NOT NULL,
  `DESCRIPTION` varchar(50) NOT NULL,
  PRIMARY KEY (`CODE`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `uart_type`
--

INSERT INTO `uart_type` (`CODE`, `DESCRIPTION`) VALUES
(170, 'ALARM FRAME'),
(255, 'SIGNAL FRAME');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
