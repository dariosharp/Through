# Define the library name
MYLIB_NAME = mylib

# Define the program name
PROGRAM_NAME = program

# Compile the library source files into object files
%.o: %.c
	gcc -fPIC -c $< -o $@

# Link the object files into a shared library
$(MYLIB_NAME).so: $(MYLIB_NAME).o
	gcc -shared $(MYLIB_NAME).o -o $(MYLIB_NAME).so

# Compile the program source files into object files
%.o: %.c
	gcc -c $< -o $@

# Link the program object files with the library
$(PROGRAM_NAME): $(PROGRAM_NAME).o $(MYLIB_NAME).so
	gcc $(PROGRAM_NAME).o -o $(PROGRAM_NAME) $(MYLIB_NAME).so
	rm  $(PROGRAM_NAME).o $(MYLIB_NAME).o

# Clean up the object files and library
clean:
	rm -f $(MYLIB_NAME).o $(MYLIB_NAME).so $(PROGRAM_NAME).o $(PROGRAM_NAME)

# Default target
all: $(PROGRAM_NAME)
