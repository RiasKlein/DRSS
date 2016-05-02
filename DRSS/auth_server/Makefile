# Manage the build of the application and run it
#
# Based on the following:
# http://hiltmon.com/blog/2013/07/03/a-simple-c-plus-plus-project-structure/
#

CC := g++ -std=c++11
SRCDIR := src
BUILDDIR := build
TARGET := bin/auth_server

SRCEXT := cpp
SOURCES := $(shell find $(SRCDIR) -type f -name *.$(SRCEXT))
OBJECTS := $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.$(SRCEXT)=.o))
CFLAGS := -g -Wall
LIB := #-pthread
INC := -I include

$(TARGET): $(OBJECTS)
	@echo " Linking..."
	@echo " $(CC) $^ -o $(TARGET) $(LIB)"; $(CC) $^ -o $(TARGET) $(LIB)

$(BUILDDIR)/%.o: $(SRCDIR)/%.$(SRCEXT)
	@mkdir -p $(BUILDDIR)
	@echo " $(CC) $(CFLAGS) $(INC) -c -o $@ $<"; $(CC) $(CFLAGS) $(INC) -c -o $@ $<

clean:
	@echo " Cleaning...";
	@echo " $(RM) -r $(BUILDDIR)/*.o $(TARGET)"; $(RM) -r $(TARGET) $(BUILDDIR)/*.o
	@echo " $(RM) -r bin/*"; $(RM) -r bin/*

