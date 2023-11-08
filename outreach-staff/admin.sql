CREATE TABLE `admin` (
  `id` integer NOT NULL,
  `name` text NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(20) NOT NULL,
  `last_signin` varchar(20) DEFAULT NULL,
  `last_signout` varchar(20) DEFAULT NULL,
  `session_time` varchar(30) DEFAULT NULL
);