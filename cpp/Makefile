CXX := g++
CXXFLAGS := -Wall -Wextra -O2 -std=c++17 -Iinclude

BUILD_DIR := build
TARGET := $(BUILD_DIR)/scc_tarjan
TEST_TARGET := $(BUILD_DIR)/test_tarjan

SRC := src/graph.cpp src/tarjan.cpp src/trace.cpp src/main.cpp
TEST_SRC := tests/test_tarjan.cpp src/graph.cpp src/tarjan.cpp src/trace.cpp

.PHONY: all clean test

all: $(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(TARGET): $(BUILD_DIR) $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $@

$(TEST_TARGET): $(BUILD_DIR) $(TEST_SRC)
	$(CXX) $(CXXFLAGS) $(TEST_SRC) -o $@

test: $(TEST_TARGET)
	cd .. && ./cpp/build/test_tarjan

clean:
	rm -rf $(BUILD_DIR)
