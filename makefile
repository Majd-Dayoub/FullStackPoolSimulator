CC = clang
CFLAGS = -std=c99 -Wall -pedantic -fPIC
LDFLAGS = -shared
TARGET = libphylib.so
SRC = phylib.c
OBJ = phylib.o
PYTHON_INCLUDE = /usr/include/python3.11  # Make sure its correct
PYTHON_LIB = /usr/lib/python3.11          # Make sure its correct

# Default target is 'all'
.DEFAULT_GOAL := all

# Target: phylib.o
phylib.o: $(SRC)
	$(CC) $(CFLAGS) -c -o $(OBJ) $(SRC)

# Target: libphylib.so
libphylib.so: $(OBJ)
	$(CC) $(LDFLAGS) -o $(TARGET) $(OBJ) -lm

# Target: phylib_wrap.c
phylib_wrap.c: phylib.i
	swig -python phylib.i

# Target: phylib_wrap.o
phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c -o phylib_wrap.o phylib_wrap.c -I$(PYTHON_INCLUDE)

# Target: _phylib.so
_phylib.so: phylib_wrap.o $(TARGET)
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L$(PYTHON_LIB) -lpython3.11 -lphylib -o _phylib.so

# Target: all
all: libphylib.so _phylib.so


# Target: clean
clean:
	rm -f $(TARGET) $(OBJ) phylib_wrap.c phylib_wrap.o _phylib.so
	rm -f *.svg
