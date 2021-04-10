-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 10-04-2021 a las 05:02:52
-- Versión del servidor: 10.4.17-MariaDB
-- Versión de PHP: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `home_sweet_home`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `buys`
--

CREATE TABLE `buys` (
  `id_user` int(12) NOT NULL,
  `id_house` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `disliked`
--

CREATE TABLE `disliked` (
  `id_user` int(12) NOT NULL,
  `id_house` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `has_favorites`
--

CREATE TABLE `has_favorites` (
  `id_user` int(12) NOT NULL,
  `id_house` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `houses`
--

CREATE TABLE `houses` (
  `id` int(12) NOT NULL,
  `owner_id` int(12) NOT NULL,
  `name` varchar(40) NOT NULL,
  `adress` varchar(40) NOT NULL,
  `old_price` int(12) DEFAULT NULL,
  `actual_price` int(12) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `on_sale` tinyint(1) NOT NULL DEFAULT 0,
  `likes` int(12) NOT NULL DEFAULT 0,
  `dislikes` int(12) NOT NULL DEFAULT 0,
  `stars` tinyint(3) UNSIGNED NOT NULL DEFAULT 0,
  `has_picture` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `liked`
--

CREATE TABLE `liked` (
  `id_user` int(12) NOT NULL,
  `id_house` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(12) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` char(60) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `phone_number` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `buys`
--
ALTER TABLE `buys`
  ADD PRIMARY KEY (`id_user`,`id_house`),
  ADD KEY `buys_ibfk_2` (`id_house`);

--
-- Indices de la tabla `disliked`
--
ALTER TABLE `disliked`
  ADD PRIMARY KEY (`id_user`,`id_house`),
  ADD KEY `disliked_ibfk_2` (`id_house`);

--
-- Indices de la tabla `has_favorites`
--
ALTER TABLE `has_favorites`
  ADD PRIMARY KEY (`id_user`,`id_house`),
  ADD KEY `has_favorites_ibfk_1` (`id_house`);

--
-- Indices de la tabla `houses`
--
ALTER TABLE `houses`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `liked`
--
ALTER TABLE `liked`
  ADD PRIMARY KEY (`id_user`,`id_house`),
  ADD KEY `liked_ibfk_1` (`id_house`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `houses`
--
ALTER TABLE `houses`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=125;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `buys`
--
ALTER TABLE `buys`
  ADD CONSTRAINT `buys_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `buys_ibfk_2` FOREIGN KEY (`id_house`) REFERENCES `houses` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `disliked`
--
ALTER TABLE `disliked`
  ADD CONSTRAINT `disliked_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `disliked_ibfk_2` FOREIGN KEY (`id_house`) REFERENCES `houses` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Filtros para la tabla `has_favorites`
--
ALTER TABLE `has_favorites`
  ADD CONSTRAINT `has_favorites_ibfk_1` FOREIGN KEY (`id_house`) REFERENCES `houses` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `has_favorites_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Filtros para la tabla `liked`
--
ALTER TABLE `liked`
  ADD CONSTRAINT `liked_ibfk_1` FOREIGN KEY (`id_house`) REFERENCES `houses` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `liked_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
