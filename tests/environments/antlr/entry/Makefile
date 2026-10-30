# variables
OUT_DIR     := bin
JAR_NAME    := target.jar
TARGET_NAME := target/target-1.0-SNAPSHOT-jar-with-dependencies.jar

.PHONY: all

all:
	mvn package
	mkdir -p $(OUT_DIR)
	cp  $(TARGET_NAME) $(OUT_DIR)/$(JAR_NAME)
