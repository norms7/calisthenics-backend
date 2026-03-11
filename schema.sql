-- ============================================================
-- Calisthenics Planner — MySQL Schema
-- Run this entire file in MySQL Workbench before starting the backend
-- ============================================================

CREATE DATABASE IF NOT EXISTS calisthenics_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE calisthenics_db;

CREATE TABLE IF NOT EXISTS users (
  id                INT          AUTO_INCREMENT PRIMARY KEY,
  username          VARCHAR(50)  NOT NULL UNIQUE,
  email             VARCHAR(100) NOT NULL UNIQUE,
  password_hash     VARCHAR(255) NOT NULL,
  fitness_level     ENUM('Beginner','Intermediate','Advanced') NOT NULL DEFAULT 'Beginner',
  notification_time TIME         NULL,
  created_at        DATETIME     DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS exercises (
  id              INT          AUTO_INCREMENT PRIMARY KEY,
  name            VARCHAR(100) NOT NULL,
  muscle_groups   VARCHAR(255) NOT NULL,
  description     TEXT         NOT NULL,
  instructions    TEXT         NOT NULL,
  common_mistakes TEXT,
  difficulty      ENUM('Beginner','Intermediate','Advanced') NOT NULL,
  base_sets       INT          NOT NULL DEFAULT 3,
  base_reps       INT          NOT NULL DEFAULT 10,
  rest_seconds    INT          NOT NULL DEFAULT 60,
  workout_type    ENUM('Full Body','Upper Body','Lower Body','Core') NOT NULL,
  image_url       VARCHAR(255) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS workout_plans (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  user_id      INT NOT NULL,
  week_number  INT NOT NULL DEFAULT 1,
  workout_type ENUM('Full Body','Upper Body','Lower Body','Core') NOT NULL,
  difficulty   ENUM('Beginner','Intermediate','Advanced') NOT NULL,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS workout_sessions (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  user_id          INT  NOT NULL,
  plan_id          INT  NULL,
  session_date     DATE NOT NULL,
  status           ENUM('pending','in_progress','completed','skipped') NOT NULL DEFAULT 'pending',
  duration_minutes INT  NULL,
  completed_at     DATETIME NULL,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (plan_id) REFERENCES workout_plans(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS exercise_logs (
  id             INT  AUTO_INCREMENT PRIMARY KEY,
  session_id     INT  NOT NULL,
  exercise_id    INT  NOT NULL,
  sets_completed INT  NOT NULL,
  reps_completed INT  NOT NULL,
  is_completed   BOOL NOT NULL DEFAULT FALSE,
  FOREIGN KEY (session_id)  REFERENCES workout_sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (exercise_id) REFERENCES exercises(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS progress_stats (
  id                    INT          AUTO_INCREMENT PRIMARY KEY,
  user_id               INT          NOT NULL UNIQUE,
  total_workouts        INT          NOT NULL DEFAULT 0,
  current_streak        INT          NOT NULL DEFAULT 0,
  longest_streak        INT          NOT NULL DEFAULT 0,
  total_exercises       INT          NOT NULL DEFAULT 0,
  weekly_completion_pct DECIMAL(5,2) NOT NULL DEFAULT 0.00,
  last_workout_date     DATE         NULL,
  updated_at            DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
