-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema thewall
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema thewall
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `thewall` DEFAULT CHARACTER SET utf8 ;
USE `thewall` ;

-- -----------------------------------------------------
-- Table `thewall`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thewall`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thewall`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thewall`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NULL DEFAULT NULL,
  `message` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_messages_users1_idx` (`users_id` ASC),
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `thewall`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 29
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thewall`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thewall`.`comments` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `messages_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `comment` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `users_id` INT(11) NOT NULL,
  `messages_id1` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_users_idx` (`users_id` ASC),
  INDEX `fk_comments_messages1_idx` (`messages_id1` ASC),
  CONSTRAINT `fk_comments_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `thewall`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_messages1`
    FOREIGN KEY (`messages_id1`)
    REFERENCES `thewall`.`messages` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 19
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
