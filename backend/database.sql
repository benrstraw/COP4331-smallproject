CREATE TABLE `users` (
  `userid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COMMENT='Holds the data for our user accounts.'
CREATE TABLE `contacts` (
  `contactid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userid` int(10) unsigned NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`contactid`),
  KEY `contacts_FK` (`userid`),
  FULLTEXT KEY `contacts_fulltext_IDX` (`first_name`,`last_name`,`phone`,`email`,`address`),
  CONSTRAINT `contacts_FK` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COMMENT='Holds the individual contact entries for all users.'
