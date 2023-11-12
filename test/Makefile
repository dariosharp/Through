MYLIB_NAME = mylib
MYLIB_NAME_32 = mylib32

PROGRAM_NAME = program
PROGRAM_NAME_32 = program32

LIB_DIR = ./lib

$(LIB_DIR):
	mkdir -p $(LIB_DIR)

$(MYLIB_NAME).o: $(MYLIB_NAME).c
	gcc -fPIC -c $< -o $@

$(MYLIB_NAME_32).o: $(MYLIB_NAME).c
	gcc -m32 -fPIC -c $< -o $@

$(MYLIB_NAME).so: $(MYLIB_NAME).o | $(LIB_DIR)
	gcc -shared $(MYLIB_NAME).o -o $(LIB_DIR)/$(MYLIB_NAME).so

$(MYLIB_NAME_32).so: $(MYLIB_NAME_32).o | $(LIB_DIR)
	gcc -shared -m32 $(MYLIB_NAME_32).o -o $(LIB_DIR)/$(MYLIB_NAME_32).so

$(PROGRAM_NAME_32).o: $(PROGRAM_NAME).c
	gcc -m32 -c $< -o $@

$(PROGRAM_NAME): $(PROGRAM_NAME).o $(MYLIB_NAME).so | $(LIB_DIR)
	gcc $(PROGRAM_NAME).o -o $(PROGRAM_NAME) $(LIB_DIR)/$(MYLIB_NAME).so
	rm $(PROGRAM_NAME).o $(MYLIB_NAME).o

$(PROGRAM_NAME_32): $(PROGRAM_NAME_32).o $(MYLIB_NAME_32).so | $(LIB_DIR)
	gcc $(PROGRAM_NAME_32).o -o $(PROGRAM_NAME_32) -m32 $(LIB_DIR)/$(MYLIB_NAME_32).so
	rm $(PROGRAM_NAME_32).o $(MYLIB_NAME_32).o

clean:
	rm -rf $(PROGRAM_NAME) $(LIB_DIR)/$(MYLIB_NAME).so $(PROGRAM_NAME_32) $(LIB_DIR)/$(MYLIB_NAME_32).so

all: $(PROGRAM_NAME) $(PROGRAM_NAME_32)

